import os
import psycopg2
import datetime


PLAYLIST_COLUMNT_IDX__pk, PLAYLIST_COLUMNT_NAME__pk = 0, 'pk'
PLAYLIST_COLUMNT_IDX__id, PLAYLIST_COLUMNT_NAME__id = 1, 'id'
PLAYLIST_COLUMNT_IDX__title, PLAYLIST_COLUMNT_NAME__title = 2, 'title'
PLAYLIST_COLUMNT_IDX__uploader_id, PLAYLIST_COLUMNT_NAME__uploader_id = 3, 'uploader_id'
PLAYLIST_COLUMNT_IDX__added, PLAYLIST_COLUMNT_NAME__added = 4, 'added'


VIDEO_COLUMN_IDX__pk, VIDEO_COLUMN_NAME__pk = 0, 'pk'
VIDEO_COLUMN_IDX__id, VIDEO_COLUMN_NAME__id = 1, 'id'
VIDEO_COLUMN_IDX__title, VIDEO_COLUMN_NAME__title = 2, 'title'
VIDEO_COLUMN_IDX__playlist_id, VIDEO_COLUMN_NAME__playlist_id = 3, 'playlistid'
VIDEO_COLUMN_IDX__added, VIDEO_COLUMN_NAME__added = 4, 'added'
VIDEO_COLUMN_IDX__is_down, VIDEO_COLUMN_NAME__is_down = 5, 'is_down'
VIDEO_COLUMN_IDX__playlist_title, VIDEO_COLUMN_NAME__playlist_title = 6, 'playlisttitle'
VIDEO_COLUMN_IDX__playlist_data, VIDEO_COLUMN_NAME__playlist_data = 7, 'playlist_data'



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
    playlist_data = row[VIDEO_COLUMN_IDX__playlist_data]
    playlists = []

    if playlist_data:
        playlists = list(map(lambda x: x + [None, None], playlist_data))
        playlists = list(map(playlist_row_to_dict, playlists))

    row = {
        VIDEO_COLUMN_NAME__pk: row[VIDEO_COLUMN_IDX__pk],
        VIDEO_COLUMN_NAME__id: row[VIDEO_COLUMN_IDX__id],
        VIDEO_COLUMN_NAME__title: row[VIDEO_COLUMN_IDX__title],
        VIDEO_COLUMN_NAME__playlist_id: row[VIDEO_COLUMN_IDX__playlist_id],
        VIDEO_COLUMN_NAME__added: str(row[VIDEO_COLUMN_IDX__added]),
        VIDEO_COLUMN_NAME__is_down: row[VIDEO_COLUMN_IDX__is_down],
        VIDEO_COLUMN_NAME__playlist_title: row[VIDEO_COLUMN_IDX__playlist_title] or None,
        VIDEO_COLUMN_NAME__playlist_data: playlists,
    }
    return row



def playlist_row_to_dict(row):
    rowdict = {
        PLAYLIST_COLUMNT_NAME__pk: row[PLAYLIST_COLUMNT_IDX__pk],
        PLAYLIST_COLUMNT_NAME__id: row[PLAYLIST_COLUMNT_IDX__id],
        PLAYLIST_COLUMNT_NAME__title: row[PLAYLIST_COLUMNT_IDX__title],
        PLAYLIST_COLUMNT_NAME__uploader_id: row[PLAYLIST_COLUMNT_IDX__uploader_id],
        PLAYLIST_COLUMNT_NAME__added: row[PLAYLIST_COLUMNT_IDX__added],
    }
    return rowdict


SQL_SELECT_ALL_VIDEOS = """
    SELECT
        video.pk,
        video.id AS youtube_id,
        video.title,
        playlist.id AS playlistid,
        video.added,
        video.is_down,
        playlist.title AS playlist,
        (
            SELECT array_agg ( array [ playlist.pk::text, playlist.id, playlist.title ])
            FROM playlist
            JOIN playlist_video ON playlist_video.playlist_pk = playlist.pk
            WHERE video.pk = playlist_video.video_pk
        ) AS playlist_data
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlist_pk
    ORDER BY video.pk
    ;
"""

