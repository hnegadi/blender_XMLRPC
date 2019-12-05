Blender XML RPC Server
=======
Blender XML RPC Server runs an xml_rpc server in blender.
It runs within a separate thread within blender in order not to breach scene graph evaluation performance.
XML RPC allows to send string commands from outside of blender.
One of its purpose is to allow python2.7 based pipelines to talk to blender sending string commands.

RELEASE NOTES:
----------------
By default it the server will run on first available port as of 8000.
So, given the fact that port 8000 is available on your computer, if you start a new blender session, it will take the next available port as of 8001, etc.
You can find the status of the xml rpc server in the world tab of the Properties panel.
The addon is compatible with both 2.7* and 2.8* versions of blender. Even if it will complain that it's been written with 2.8* it will still properly run in 2.7*

HOW TO:
----------------

within a python2.7 enviromnent you should proceed this way:

```python
import xmlrpclib, os, socket, sys

def xmlrpc_command(string_cmd, port=8000):
    # try except in case of remaining zombie processes
    try:
        host = socket.gethostname()
        proxy = xmlrpclib.ServerProxy("http://localhost:"+str(port)+"/", allow_none=True)
        print "on port",port,"and host", host, "Your command is: " + proxy.command(string_cmd)
        return True
    except:
        return

string_cmd = ''
string_cmd += 'running from\n' + sys.version + '\n'
string_cmd += 'print("HELLO")\n'
xmlrpc_command(, port=8000)
```

IMPORTANT LINKS:
----------------
https://docs.python.org/3/library/xmlrpc.server.html
https://docs.python.org/3/library/threading.html

