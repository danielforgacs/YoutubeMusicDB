import os
import psycopg2
import pytest
import tests.setup
import dbaccess.dbfuncs as dbf
# import app.data as data



def setup():
    tests.setup.init_test_db()




@pytest.mark.parametrize('pldata', tests.setup.PLAYLIST_DATA)
def test_insert_playlist(pldata):
    newplist = dbf.insert_playlist(pldict=pldata)
    plpk = [pldict for pldict in newplist.values()][0]

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=pldata)
        result = cur.fetchone()

    assert result[dbf.PLAYLIST_PK_IDX] == plpk['pk']
    assert result[dbf.PLAYLIST_ID_IDX] == pldata['id']
    assert result[dbf.PLAYLIST_TITLE_IDX] == pldata['title']
    assert result[dbf.PLAYLIST_UPLOADER_ID_IDX] == pldata['uploader_id']



def test_playlist_insert_updates_data_if_playlist_extsts():
    playlist = dict(tests.setup.PLAYLIST_DATA[0])
    newtitle = 'new_title'
    result = dbf.insert_playlist(pldict=playlist)
    plpk = [playlist for playlist in result.values()][0]['pk']

    playlist['title'] = newtitle
    result2 = dbf.insert_playlist(pldict=playlist)
    plpk2 = [playlist for playlist in result2.values()][0]['pk']

    assert plpk == plpk2

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=playlist)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][dbf.PLAYLIST_TITLE_IDX] == newtitle



@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_insert_video(vdata):
    result = dbf.insert_video(vdata=vdata)
    vpk = [video for video in result.values()][0]

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT pk, id, title, playlist
            FROM video
            WHERE id = %(id)s
        ;
        """, vars=vdata)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][dbf.VIDEO_PK_IDX] == vpk['pk']
    assert result[0][dbf.VIDEO_ID_IDX] == vdata['id']
    assert result[0][dbf.VIDEO_TITLE_IDX] == vdata['title']
    assert result[0][dbf.VIDEO_PLAYLIST_IDX] == vdata['playlist']




def test_get_video_ids_by_playlist():
    result1 = dbf.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[0]))
    plpk1 = [playlist for playlist in result1.values()][0]
    result2 = dbf.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[1]))
    plpk2 = [playlist for playlist in result2.values()][0]
    videodata1 = dict(tests.setup.VIDEO_DATA[0])
    videodata2 = dict(tests.setup.VIDEO_DATA[1])
    videodata3 = dict(tests.setup.VIDEO_DATA[2])
    videodata1['playlist'] = plpk1['pk']
    videodata2['playlist'] = plpk1['pk']
    videodata3['playlist'] = plpk2['pk']
    vpk1 = dbf.insert_video(vdata=videodata1)
    vpk2 = dbf.insert_video(vdata=videodata2)
    vpk3 = dbf.insert_video(vdata=videodata3)
    videoids1_raw = dbf.select_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[0])['id'])
    videoids1 = [video for video in videoids1_raw.values()]
    videoids2_raw = dbf.select_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[1])['id'])
    videoids2 = [video for video in videoids2_raw.values()]

    assert [vid['id'] for vid in videoids1] == [videodata1['id'], videodata2['id']]
    assert [vid['id'] for vid in videoids2] == [videodata3['id']]





def test_set_video_playlist_sets_updates():
    sql = """
        SELECT pk, id, title, playlist
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    videodata = dict(tests.setup.VIDEO_DATA[0])

    plpk1 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[0])
    plpk2 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[1])
    vpk = dbf.insert_video(vdata=videodata)

    result = data.set_video_playlist(vid=videodata['id'], plpk=plpk1['pk'])
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlist']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk1['pk'] == plpk
    assert result[data.IDX_VIDEO__pk] == vpk

    result = data.set_video_playlist(vid=videodata['id'], plpk=plpk2['pk'])
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlist']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk2['pk'] == plpk
    assert result[data.IDX_VIDEO__pk] == vpk

    plpk3 = None

    result = data.set_video_playlist(vid=videodata['id'], plpk=plpk3)
    vpk = result['pk']
    vid = result['id']
    plpk = result['playlist']

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk3 == plpk
    assert result[data.IDX_VIDEO__pk] == vpk



