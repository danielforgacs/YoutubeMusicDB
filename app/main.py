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



if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'))
