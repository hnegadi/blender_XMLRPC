Blender XML RPC Server
=======
Blender XML RPC Server runs an xml_rpc server in blender.
It runs within a separate thread within blender in order not to breach scene graph evaluation performance.
XML RPC allows to send string commands from outside of blender.
One of its purpose is to allow python2.7 based pipelines to talk to blender sending string commands.
It can be also usefull to have two blender sessions talking to each other.

RELEASE NOTES
----------------
By default it the server will run on first available port as of 8000.
So, given the fact that port 8000 is available on your computer, if you start a new blender session, it will take the next available port as of 8001, etc.
You can find the status of the xml rpc server in the world tab of the Properties panel.
The addon is compatible with both 2.7* and 2.8* versions of blender. Even if it will complain that it's been written with 2.8* it will still properly run in 2.7*

HOW TO
----------------

within a python2.7* enviromnent you should proceed this way:
```python
mport xmlrpclib, socket

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

# get blender data as scene contents
port=8000
data = server_data(port=port)
scene_objects = data['scene_objects']
print scene_objects, type(scene_objects)

# send a string command
string_cmd=''
string_cmd+='print()\n'
string_cmd+='print("Blender data is: '+str(data)+'")\n'
string_cmd+='print("Scene Objects are: '+str(data)+'")\n'
string_cmd+='print()\n'
xmlrpc_command(string_cmd, port=port)
```

within a python3.* environment.
In this example we assume a blender session  talking to another one on localhost.
```python
mport xmlrpclib, socket

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

# get blender data as scene contents
port=8000
data = server_data(port=port)
scene_objects = data['scene_objects']
print scene_objects, type(scene_objects)

# build the string command
string_cmd+='print()\n'
string_cmd+='print("Blender data is: '+str(data)+'")\n'
string_cmd+='print("Scene Objects are: '+str(data)+'")\n'
string_cmd+='print()\n'
# send the string command
xmlrpc_command(string_cmd, port=port)
```

IMPORTANT LINKS:
----------------
https://docs.python.org/3/library/xmlrpc.server.html
https://docs.python.org/3/library/threading.html

