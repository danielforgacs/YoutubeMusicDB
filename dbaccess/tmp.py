import xmlrpc.client

host = 'localhost'
# host = '0.0.0.0'
port = 5001

url = 'http://{}:{}'.format(host, port)

s = xmlrpc.client.ServerProxy(url)

# Print list of available methods
print(s.system.listMethods())
