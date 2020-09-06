import os
import psycopg2
import datetime


PLAYLIST_pk = 'pk'
PLAYLIST_id = 'id'
PLAYLIST_title = 'title'
PLAYLIST_uploader_id = 'uploader_id'
PLAYLIST_added = 'added'

VIDEO_pk = 'pk'
VIDEO_id = 'id'
VIDEO_title = 'title'
VIDEO_playlist_id = 'playlistid'
VIDEO_added = 'added'
VIDEO_is_down = 'is_down'
VIDEO_playlist_title = 'playlisttitle'
VIDEO_playlist_data = 'playlist_data'

PLAYLIST_COL_NAMES = [
    PLAYLIST_pk,
    PLAYLIST_id,
    PLAYLIST_title,
    PLAYLIST_uploader_id,
    PLAYLIST_added,
]

VIDEO_COL_NAMES = [
    VIDEO_pk,
    VIDEO_id,
    VIDEO_title,
    VIDEO_playlist_id,
    VIDEO_added,
    VIDEO_is_down,
    VIDEO_playlist_title,
    VIDEO_playlist_data,
]

PLAYLIST_COLS = dict(reversed(nameidx) for nameidx in enumerate(PLAYLIST_COL_NAMES))
VIDEO_COLS = dict(reversed(nameidx) for nameidx in enumerate(VIDEO_COL_NAMES))




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
    playlist_data = row[VIDEO_COLS[VIDEO_playlist_data]]
    playlists = []

    if playlist_data:
        playlists = map(lambda x: x + [None, None], playlist_data)
        playlists = map(playlist_row_to_dict, playlists)

    for playlist in playlists:
        playlist[PLAYLIST_pk] = int(playlist[PLAYLIST_pk])

    videorow = list(row)
    videorow[VIDEO_COLS[VIDEO_playlist_data]] = list(playlists)
    videorow[VIDEO_COLS[VIDEO_added]] = str(videorow[VIDEO_COLS[VIDEO_added]])

    videodict = dict(zip(VIDEO_COL_NAMES, videorow))

    return videodict



def playlist_row_to_dict(row):
    rowdict = {
        PLAYLIST_pk: row[PLAYLIST_COLS[PLAYLIST_pk]],
        PLAYLIST_id: row[PLAYLIST_COLS[PLAYLIST_id]],
        PLAYLIST_title: row[PLAYLIST_COLS[PLAYLIST_title]],
        PLAYLIST_uploader_id: row[PLAYLIST_COLS[PLAYLIST_uploader_id]],
        PLAYLIST_added: row[PLAYLIST_COLS[PLAYLIST_added]],
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
        playlist.title AS playlist,
        (
            SELECT array_agg ( array [ playlist.pk::text, playlist.id, playlist.title ])
            FROM playlist
            JOIN playlist_video ON playlist_video.playlist_pk = playlist.pk
            WHERE video.pk = playlist_video.video_pk
        ) AS playlist_data
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

    result = select_videos_by_id(vids=(row[VIDEO_COLS[VIDEO_id]],))

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
