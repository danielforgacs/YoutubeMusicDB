import pytest
import dbaccess.dbfuncs as dbf
import tests.setup



def setup():
    tests.setup.init_test_db()



def test_select_all_videos_empty_db():
    data = dbf.select_all_videos()
    expected = {}

    assert data == {}



def test_select_all_videos_01():
    tests.setup.run_sql_file(sqlfile='testData_01')
    expected = {
        'id1': {
            'id': 'id1',
            'title': 'title1',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
    }

    data = dbf.select_all_videos()

    assert data == expected



def test_select_all_videos_02():
    tests.setup.run_sql_file(sqlfile='testData_02')
    expected = {
        'id1': {
            'id': 'id1',
            'title': 'title1',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
        'id2': {
            'id': 'id2',
            'title': 'title2',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
        'id3': {
            'id': 'id3',
            'title': 'title3',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
    }

    data = dbf.select_all_videos()

    assert data == expected



def test_select_all_videos_03():
    tests.setup.run_sql_file(sqlfile='testData_03')
    expected = {
        'id1': {
            'id': 'id1',
            'title': 'title1',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': True,
            'playlisttitle': None,
        },
        'id2': {
            'id': 'id2',
            'title': 'title2',
            'playlistid': 'plid1',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle1',
        },
        'id3': {
            'id': 'id3',
            'title': 'title3',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
        'id4': {
            'id': 'id4',
            'title': 'title4',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': True,
            'playlisttitle': 'pltitle2',
        },
        'id5': {
            'id': 'id5',
            'title': 'title5',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle2',
        },
    }

    data = dbf.select_all_videos()

    assert data == expected




def test_select_videos_by_id():
    tests.setup.run_sql_file(sqlfile='testData_03')
    expected = {
        'id2': {
            'id': 'id2',
            'title': 'title2',
            'playlistid': 'plid1',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle1',
        },
        'id4': {
            'id': 'id4',
            'title': 'title4',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': True,
            'playlisttitle': 'pltitle2',
        },
        'id5': {
            'id': 'id5',
            'title': 'title5',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle2',
        },
    }

    data = dbf.select_videos_by_id(vids=('id2', 'id4','id5'))

    assert data == expected



def test_set_video_as_downloaded():
    tests.setup.run_sql_file(sqlfile='testData_03')
    expected = {'id5': {
        'id': 'id5',
        'title': 'title5',
        'playlistid': 'plid2',
        'added': '2000-01-01 00:00:00',
        'is_down': True,
        'playlisttitle': 'pltitle2',
    }}
    data = dbf.set_video_as_downloaded(vid='id5')

    assert data == expected




def test_set_video_playlist():
    tests.setup.run_sql_file(sqlfile='testData_03')
    vid = 'id1'
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[vid]['playlistid'] is None
    assert video[vid]['playlisttitle'] is None

    plpk = 1
    result = dbf.set_video_playlist(vid=vid, plpk=plpk)
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[vid]['playlistid'] == 'plid1'
    assert video[vid]['playlisttitle'] == 'pltitle1'

    plpk = 2
    result = dbf.set_video_playlist(vid=vid, plpk=plpk)
    video = dbf.select_videos_by_id(vids=(vid,))

    assert video[vid]['playlistid'] == 'plid2'
    assert video[vid]['playlisttitle'] == 'pltitle2'




@pytest.mark.parametrize('plid, expected', (
    ('plid0', []),
    ('plid1', ['id2']),
    ('plid2', ['id4', 'id5']),
))
def test_query_videos_by_playlistid(plid, expected):
    tests.setup.run_sql_file(sqlfile='testData_03')
    result = dbf.query_videos_by_playlistid(playlistid=plid)
    vids = [video['id'] for video in result.values()]

    assert vids == expected




def test_insert_video():
    video = {
        'id': 'new_vid_id_1',
        'title': 'new_vid_title_1',
    }
    result = dbf.insert_video(vdata=video)

    assert list(result.keys()) == [video['id']]
    assert list(result[video['id']].keys()) == [
        'id', 'title', 'playlistid', 'added', 'is_down', 'playlisttitle']
    assert result[video['id']]['id'] == video['id']
    assert result[video['id']]['title'] == video['title']




@pytest.mark.parametrize('plids', (
    ('plid1',),
    ('plid2',),
    ('plid1', 'plid2'),
))
def test_select_playlists_by_id(plids):
    tests.setup.run_sql_file(sqlfile='testData_03')
    expected = list(plids)
    result = dbf.select_playlists_by_id(plids=plids)

    assert list(result.keys()) == expected
    assert [pl['id'] for pl in result.values()] == expected




@pytest.mark.parametrize('pldict', (
    {
        'id': 'pl_id_1',
        'title': 'pl_title_1',
        'uploader_id': 'pl_uploader_id_1',
    },
    {
        'id': 'pl_id_2',
        'title': 'pl_title_2',
        'uploader_id': 'pl_uploader_id_2',
    },
))
def test_insert_playlist(pldict):
    result = dbf.insert_playlist(pldict=pldict)

    assert len(result.keys()) == 1
    assert list(result.keys()) == [pldict['id']]
    assert list(result[pldict['id']].keys()) == [
        'id', 'title', 'uploader_id', 'added']
    assert result[pldict['id']]['id'] == pldict['id']
    assert result[pldict['id']]['title'] == pldict['title']
    assert result[pldict['id']]['uploader_id'] == pldict['uploader_id']
