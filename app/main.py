import os
import flask
import json
import zipfile
import app.config as config
import app.data as data
import app.youtube as youtube

ROOT_DIR = (
    os.path.dirname(
        os.path.dirname(__file__)
))


# DOWNLOAD_DIR = '/home/download/'
DOWNLOAD_DIR = os.path.join(ROOT_DIR, '.download')
ARCHIVE_NAME = os.path.join(DOWNLOAD_DIR, 'download.zip')

print(ROOT_DIR)
print(DOWNLOAD_DIR)
print(ARCHIVE_NAME)

app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
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




@app.route('/download', methods=['POST'])
def download_playlist():
    print()
    print(os.getcwd())
    print(__file__)
    ytid = flask.request.json.get('id')

    if not ytid:
        return flask.jsonify({'error': 'missing id'})

    videoids = data.query_videos_by_playlistid(playlistid=ytid)
    titles = []

    for videoid in videoids:
        print('<<< DOWNLOADING >>>', videoid)
        os.chdir(DOWNLOAD_DIR)
        ytdl = youtube.Youtube(url=videoid, do_download=True)
        print('-- downloaded: ', ytdl.video.title)
        titles.append(ytdl.video.title)

    downloads = os.listdir(DOWNLOAD_DIR)

    with zipfile.ZipFile(ARCHIVE_NAME, 'w') as downlfile:
        for fname in downloads:
            downlfile.write('{}'.format(fname))

    response = {'videos': str(videoids)}

    return response




@app.route('/archive')
def archive():
    # return flask.send_file('/home/download/download.zip')
    return flask.send_file('/home/ford/storage/dev/YoutubeMusicDB/.download/download.zip')




if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
