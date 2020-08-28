import os
import psycopg2
import datetime



IDX_PLAYLIST__pk = 0
IDX_PLAYLIST__id = 1
IDX_PLAYLIST__title = 2
IDX_PLAYLIST__uploader_id = 3

IDX_VIDEO__pk = 0
IDX_VIDEO__id = 1
IDX_VIDEO__title = 2
IDX_VIDEO__playlist = 3


SQL_INSERT_PLAYLIST = """
    INSERT INTO playlist (id, title, uploader_id, added)
    VALUES (%(id)s, %(title)s, %(uploader_id)s, %(added)s)
    ON CONFLICT (id) DO UPDATE SET
        title = %(title)s,
        uploader_id = %(uploader_id)s
    RETURNING pk
    ;
"""

SQL_INSERT_VIDEO = """
    INSERT INTO video (id, title, playlist, added)
    VALUES (%(id)s, %(title)s, %(playlist)s, %(added)s)
    ON CONFLICT (id) DO UPDATE SET
        title = %(title)s
    RETURNING pk
    ;
"""

SQL_VIDEO_BY_PLAYLIST = """
    SELECT video.id, video.is_down
    FROM video
    JOIN playlist ON playlist.pk = video.playlist
    WHERE playlist.id = %(plid)s
    ;
"""

SQL_SET_VIDEO_PLAYLIST = """
    UPDATE video
    SET playlist = %(plpk)s
    WHERE video.id = %(vid)s
    RETURNING pk, id, title, playlist
    ;
"""

SQL_SET_VIDEO_AS_DOWNLOADED = """
    UPDATE video
    SET is_down = true
    WHERE id = %(id)s
    RETURNING pk
    ;
"""

SQL_SELECT_ALL_VIDEOS = """
    SELECT
        video.pk,
        video.title,
        video.is_down,
        video.added,
        video.id AS youtube_id,
        playlist.title AS playlist,
        playlist.id AS playlistid
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlist
    ;
"""


SQL_SELECT_VIDEOS_BY_IDS = """
    SELECT
        video.pk,
        video.title,
        video.is_down,
        video.added,
        video.id AS youtube_id,
        playlist.title AS playlist,
        playlist.id AS playlistid
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlist
    WHERE video.id in %(vids)s
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
    pldict['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_PLAYLIST, pldict)
        conn.commit()
        row = cur.fetchone()

    pk = row[IDX_PLAYLIST__pk]

    return pk



def insert_video(vdata):
    vdata.setdefault('playlist', None)
    vdata['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_VIDEO, vdata)
        conn.commit()
        row = cur.fetchone()

    pk = row[IDX_VIDEO__pk]

    return pk



def query_videos_by_playlistid(playlistid):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_VIDEO_BY_PLAYLIST, {'plid': playlistid})
        conn.commit()
        rows = cur.fetchall()

    result = [row[0] for row in rows]

    return result




def set_video_playlist(vid, plpk):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_SET_VIDEO_PLAYLIST, {'vid': vid, 'plpk': plpk})
        conn.commit()
        row = cur.fetchone()

    result = [
        row[IDX_VIDEO__pk],
        row[IDX_VIDEO__id],
        row[IDX_VIDEO__playlist],
    ]

    return result




def set_video_as_downloaded(vid):
    data = {'id': vid}

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SET_VIDEO_AS_DOWNLOADED, vars=data)
        conn.commit()
        row = cur.fetchone()

    pk = row[0]

    return pk



def select_all_videos():
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_ALL_VIDEOS)
        rows = cur.fetchall()

    return rows




def select_videos_by_id(vids):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_VIDEOS_BY_IDS, vars={'vids': tuple(vids)})
        rows = cur.fetchall()

    return rows





if __name__ == '__main__':
    pass
