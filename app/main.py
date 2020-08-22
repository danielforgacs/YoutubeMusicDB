import os
import flask
import json
import zipfile
import uuid
import app.data as data
import app.youtube as youtube
from app import config

ROOT_DIR = (
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
)
)


DOWNLOAD_DIR = os.path.join(ROOT_DIR, '.download')

if not os.path.isdir(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

ARCHIVE_NAME = os.path.join(DOWNLOAD_DIR, 'download.zip')


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
        download = ytdl.playlist.as_dict
    else:
        download = ytdl.video.as_dict

    response = flask.jsonify(download)

    return response




@app.route('/api/download', methods=['POST'])
def download_playlist():
    ytid = flask.request.json.get('id')

    if not ytid:
        return flask.jsonify({'error': 'missing id'})

    print('::ytid:', ytid)
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


    videoids = data.query_videos_by_playlistid(playlistid=ytid)
    print('::videoids:', videoids)
    titles = []

    for videoid in videoids:
        os.chdir(DOWNLOAD_DIR)
        ytdl = youtube.Youtube(url=videoid, do_download=True)
        data.set_video_as_downloaded(vid=videoid)
        titles.append(ytdl.video.title)

    downloads = os.listdir(DOWNLOAD_DIR)

    with zipfile.ZipFile(archivename, 'w') as downlfile:
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
        'videos': videoids,
        'archive': archivename,
    }

    return response




@app.route('/api/archive')
def archive():
    return flask.send_file(ARCHIVE_NAME)




@app.route('/', methods=['GET', 'POST'])
def view_playlists():
    print('--> view_playlists')
    print('--> flask.request', flask.request)
    print('--> flask.request.json', flask.request.json)
    
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
