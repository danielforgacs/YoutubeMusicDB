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




def video_row_to_dict(row):
    playlisttitle_idx = 6
    row = {
        'id': row[VIDEO_ID_IDX],
        'title': row[VIDEO_TITLE_IDX],
        'playlistid': row[VIDEO_PLAYLIST_IDX],
        'added': str(row[VIDEO_ADDED_IDX]),
        'is_down': row[VIDEO_IS_DOWN_IDX],
        'playlisttitle': row[playlisttitle_idx] or None,
    }
    return row




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

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql)
        rows = cur.fetchall()

    data = {
        row[VIDEO_ID_IDX]: video_row_to_dict(row=row)
        for row in rows
    }

    return data




def select_videos_by_id(vids):
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
        WHERE video.id in %(vids)s
        ;
    """

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vids': vids})
        rows = cur.fetchall()

    data = {
        row[VIDEO_ID_IDX]: video_row_to_dict(row=row)
        for row in rows
    }

    return data




def set_video_as_downloaded(vid):
    sql = """
        UPDATE video
        SET is_down = true
        WHERE id = %(id)s
        ;
    """

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'id': vid})
        conn.commit()

    result = select_videos_by_id(vids=(vid,))

    return result




def set_video_playlist(vid, plpk):
    sql = """
        UPDATE video
        SET playlist = %(plpk)s
        WHERE video.id = %(vid)s
        RETURNING pk, id, title, playlist
        ;
    """
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(sql, {'vid': vid, 'plpk': plpk})
        conn.commit()

    result = select_videos_by_id(vids=(vid,))

    return result




def query_videos_by_playlistid(playlistid):
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
        JOIN playlist ON playlist.pk = video.playlist
        WHERE playlist.id = %(plid)s
        ;
    """
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(sql, {'plid': playlistid})
        conn.commit()
        rows = cur.fetchall()

    data = {
        row[VIDEO_ID_IDX]: video_row_to_dict(row=row)
        for row in rows
    }

    return data




def insert_video(vdata):
    sql = """
        INSERT INTO video (id, title, playlist, added)
        VALUES (%(id)s, %(title)s, %(playlist)s, %(added)s)
        ON CONFLICT (id) DO UPDATE SET
            title = %(title)s
        RETURNING pk, id
        ;
    """
    vdata.setdefault('playlist', None)
    vdata['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(sql, vdata)
        conn.commit()
        row = cur.fetchone()

    result = select_videos_by_id(vids=(row[VIDEO_ID_IDX],))

    return result
