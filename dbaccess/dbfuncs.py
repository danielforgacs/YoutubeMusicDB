import os
import psycopg2
import datetime
import json


VIDEO_PK_IDX = 0
VIDEO_ID_IDX = 1
VIDEO_TITLE_IDX = 2
VIDEO_PLAYLIST_IDX = 3
VIDEO_ADDED_IDX = 4
VIDEO_IS_DOWN_IDX = 5



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
        SELECT
            video.pk,
            video.id AS youtube_id,
            video.title,
            playlist.id AS playlistid,
            video.added,
            video.is_down,
            playlist.title AS playlist
        FROM video
        LEFT JOIN playlist ON playlist.pk = video.playlist
    """
    playlisttitle_idx = 6

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql)
        rows = cur.fetchall()

    data = {
        row[VIDEO_ID_IDX]: {
            'id': row[VIDEO_ID_IDX],
            'title': row[VIDEO_TITLE_IDX],
            'playlistid': row[VIDEO_PLAYLIST_IDX],
            'added': str(row[VIDEO_ADDED_IDX]),
            'is_down': row[VIDEO_IS_DOWN_IDX],
            'playlisttitle': row[playlisttitle_idx] or None,
        } for row in rows
    }

    return data
