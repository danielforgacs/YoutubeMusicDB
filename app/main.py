import os
import flask
import json
import app.config as config
import app.data as data
import app.youtube as youtube


DOWNLOAD_DIR = '/home/download/'


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

    for videoid in videoids:
        print('<<< DOWNLOADING >>>', videoid)
        os.chdir(DOWNLOAD_DIR)
        ytdl = youtube.Youtube(url=videoid, do_download=True)

    response = {'videos': str(videoids)}
    # response = {'videos': str(videoids),
    #     'cwd': os.getcwd(),
    #     '__filw__': __file__,
    #     '_ss_filw__': os.path.dirname(__file__),
    #     '__filw_ss_': os.path.abspath(__file__),
    # }

    return response




if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
