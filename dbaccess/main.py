import os
import dbaccess.dbfuncs
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


HOST = os.environ['DBACCESS_RPC_HOST']
PORT = int(os.environ['DBACCESS_RPC_PORT'])
ADDRESS = (HOST, PORT)



class Server(SimpleXMLRPCServer):
    def __init__(self, *args, **kwargs):
        super().__init__(addr=ADDRESS, allow_none=True)


    def __enter__(self, *args, **kwargs):
        server = super().__enter__(*args, **kwargs)
        print('--> DBAccess RPC Server started...')

        return server


    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        print('--> DBAccess RPC Server close.')



def server_test(data):
    response = {'OK': data}

    return response



def main():
    with Server() as server:
        server.register_function(function=server_test)
        server.register_function(function=dbaccess.dbfuncs.select_all_videos)
        server.register_function(function=dbaccess.dbfuncs.set_video_playlist)
        server.register_function(function=dbaccess.dbfuncs.insert_video)
        server.serve_forever()



if __name__ == '__main__':
    main()
