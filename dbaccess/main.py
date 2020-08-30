import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


HOST = os.environ['DBACCESS_RPC_HOST']
PORT = os.environ['DBACCESS_RPC_PORT']
ADDRESS = (HOST, int(PORT))



class Server(SimpleXMLRPCServer):
    def __init__(self, *args, **kwargs):
        super().__init__(addr=ADDRESS)


    def __enter__(self, *args, **kwargs):
        return super().__enter__(*args, **kwargs)



def main():
    with Server() as server:
        server.register_introspection_functions()

        print('--> serving...')
        server.serve_forever()



if __name__ == '__main__':
    main()
