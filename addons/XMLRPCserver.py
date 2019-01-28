import bpy, sys, os, time, socket, threading
import multiprocessing as mp
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
    return {
        'hostname':socket.gethostname(),
        'app_version':bpy.app.version_string,
        'file_path':bpy.context.blend_data.filepath.replace('\\', '/'),
        'exe':os.path.basename(bpy.app.binary_path)
        }

def pscan(host=HOST, port=PORT):
    # Setting up a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy = (host, port)
    try:
        con = sock.connect(proxy)
        return True
    except:
        pass

class ServerThread(threading.Thread):
    def __init__(self, host=HOST, port=PORT):
        self.proxy = (host, port)
        self.server = SimpleServer(self.proxy)
        self.data = server_data
        self.port = port
        self.host = host
        threading.Thread.__init__(self)
        self.server.register_introspection_functions()
        self.server.register_function(command, "command")
        self.server.register_function(server_data, "server_data")

    def run(self):
        try:
            # self.server.serve_forever()
            # self.server_thread.setDaemon(True)
            global thread
            self.server.proc = mp.Process(target=run_server)
            self.server.proc.daemon = True
            self.server.proc.start()
        except :
            print("Exiting")
            sys.exit()

class ServerPanel(bpy.types.Panel):
    bl_label = "Server Panel"
    bl_idname = "Object_PT_server"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Shortcuts"
    server = ServerThread()

    def draw(self, context):
        layout = self.layout
        hostname = server_data()
        s_port = ServerThread(port=PORT)
        layout.row().label(text="XML RPC Server running on {}: {}".format(hostname, s_port))

# Turns on the addon
def register():
    bpy.utils.register_class(ServerPanel)

# Turns off the addon
def unregister():
    bpy.utils.unregister_class(ServerPanel)

def run_server():
    server = None
    x=8000
    while(server is None):
        con = pscan(port=x)
        if con is not None:
            print("Server found on: localhost:", x)
            x += 1
        else:
            server = ServerThread(port=x)
            # Make sure the first port is the start up port.
            print("Started the server with:", server.host, ":", server.port)
            server.start()
            print()
            # print("... Press Ctrl+C to exit")
            # print('\n'.join(dir(server.server)))
        return server, x

if __name__ == "__main__":
    register()