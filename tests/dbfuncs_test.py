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
