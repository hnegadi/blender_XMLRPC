import bpy
import socket
import threading
import os
from xmlrpc.server import SimpleXMLRPCServer

# basic infos
bl_info = {
    'name': 'xmlrpc Server',
    'author': 'Kristen Haave | Halim Negadi',
    'version': (0, 5, 0, 2),
    'blender': (2, 80, 0),
    'category': 'System'
}
# where are we running from ?
print(os.path.dirname(os.path.abspath(__file__)))


# scan function to used to check first available port
def port_scan(host='localhost', port=8000, debug=False):
    # Setting up a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy = (host, port)
    try:
        if debug:
            print (proxy)
        sock.connect(proxy)
        return True
    except(socket.error):
        if debug:
            print('Couldnt connect with the socket-server: %s\n' % port)
        return False


# server functions registered in ServerThread class
def command(com):
    com = 'import bpy\n'+com
    exec(com)
    return com

def scene_objects():
    s = ''
    for i in bpy.data.objects.keys():
        s += i
        s += ','
    if s:
        return s[:-1]
    else:
        return s

def server_data():
    return {
        'hostname': socket.gethostname(),
        'app_version': bpy.app.version_string,
        'file_path': bpy.context.blend_data.filepath.replace('\\', '/'),
        'exe': os.path.basename(bpy.app.binary_path),
        'scene_objects': bpy.data.objects.keys(),
        'pid': os.getpid()
        }


# ServerThread class
class ServerThread(threading.Thread):
    def __init__(self, host='localhost', port=8000):
        self._stop_event = threading.Event()
        self.proxy = (host, port)
        self.server = SimpleXMLRPCServer(self.proxy)
        self.server.register_introspection_functions()
        self.server.register_function(command, 'command')
        self.server.register_function(server_data, 'server_data')
        self.server.register_function(scene_objects, 'scene_objects')
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.port = port

    # we make sure to demonize
    # to avoid zombie process
    # remaining after blender exit
    def start(self):
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self.thread.stop()


class ServerPanel(bpy.types.Panel):
    bl_label = 'Server Panel'
    bl_idname = 'Object_PT_server'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = 'Shortcuts'
    bl_context = 'world'

    def draw(self, context):
        layout = self.layout
        layout.row().label(text='XMLRPC Server Running:')
        layout.row().label(text='{}:{}'.format(
            socket.gethostname(), server.port))
        layout.row().label(text='Blender Version: {}'.format(str(bpy.app.version)))


DEBUG = False
server = None
x = 8000
while(server is None):
    is_socket = port_scan(port=x, debug=DEBUG)
    if is_socket:
        if DEBUG:
            print('Server found on: localhost:', x)
        x += 1
    else:
        server = ServerThread(port=x)
        server.start()


# Enable server addon on Blender
def register():
    from bpy.utils import register_class
    register_class(ServerPanel)


# Disable server addon form Blender
def unregister():
    from bpy.utils import unregister_class
    unregister_class(ServerPanel)


if __name__ == '__main__':
    register()
