import os
import pytest
import xmlrpc.client
import tests.setup




def setup():
    tests.setup.init_test_db()


def test_server_is_working():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=tests.setup.DB_ACCESS_URL)
    data = 1
    response = dbacces_svr.server_test(data)
    expected = {'OK': data}

    assert response == expected



def test_select_all_videos_01():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=tests.setup.DB_ACCESS_URL)
    videos = dbacces_svr.select_all_videos()
    expected = {}

    assert videos == {}



def test_select_all_videos_02():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=tests.setup.DB_ACCESS_URL)
    videos = dbacces_svr.select_all_videos()
    expected = {}

    assert videos == {}

    tests.setup.run_sql_file(sqlfile='testData_03')

    videos = dbacces_svr.select_all_videos()
    expected = {
        'id1': {
            'pk': 1,
            'id': 'id1',
            'title': 'title1',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': True,
            'playlisttitle': None,
        },
        'id2': {
            'pk': 2,
            'id': 'id2',
            'title': 'title2',
            'playlistid': 'plid1',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle1',
        },
        'id3': {
            'pk': 3,
            'id': 'id3',
            'title': 'title3',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
        'id4': {
            'pk': 4,
            'id': 'id4',
            'title': 'title4',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': True,
            'playlisttitle': 'pltitle2',
        },
        'id5': {
            'pk': 5,
            'id': 'id5',
            'title': 'title5',
            'playlistid': 'plid2',
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': 'pltitle2',
        },
    }

    assert videos == expected
