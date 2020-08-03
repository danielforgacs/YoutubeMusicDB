import os
import flask
import app.config as config
import app.data as data


app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
def post_playlist():
    data = flask.request.json
    return 'askdfhj\n{}\n'.format(data)



if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
