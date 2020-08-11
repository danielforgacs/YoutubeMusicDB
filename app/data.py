import os
import psycopg2



IDX_PLAYLIST__id = 0
IDX_PLAYLIST__youtubeid = 1
IDX_PLAYLIST__title = 2
IDX_PLAYLIST__uploaderid = 3

SQL_INSERT_PLAYLIST = """
INSERT INTO playlist (youtubeid, title, uploaderid)
VALUES (%(id)s, %(title)s, %(uploader_id)s)
ON CONFLICT (youtubeid) DO UPDATE SET
    title = %(title)s,
    uploaderid = %(uploader_id)s
RETURNING id
;
"""


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




def insert_playlist(pldict):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_PLAYLIST, pldict)
        conn.commit()
        row = cur.fetchone()

    plid = row[IDX_PLAYLIST__id]

    return plid



def insert_video(video):
    # print('\nDB_INSERT - VIDEO')
    sql = """
"""



if __name__ == '__main__':
    pass
