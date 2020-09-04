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
    expected = []

    assert videos == expected



def test_select_all_videos_02():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=tests.setup.DB_ACCESS_URL)
    videos = dbacces_svr.select_all_videos()
    expected = []

    assert videos == expected

    tests.setup.run_sql_file(sqlfile='testData')

    videos = dbacces_svr.select_all_videos()
    expected = [
        {
            'pk': index,
            'id': 'id{}'.format(index),
            'title': 'title{}'.format(index),
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        } for index in range(1, 11)
    ]
    expected[1]['playlistid'] = 'plid1'
    expected[1]['playlisttitle'] = 'pltitle1'
    expected[3]['playlistid'] = 'plid2'
    expected[3]['playlisttitle'] = 'pltitle2'
    expected[4]['playlistid'] = 'plid2'
    expected[4]['playlisttitle'] = 'pltitle2'

    assert videos == expected
