import os
import xmlrpc.client
import test.setup



def test_server_is_working():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=test.setup.DB_ACCESS_URL)
    data = 1
    response = dbacces_svr.server_test(data)
    expected = {'OK': data}

    assert response == expected



def test_select_all_videos_01():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=test.setup.DB_ACCESS_URL)
    videos = dbacces_svr.select_all_videos()
    expected = {}

    assert videos == {}
