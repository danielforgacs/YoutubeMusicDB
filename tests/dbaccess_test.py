import os
import xmlrpc.client


HOST = os.environ['DBACCESS_RPC_HOST']
PORT = int(os.environ['DBACCESS_RPC_PORT'])
DB_ACCESS_URL = 'http://{host}:{port}'.format(host=HOST, port=PORT)



def test_server_is_working():
    dbacces_svr = xmlrpc.client.ServerProxy(uri=DB_ACCESS_URL)
    data = 1
    response = dbacces_svr.server_test(data)
    expected = {'OK': data}

    assert response == expected
