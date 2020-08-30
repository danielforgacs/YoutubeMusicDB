import os
import dbfuncs
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


HOST = os.environ['DBACCESS_RPC_HOST']
PORT = int(os.environ['DBACCESS_RPC_PORT'])
ADDRESS = (HOST, PORT)



class Server(SimpleXMLRPCServer):
    def __init__(self, *args, **kwargs):
        super().__init__(addr=ADDRESS)


    def __enter__(self, *args, **kwargs):
        server = super().__enter__(*args, **kwargs)
        print('--> Server started')

        return server


    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        print('--> Server closed.')



def server_test(data):
    response = {'OK': data}

    return response



def main():
    with Server() as server:
        server.register_function(function=server_test)
        server.serve_forever()



if __name__ == '__main__':
    main()
