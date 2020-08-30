import os
import psycopg2
import datetime


print("::os.getenv('PGDATABASE'):", os.getenv('PGDATABASE'))
print("::os.getenv('DB_HOST'):", os.getenv('DB_HOST'))
print("::os.getenv('DB_PORT'):", os.getenv('DB_PORT'))
# print("::self.dbname:", self.dbname)
print("::os.getenv('DB_USER'):", os.getenv('DB_USER'))
print("::os.getenv('DB_PASSWORD'):", os.getenv('DB_PASSWORD'))


class PGConnection:
    def __init__(self, dbname=None):
        self.dbname = dbname or os.getenv('PGDATABASE')

    def __enter__(self, *args, **kwargs):
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
        FROM video
        ;
    """

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql)
        rows = cur.fetchall()

    data = {
        row[0]: {
            'pk': row[0]
        } for row in rows
    }

    return data
