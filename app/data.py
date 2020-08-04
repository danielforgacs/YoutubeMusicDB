import os
import psycopg2



class PGConnection:
    def __init__(self, dbname=None):
        self.dbname = dbname or os.getenv('DB_DBNAME')

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



def create_playlist(title, ytid):
    sql = """
INSERT INTO playlist (title, youtubeid)
VALUES (%s, %s)
"""

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(sql, (title, ytid))
        conn.commit()



if __name__ == '__main__':
    pass
