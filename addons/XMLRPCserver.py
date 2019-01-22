import socket
import sys
import bpy
import time
import threading
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
bl_info = {
    "name": "XMLRPC Server",
    "author": "KristenH",
    "version": (0, 5, 0, 1),
    "blender": (2, 79, 0),
    "category": "System"
}

HOST = 'localhost'
PORT = 8000

class SimpleServer(SimpleXMLRPCServer):
    pass

def command(com):
    com = 'import bpy\n'+com
    exec(com)
    return com

def server_data():
    return bpy.app.version_string, bpy.context.blend_data.filepath, socket.gethostname()

class ServerPanel(bpy.types.Panel):
    bl_label = "Server Panel"
    bl_idname = "Object_PT_server"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Shortcuts"
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    def draw(self, context):
        layout = self.layout
        version_string, filepath, hostname = self.proxy.server_data()
        print('found server on', 'localhost:', hostname)
        layout.row().label(text="Server found on: {}:{}".format(hostname,PORT))
        layout.row().label(text="Press Ctrl-C in terminal to exit".format(hostname,PORT))        

def register():
    global thread
    thread = threading.Thread(target=maybe_launch_server)
    thread.daemon = False
    thread.start()
    bpy.utils.register_class(ServerPanel)

def unregister():
    bpy.utils.unregister_class(ServerPanel)

def maybe_launch_server():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    try:
        result = proxy.server_data()
    except ConnectionRefusedError:
        server = SimpleServer((HOST, PORT))
        server.register_introspection_functions()
        server.register_function(command, "command")
        server.register_function(server_data, "server_data")
        version_string = bpy.app.version_string
        print("Started the server with:", HOST, ":", PORT)
        server.serve_forever()


if __name__ == "__main__":
    register()