SQL_SELECT_VIDEOS_BY_ID = """
    SELECT
        video.pk,
        video.id AS youtube_id,
        video.title,
        playlist.id AS playlistid,
        video.added,
        video.is_down,
        playlist.title AS playlist,
        (
            SELECT array_agg ( array [ playlist.pk::text, playlist.id, playlist.title ])
            FROM playlist
            JOIN playlist_video ON playlist_video.playlist_pk = playlist.pk
            WHERE video.pk = playlist_video.video_pk
        ) AS playlist_data
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlist_pk
    WHERE video.id in %(vids)s
    ORDER BY video.pk
    ;
"""

SQL_SET_VIDEO_AS_DOWNLOADED = """
    UPDATE video
    SET is_down = true
    WHERE id = %(id)s
    ;
"""

SQL_SET_VIDEO_PLAYLIST = """
    UPDATE video
    SET playlist_pk = %(plpk)s
    WHERE video.id = %(vid)s
    RETURNING pk, id, title, playlist_pk
    ;
"""

SQL_SELECT_VIDEOS_BY_PLAYLISTID = """
    SELECT
        video.pk,
        video.id AS youtube_id,
        video.title,
        playlist.id AS playlistid,
        video.added,
        video.is_down,
        playlist.title AS playlist
    FROM video
    JOIN playlist ON playlist.pk = video.playlist_pk
    WHERE playlist.id = %(plid)s
    ;
"""

SQL_INSERT_VIDEO = """
    INSERT INTO video (id, title, playlist_pk, added)
    VALUES (%(id)s, %(title)s, %(playlist_pk)s, %(added)s)
    ON CONFLICT (id) DO UPDATE SET
        title = %(title)s
    RETURNING pk, id
    ;
"""

SQL_SELECT_PLAYLISTS_BY_ID = """
    SELECT
        pk,
        id,
        title,
        uploader_id,
        added
    FROM playlist
    WHERE id in %(plids)s
    ;
"""

SQL_INSERT_PLAYLIST = """
    INSERT INTO playlist (id, title, uploader_id, added)
    VALUES (%(id)s, %(title)s, %(uploader_id)s, %(added)s)
    ON CONFLICT (id) DO UPDATE SET
        title = %(title)s,
        uploader_id = %(uploader_id)s
    RETURNING pk
    ;
"""


def select_all_videos():
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_ALL_VIDEOS)
        rows = cur.fetchall()

    data = [video_row_to_dict(row=row) for row in rows]

    return data




def select_videos_by_id(vids):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_VIDEOS_BY_ID, vars={'vids': tuple(vids)})
        rows = cur.fetchall()

    data = [video_row_to_dict(row=row) for row in rows]

    return data




def set_video_as_downloaded(vid):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SET_VIDEO_AS_DOWNLOADED, vars={'id': vid})
        conn.commit()

    result = select_videos_by_id(vids=(vid,))

    return result




def set_video_playlist(vid, plpk):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_SET_VIDEO_PLAYLIST, {'vid': vid, 'plpk': plpk})
        conn.commit()

    result = select_videos_by_id(vids=(vid,))

    return result




def select_videos_by_playlistid(playlistid):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_SELECT_VIDEOS_BY_PLAYLISTID, {'plid': playlistid})
        conn.commit()
        rows = cur.fetchall()

    data = [video_row_to_dict(row=row) for row in rows]

    return data




def insert_video(vdata):
    vdata.setdefault('playlist_pk', None)
    vdata['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_VIDEO, vdata)
        conn.commit()
        row = cur.fetchone()

    result = select_videos_by_id(vids=(row[VIDEO_COLUMN_IDX__id],))

    return result



def select_playlists_by_id(plids):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_PLAYLISTS_BY_ID, vars={'plids': plids})
        rows = cur.fetchall()

    data = [playlist_row_to_dict(row=row) for row in rows]

    return data



def insert_playlist(pldict):
    pldict['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_PLAYLIST, pldict)
        conn.commit()

    result = select_playlists_by_id(plids=(pldict['id'],))

    return result
