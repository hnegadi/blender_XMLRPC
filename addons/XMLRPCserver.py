import bpy, sys, os, time, socket, threading
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

bl_info = {
    "name": "XMLRPC Server",
    "author": "KristenH",
    "version": (0, 5, 0, 1),
    "blender": (2, 79, 0),
    "category": "System"
}

from bpy.props import (BoolProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)

class SimpleServer(SimpleXMLRPCServer):
    pass

def command(com):
    com = 'import bpy\n'+com
    exec(com)
    return com

def server_data():
    return {
        'hostname':socket.gethostname(),
        'app_version':bpy.app.version_string,
        'file_path':bpy.context.blend_data.filepath.replace('\\', '/'),
        'exe':os.path.basename(bpy.app.binary_path)
        }

def pscan(host='localhost', port=8000):
    # Setting up a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy = (host, port)
    try:
        con = sock.connect(proxy)
        return True
    except:
        pass

# Add a turn on/off button for Blender
class MySettings(PropertyGroup):
    my_bool = BoolProperty(
        name="End is checked",
        description="End Server",
        default = True
    )

class ServerThread(threading.Thread):
    def __init__(self, host='localhost', port=8000):
        self.proxy = (host, port)
        self.server = SimpleServer(self.proxy)
        self.port = port
        self.host = host
        threading.Thread.__init__(self)
        self.server.register_introspection_functions()
        self.server.register_function(command, "command")
        self.server.register_function(server_data, "server_data")

    # We must need this!!
    def run(self):
        try:
            self.server.serve_forever()
            self.server_thread.setDaemon(True)
            # self.server. = mp.Process(target=register)
            # self.server.proc.daemon = True
            # self.server.proc.start()

        except KeyboardInterrupt:
            print("Exiting")
            self.server_thread.setDaemon(False)
            sys.exit()

global server
server = None
global x
x = 8000
while (server is None):
    con = pscan(port=x)
    if con is not None:
        print("Server found on: localhost:", x)
        x += 1
    else:
        server = ServerThread(port=x)
        print("Started the server with:", server.host, ":", server.port)
        server.start()

class ServerOperator(bpy.types.Operator):
    bl_idname = "wm.xmlrpc_server"
    bl_label = "Terminate"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        global server
        global x
        #layout = self.layout
        if (mytool.my_bool == True):
            while (server is not None):
                con = pscan(port=x)
                server = ServerThread(port=x)
                print("Server with", server.host, ":", server.port, "terminated.")
                server.exit()
                x -= 1
        else:
            pass
        return {'FINISHED'}

class ServerMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.select_all", text="Select/Deselect ALL").action = 'TOOGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

class ServerPanel(Panel):
    bl_label = "Server"
    bl_idname = "Object_PT_server"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"
    bl_context = "objectmode"
    #server = ServerThread()

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        # server = run_server()
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_bool")
        layout.operator("wm.xmlrpc_server")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)
    #bpy.utils.register_class(ServerPanel)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool
    #bpy.utils.unregister_class(ServerPanel)

if __name__ == "__main__":
    register()