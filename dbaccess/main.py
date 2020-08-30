import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


HOST = os.environ['DBACCESS_RPC_HOST']
PORT = os.environ['DBACCESS_RPC_PORT']
ADDRESS = (HOST, int(PORT))



class MyFuncs:
    def mul(self, x, y):
        return x * y


def adder_function(x, y):
    return x + y



with SimpleXMLRPCServer(addr=ADDRESS) as server:
    server.register_introspection_functions()
    server.register_function(pow)
    server.register_function(adder_function, 'add')


    server.register_instance(MyFuncs())

    print('--> serving...')
    server.serve_forever()
