import os
import psycopg2
import datetime


PLAYLIST_PK_IDX = 0
PLAYLIST_ID_IDX = 1
PLAYLIST_TITLE_IDX = 2
PLAYLIST_UPLOADER_ID_IDX = 3
PLAYLIST_ADDED_IDX = 4


VIDEO_ROW_IDX__pk = 0
VIDEO_ROW_IDX__id = 1
VIDEO_ROW_IDX__title = 2
VIDEO_ROW_IDX__added = 3
VIDEO_ROW_IDX__is_down = 4
VIDEO_ROW_IDX__playlistid = 5



SQL_SELECT_ALL_VIDEOS = """
    SELECT
        video.pk,
        video.id,
        video.title,
        video.added,
        video.is_down,
        playlist.id,
        playlist.title
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlistpk
    ORDER BY video.pk
"""

SQL_SELECT_VIDEOS_BY_ID = """
    SELECT
        video.pk,
        video.id,
        video.title,
        video.added,
        video.is_down,
        playlist.id,
        playlist.title
    FROM video
    LEFT JOIN playlist ON playlist.pk = video.playlistpk
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
    SET playlistpk = %(plpk)s
    WHERE video.id = %(vid)s
    RETURNING pk, id, title, playlistpk
    ;
"""

SQL_SELECT_VIDEOS_BY_PLAYLISTID = """
    SELECT
        video.pk,
        video.id,
        video.title,
        video.added,
        video.is_down,
        playlist.id,
        playlist.title
    FROM video
    JOIN playlist ON playlist.pk = video.playlistpk
    WHERE playlist.id = %(plid)s
    ORDER BY video.pk
    ;
"""

SQL_INSERT_VIDEO = """
    INSERT INTO video (id, title, playlistpk, added)
    VALUES (%(id)s, %(title)s, %(playlistpk)s, %(added)s)
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
    ORDER BY playlist.pk
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
        'pk': row[VIDEO_ROW_IDX__pk],
        'id': row[VIDEO_ROW_IDX__id],
        'title': row[VIDEO_ROW_IDX__title],
        'added': str(row[VIDEO_ROW_IDX__added]),
        'is_down': row[VIDEO_ROW_IDX__is_down],
        'playlistid': row[VIDEO_ROW_IDX__playlistid],
        'playlisttitle': row[playlisttitle_idx] or None,
    }
    return row



def playlist_row_to_dict(row):
    rowdict = {
        'pk': row[PLAYLIST_PK_IDX],
        'id': row[PLAYLIST_ID_IDX],
        'title': row[PLAYLIST_TITLE_IDX],
        'uploader_id': row[PLAYLIST_UPLOADER_ID_IDX],
        'added': row[PLAYLIST_ADDED_IDX],
    }
    return rowdict




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

    data = {
        row[VIDEO_ROW_IDX__id]: video_row_to_dict(row=row)
        for row in rows
    }

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

    data = {
        row[VIDEO_ROW_IDX__id]: video_row_to_dict(row=row)
        for row in rows
    }

    return data




def insert_video(vdata):
    vdata.setdefault('playlistpk', None)
    vdata['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_VIDEO, vdata)
        conn.commit()
        row = cur.fetchone()

    result = select_videos_by_id(vids=(row[VIDEO_ROW_IDX__id],))

    return result



def select_playlists_by_id(plids):
    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=SQL_SELECT_PLAYLISTS_BY_ID, vars={'plids': plids})
        rows = cur.fetchall()

    result = {
        row[PLAYLIST_ID_IDX]: playlist_row_to_dict(row=row)
        for row in rows
    }

    return result



def insert_playlist(pldict):
    pldict['added'] = datetime.datetime.now()

    with PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(SQL_INSERT_PLAYLIST, pldict)
        conn.commit()

    result = select_playlists_by_id(plids=(pldict['id'],))

    return result
