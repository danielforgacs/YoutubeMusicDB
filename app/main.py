import os
import flask
import json
import app.config as config
import app.data as data
import app.youtube as youtube


app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
def post_playlist():
    result = {}
    ytid = flask.request.json.get('id')

    if not ytid:
        result = {'error': 'missing id'}

    else:
        ytdl = youtube.Youtube()
        ytdl.url = ytid
        ytdl.fetch_info()

        if ytdl.playlist:
            data = ytdl.playlist.as_dict
        elif ytdl.video:
            data = ytdl.video.as_dict
        else:
            result = {'error': 'something wrong'}


    return flask.jsonify(result)



if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
