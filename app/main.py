import os
import flask
import json
import app.config as config
import app.data as data
import app.youtube as youtube


app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
def post_playlist():
    print(flask.request.json['id'])
    print(flask.request.json['id'])
    print(type(flask.request.json['id']))
    print(type(flask.request.json['id']))
    ytdl = youtube.Youtube()
    ytdl.url = flask.request.json['id']
    ytdl.fetch_info()

    if ytdl.playlist:
        data = ytdl.playlist.as_dict
    else:
        data = ytdl.video.as_dict


    return flask.jsonify(data)



if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
