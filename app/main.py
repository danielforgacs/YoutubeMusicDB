import os
import flask
import json
import zipfile
import uuid
# import app.data as data
import app.youtube as youtube
from app import config


DB_ACCESS_HOST = os.environ['DBACCESS_RPC_HOST']
DB_ACCESS_PORT = int(os.environ['DBACCESS_RPC_PORT'])
DB_ACCESS_URL = 'http://{host}:{port}'.format(host=DB_ACCESS_HOST, port=DB_ACCESS_PORT)
RPC_CLIENT_KWARGS = {
    'uri': DB_ACCESS_URL,
    'allow_none': True,
}


ROOT_DIR = (
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
)
)


DOWNLOAD_DIR = os.path.join(ROOT_DIR, '.download')

if not os.path.isdir(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)



app = flask.Flask(__name__)



@app.route('/api/createplaylist', methods=['POST'])
def post_playlist():
    ytid = flask.request.json.get('id')

    if not ytid:
        return flask.jsonify({'error': 'missing id'})

    ytdl = youtube.Youtube(url=ytid)

    if ytdl.error:
        return {'error': ytdl.error}

    if ytdl.playlist:
        vids = [video.id for video in ytdl.playlist.videos]
    else:
        vids = [ytdl.video.id]

    videos = data.select_videos_by_id(vids=vids)
    context = {'videos': videos}
    response = flask.jsonify(context)

    return response





@app.route('/api/download', methods=['POST'])
def download_playlist():
    ytid_raw = flask.request.json.get('id')

    if not ytid_raw:
        return flask.jsonify({'error': 'missing id'})

    yout = youtube.Youtube(url=ytid_raw, do_download=False)

    if not yout.playlist:
        return flask.jsonify({'error': 'id is not a playlist'})

    ytid = yout.playlist.id

    archver = 0

    while True:
        archivename = config.DOWNLOAD_ZIP_NAME.format(
            plid=ytid,
            ver=archver,
        )
        archivepath = os.path.join(DOWNLOAD_DIR, archivename)

        if os.path.isfile(archivepath):
            archver += 1
        else:
            break


    videos = data.select_videos_by_playlistid(playlistid=ytid)
    titles = []

    for video in videos:
        if video['is_down']:
            continue

        os.chdir(DOWNLOAD_DIR)
        ytdl = youtube.Youtube(url=video['id'], do_download=True)
        data.set_video_as_downloaded(vid=video['id'])
        titles.append(ytdl.video.title)

    downloads = os.listdir(DOWNLOAD_DIR)

    with zipfile.ZipFile(archivepath, 'w') as downlfile:
        for fname in downloads:
            if fname.startswith(config.DOWNLOAD_ZIP_PREFIX):
                continue

            downlfile.write('{}'.format(fname))

    videofiles = os.listdir(path=DOWNLOAD_DIR)

    for vfile in videofiles:
        if vfile.startswith(config.DOWNLOAD_ZIP_PREFIX):
            continue

        os.remove(vfile)

    response = {
        'videos': videos,
        'archive': archivename,
    }

    return response




@app.route('/api/archive/<string:zipname>')
def archive(zipname):
    return flask.send_file(os.path.join(DOWNLOAD_DIR, zipname))




@app.route('/api/all_videos', methods=['GET'])
def GET_all_videos():
    allvids = data.select_all_videos()
    context = {
        'videos': allvids
    }

    return flask.jsonify(context)





@app.route('/', methods=['GET', 'POST'])
def view_playlists():
    if flask.request.method == 'POST':
        if flask.request.form:
            ytdl = youtube.Youtube(url=flask.request.form['id'])

    if flask.request.json:
        vid = flask.request.json.get('id')
        ytdl = youtube.Youtube(url=vid)

    allvids = data.select_all_videos()
    context = {
        'videos': allvids
    }

    return flask.render_template(template_name_or_list='allvideos.html', context=context)




if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
