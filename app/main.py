import os
import flask
import json
import app.config as config
import app.data as data
import app.youtube as youtube


app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
def post_playlist():
    ytid = flask.request.json.get('id')

    if not ytid:
        return flask.jsonify({'error': 'missing id'})


    ytdl = youtube.Youtube(url=ytid)

    if ytdl.playlist:
        download = ytdl.playlist.as_dict
    else:
        download = ytdl.video.as_dict

    response = flask.jsonify(download)

    return response




@app.route('/download', methods=['POST'])
def download_playlist():
    ytid = flask.request.json.get('id')

    if not ytid:
        return flask.jsonify({'error': 'missing id'})

    videoids = data.query_videos_by_playlistid(playlistid=ytid)
    print('>>> ytid', ytid)
    response = {'lkjh': 123}

    return response




if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
