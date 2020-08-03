import os
import psycopg2
import flask
import app.config as config


conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_DBNAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
)

app = flask.Flask(__name__)



@app.route('/', methods=['POST'])
def post_playlist():
    data = flask.request
    print()
    # print(data)
    # print(type(data))
    # print('data.args: ', data.args)
    # print('data.data: ', data.data)
    # print('data.form: ', data.form)
    # print('data.from_values(): ', data.from_values())
    # print('data.get_data(): ', data.get_data())
    # print('data.get_json(): ', data.get_json())
    # print('data.json: ', data.json)
    # print('data.values: ', data.values)
    print()
    # print(data.get_json(force=True))
    # print(data.get_json())
    print(flask.request.json)
    print(flask.request.json['a'])
    print(type(flask.request.json['a']))
    # print(flask.request.get_json())
    # print(dir(data.form))
    # print(data.form.to_dict())
    print()
    return 'askdfhj\n'



if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG'),
        host=os.environ['FLASK_HOST'],
        port=os.environ['FLASK_PORT'],
    )
