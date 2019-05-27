import xmlrpc.client as xmlrpclib
import socket


# get server data function
def server_data(host='localhost', port=8000, app='', debug=False):
    if debug:
        print('Scanning port:', port)
    try:
        proxy = xmlrpclib.ServerProxy(
            'http://'+host+':'+str(port)+'/', allow_none=True)
        data = proxy.server_data()
        if debug:
            print('   ', port, data)
        if app in data['exe']:
            return data
    except(socket.error):
        if debug:
            print('Couldnt connect with the socket-server: %s\n' % port)

def scene_objects(host='localhost', port=8000, app='', debug=False):
    if debug:
        print('Scanning port:', port)
    try:
        proxy = xmlrpclib.ServerProxy(
            'http://'+host+':'+str(port)+'/', allow_none=True)
        return proxy.scene_objects()
    except(socket.error):
        if debug:
            print('Couldnt connect with the socket-server: %s\n' % port)

# get server data function


# send a command to the server
def xmlrpc_command(string_cmd, host='localhost', port=8000, debug=False):
    proxy = xmlrpclib.ServerProxy(
        'http://'+host+':'+str(port)+'/',
        allow_none=True)
    com = proxy.command(string_cmd)
    if debug:
        print(
            'on port',
            port,
            'and host',
            host,
            'Your command is: ' + com
            )
    return com

data = server_data()
scene_objects =scene_objects()
print('Scene Objects are:', *scene_objects, sep='\n')
string_cmd=''
string_cmd+='print("Scene Objects are:", *'+scene_objects+', sep="\n\")\n'
xmlrpc_command(string_cmd)