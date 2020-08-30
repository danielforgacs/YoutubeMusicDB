import os
import psycopg2
import datetime
import json



class PGConnection:
    def __init__(self, dbname=None):
        self.dbname = dbname or os.getenv('PGDATABASE')

    def __enter__(self, *args, **kwargs):
        print('\n### dbname', self.dbname)
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=self.dbname,
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )
        return self.conn


    def __exit__(self, errtype, err, traceback):
        self.conn.close()




def select_all_videos():
    sql = """
        SELECT pk
        FROM playlist
        ;
    """

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql)
        rows = cur.fetchall()
        # print('@@@ conn.dbname:', conn.dbname)

    print('\nROWS:', rows)

    data = {
        str(row[0]): {
        # row[0]: {
            'pk': row[0]
        } for row in rows
    }

    # print(data)
    # data_j = json.dumps(data)
    # data_j = data
    # print(data_j)

    return data


# select_all_videos()
