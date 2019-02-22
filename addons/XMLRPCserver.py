import bpy, socket, threading, atexit, platform, subprocess, os
from xmlrpc.server import SimpleXMLRPCServer

# basic infos
bl_info = {
    "name": "XMLRPC Server",
    "author": "KristenH",
    "version": (0, 5, 0, 1),
    "blender": (2, 80, 0),
    "category": "System"
}
# where are we running from ?
print(os.path.dirname(os.path.abspath(__file__)))


# function to try to kill zombies upon blender exit
def kill_process(pid):
    if not(pid):
        return
    pid = str(pid)
    current_os = platform.system()
    if current_os == 'Windows':
        cmd = ['taskkill', '/PID', pid]
        # cmd = 'T:/apptools/bin/pskill.exe ' + pid
        os.system(cmd)
    else:
        cmd = ['kill -9', '-ef', pid]
        output = subprocess.check_output(cmd)
        if self.debug:
            print(output)


# this is what we try to register to catch blender exit event but it's not being triggered
def goodbye(server):
    print('goodbye')
    server.stop()
    kill_process(server._get_my_tid())
    # kill_process(os.pid())


# scan function to used to check first available port
def pscan(host='localhost', port=8000):
    # Setting up a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy = (host, port)
    try:
        con = sock.connect(proxy)
        return True
    except:
        pass


# server functions registered in ServerThread class
def command(com):
    com = 'import bpy\n'+com
    exec(com)
    return com

def server_data():
    return {
        'hostname':socket.gethostname(),
        'app_version':bpy.app.version_string,
        'file_path':bpy.context.blend_data.filepath.replace('\\', '/'),
        'exe':os.path.basename(bpy.app.binary_path),
        'scene_objects':bpy.data.objects.keys(),
        'pid':os.getpid()
        }

# this is needed in ServerThread class
def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# Server classes
class SimpleServer(SimpleXMLRPCServer):
    pass

class ServerThread(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.'''
    def __init__(self, host='localhost', port=8000):
        super(ServerThread, self).__init__()
        self._stop_event = threading.Event()
        self.proxy = (host, port)
        self.server = SimpleServer(self.proxy)
        self.port = port
        self.host = host
        threading.Thread.__init__(self)
        self.server.register_introspection_functions()
        self.server.register_function(command, "command")
        self.server.register_function(server_data, "server_data")
    
    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        _async_raise( self._get_my_tid(), exctype )


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()        

    # We no longer use this one at server_forever breaches blender's performance
    def run(self):
        try:
            self.server.serve_forever()
            self.server_thread.setDaemon(True)
            # self.server. = mp.Process(target=register)
            # self.server.proc.daemon = True
            # self.server.proc.start()

        except Exception:
            print("Exiting")
            leaveBlender()


class ServerPanel(bpy.types.Panel):
    bl_label = "Server Panel"
    bl_idname = "Object_PT_server"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Shortcuts"
    #server = ServerThread()

    def draw(self, context):
        # server = run_server()
        layout = self.layout
        layout.row().label(text="Server running on: {}:{}".format(server.host, server.port))


server = None
x=8000
while(server is None):
    con = pscan(port=x)
    if con is not None:
        print("Server found on: localhost:", x)
        x += 1
    else:
        server = ServerThread(port=x)
        server.start()
        print("Started the server with:", server.host, ":", server.port, 'thread_id' ,server._get_my_tid())
        atexit.register(goodbye,server)
        print(dir(atexit))



# Enable server addon on Blender
def register():
    from bpy.utils import register_class
    register_class(ServerPanel)

# Disable server addon form Blender
def unregister():
    print("Started the server with:", server.host, ":", server.port, 'thread_id' ,server._get_my_tid())
    from bpy.utils import unregister_class
    unregister_class(ServerPanel)

        
if __name__ == "__main__":
    register()