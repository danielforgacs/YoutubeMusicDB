import os
import psycopg2
import pytest
import tests.setup
import app.data as data
# import app.youtube as youtube



def setup():
    tests.setup.init_test_db()




@pytest.mark.parametrize('pldata', tests.setup.PLAYLIST_DATA)
def test_insert_playlist(pldata):
    plpk = data.insert_playlist(pldict=pldata)

    assert isinstance(plpk, int)

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=pldata)
        result = cur.fetchone()

    assert result[data.IDX_PLAYLIST__pk] == plpk
    assert result[data.IDX_PLAYLIST__id] == pldata['id']
    assert result[data.IDX_PLAYLIST__title] == pldata['title']
    assert result[data.IDX_PLAYLIST__uploader_id] == pldata['uploader_id']



def test_playlist_insert_updates_data_if_playlist_extsts():
    playlist = dict(tests.setup.PLAYLIST_DATA[0])
    newtitle = 'new_title'
    plpk = data.insert_playlist(pldict=playlist)

    playlist['title'] = newtitle
    plpk2 = data.insert_playlist(pldict=playlist)

    assert plpk == plpk2

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query="""
            SELECT pk, id, title, uploader_id
            FROM playlist
            WHERE id = %(id)s
            ;
        """, vars=playlist)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][data.IDX_PLAYLIST__title] == newtitle



@pytest.mark.parametrize('vdata', tests.setup.VIDEO_DATA)
def test_insert_video(vdata):
    vpk = data.insert_video(vdata=vdata)

    assert isinstance(vpk, int)

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT pk, id, title, playlist
            FROM video
            WHERE id = %(id)s
        ;
        """, vars=vdata)
        result = cur.fetchall()

    assert len(result) == 1
    assert result[0][data.IDX_VIDEO__pk] == vpk
    assert result[0][data.IDX_VIDEO__id] == vdata['id']
    assert result[0][data.IDX_VIDEO__title] == vdata['title']
    assert result[0][data.IDX_VIDEO__playlist] == vdata['playlist']




def test_get_video_ids_by_playlist():
    plpk1 = data.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[0]))
    plpk2 = data.insert_playlist(pldict=dict(tests.setup.PLAYLIST_DATA[1]))
    videodata1 = dict(tests.setup.VIDEO_DATA[0])
    videodata2 = dict(tests.setup.VIDEO_DATA[1])
    videodata3 = dict(tests.setup.VIDEO_DATA[2])
    videodata1['playlist'] = plpk1
    videodata2['playlist'] = plpk1
    videodata3['playlist'] = plpk2
    vpk1 = data.insert_video(vdata=videodata1)
    vpk2 = data.insert_video(vdata=videodata2)
    vpk3 = data.insert_video(vdata=videodata3)
    videoids1 = data.query_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[0])['id'])
    videoids2 = data.query_videos_by_playlistid(
        playlistid=dict(tests.setup.PLAYLIST_DATA[1])['id'])

    assert videoids1 == [videodata1['id'], videodata2['id']]
    assert videoids2 == [videodata3['id']]





def test_set_video_playlist_sets_updates():
    sql = """
        SELECT pk, id, title, playlist
        FROM video
        WHERE video.id = %(vid)s
        ;
    """
    videodata = dict(tests.setup.VIDEO_DATA[0])

    plpk1 = data.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[0])
    plpk2 = data.insert_playlist(pldict=tests.setup.PLAYLIST_DATA[1])
    vpk = data.insert_video(vdata=videodata)

    vpk, vid, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk1)

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk1 == plpk
    assert result[data.IDX_VIDEO__pk] == vpk

    vpk, vid, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk2)

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars={'vid': videodata['id']})
        result = cur.fetchone()

    assert result[data.IDX_VIDEO__playlist] == plpk2 == plpk
    assert result[data.IDX_VIDEO__pk] == vpk

    plpk3 = None

    vpk, vid, plpk = data.set_video_playlist(vid=videodata['id'], plpk=plpk3)

    with data.PGConnection() as conn:
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
    video1 = data.insert_video(vdata=videdict)

    sql = """
        SELECT is_down
        FROM video
        WHERE video.id = %(id)s
        ;
    """
    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is False

    vpk = data.set_video_as_downloaded(vid=videdict['id'])

    with data.PGConnection() as conn:
        cur = conn.cursor()
        cur.execute(query=sql, vars=videdict)
        row = cur.fetchone()

    is_downloaded = row[0]

    assert is_downloaded is True



def test_select_all_videos_returns_all_video_rows_once():
    with data.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute("""
            INSERT INTO public.video 
                (id,  title,   playlist, added, is_down) VALUES
                ('a', 'vid01', NULL, '2020-08-18 14:53:22.697986', false),
                ('b', 'vid02', NULL, '2020-08-18 14:53:24.035011', false)
                ('c', 'vid03', NULL, '2020-08-18 14:58:58.980937', false)
            ;
        """)
        conn.commit()

    with data.PGConnection() as conn:
        curs = conn.cursor()
        curs.execute("""
            SELECT count (pk)
            FROM video
            ;
        """)
        rows = curs.fetchone()
        # rows = curs.fetchall()

    rowcount = rows[0]
    allvids = data.select_all_videos()
    print()
    print('::rows:', rows)
    print('::rowcount:', rowcount)
    print(len(allvids))



    assert rowcount == len(allvids)
    # print(allvids)
    # assert 



if __name__ == '__main__':
    pass
