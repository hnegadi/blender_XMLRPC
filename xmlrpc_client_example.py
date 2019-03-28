import xmlrpclib
import socket


# get server data function
def server_data(host='localhost', port=8000, app='', debug=False):
    if debug:
        print 'Scanning port:', port
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
string_cmd=''
string_cmd+='def str_data(data):'
string_cmd+='\n'
string_cmd+='   return data'
string_cmd+='\n'
string_cmd+='print(str_data('+str(data)+'))'
xmlrpc_command(string_cmd)

