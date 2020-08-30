import os
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



dbacces_svr = xmlrpc.client.ServerProxy(uri=tests.setup.DB_ACCESS_URL)
videos = dbacces_svr.select_all_videos()