def test_set_video_as_downloaded():
    videdict = {
        'id': 'id_test',
        'title': 'title_test',
    }
    video1 = dbf.insert_video(vdata=videdict)

    sql = """
        SELECT is_down
        FROM video
        WHERE video.id = %(id)s
        ;
    """
    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is False

    vpk = data.set_video_as_downloaded(vid=videdict['id'])

    assert isinstance(vpk, dict)

    with dbf.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is True



@pytest.mark.parametrize('sql', [
    """
    INSERT INTO public.video (id,  title,   playlist, added, is_down)
    VALUES ('a', 'vid01', NULL, '2020-08-18 14:53:22.697986', false);
    """,
    """
    INSERT INTO public.video (id,  title,   playlist, added, is_down) VALUES
    ('a', 'vid01', NULL, '2020-08-18 14:53:22.697986', false),
    ('b', 'vid02', NULL, '2020-08-18 14:53:24.035011', false),
    ('c', 'vid03', NULL, '2020-08-18 14:58:58.980937', false);
    """,
])
def test_select_all_videos_returns_all_video_rows_once(sql):
    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

        curs.execute("""
            SELECT count (pk)
            FROM video;
        """)
        rows = curs.fetchone()

    rowcount = rows[0]
    allvids = data.select_all_videos()

    assert rowcount == len(allvids)





@pytest.mark.parametrize('vids, count', (
    [('id_aa',), 1],
    [('id_aa', 'id_aa', 'id_aa',), 1],
    [('id_aa', 'id_cc', 'id_dd'), 3],
    [('id_aa', '--id_cc', '--id_dd'), 1],
    [('--id_aa', '--id_cc', '--id_dd'), 0],
))
def test_select_videos_by_id_retursn_videos_by_video_id_list(vids, count):
    sql = """
        INSERT INTO public.video (id,  title,   playlist, added, is_down) VALUES
            ('id_aa', 'title_aa', NULL, '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', NULL, '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', NULL, '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', NULL, '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', NULL, '2020-01-01 12:12:12.12', false)
    """

    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

    videos = data.select_videos_by_id(vids=vids)

    assert len(videos) == count




@pytest.mark.parametrize('vids', (
    ('id_aa',),
    ('id_aa', 'id_aa', 'id_aa',),
    ('id_aa', 'id_cc', 'id_dd'),
    ('id_aa', '--id_cc', '--id_dd'),
))
def test_select_videos_by_id_retursn_returns_same_columns_as_all_videos(vids):
    sql = """
        INSERT INTO public.video (id,  title,   playlist, added, is_down) VALUES
            ('id_aa', 'title_aa', NULL, '2020-01-01 12:12:12.12', false),
            ('id_bb', 'title_bb', NULL, '2020-01-01 12:12:12.12', false),
            ('id_cc', 'title_cc', NULL, '2020-01-01 12:12:12.12', false),
            ('id_dd', 'title_dd', NULL, '2020-01-01 12:12:12.12', false),
            ('id_ff', 'title_ff', NULL, '2020-01-01 12:12:12.12', false)
    """

    with dbf.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()

    videos = data.select_videos_by_id(vids=vids)
    allvideos = data.select_all_videos()

    assert len(list(videos.values())[0]) == len(list(allvideos.values())[0])





@pytest.mark.parametrize('pldata', tests.setup.PLAYLIST_DATA)
def test_insert_playlist_returns_dict(pldata):
    result = dbf.insert_playlist(pldict=pldata)

    assert isinstance(result, dict)
    assert list(result.keys()) == ['pk']
    assert isinstance(result['pk'], int)




@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_insert_video_returns_dict(vdata):
    result = dbf.insert_video(vdata=vdata)

    assert isinstance(result, dict)
    assert list(result.keys()) == ['pk']
    assert isinstance(result['pk'], int)



def test_set_video_playlist_returns_dict():
    sql = """
        SELECT pk, id, title, playlist
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    videodata = dict(tests.setup.VIDEO_DATA[0])

    plpk1 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[0])
    plpk2 = dbf.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[1])
    vpk = dbf.insert_video(vdata=videodata)

    result = data.set_video_playlist(vid=videodata['id'], plpk=plpk1['pk'])

    assert isinstance(result, dict)




@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_select_all_videos_returns_dict_of_dicts(vdata):
    vpk = dbf.insert_video(vdata=vdata)
    vpk = dbf.insert_video(vdata=tests.setup.VIDEO_DATA[0])
    result = data.select_all_videos()

    assert isinstance(result, dict)
    assert all(map(lambda x: isinstance(x, dict), result.values()))
