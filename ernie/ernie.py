import logging
import bert
import struct
import threading
import SocketServer


class ErnieTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        ernie_inst = Ernie()
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        ernie_inst.handle_input(self.rfile, self.wfile)


class Ernie(object):
    mods = {}
    logger = None

    @classmethod
    def mod(cls, name):
        if name not in cls.mods:
            cls.mods[name] = Mod(name)
        return cls.mods[name]

    @classmethod
    def logfile(cls, file):
        logging.basicConfig(filename=file, level=logging.DEBUG)
        cls.logger = logging.getLogger('ernie')

    @classmethod
    def log(cls, text):
        if cls.logger != None:
            cls.logger.debug(text)

    def dispatch(self, mod, fun, args):
        if mod not in Ernie.mods:
            raise ServerError("No such module '" + mod + "'")
        if fun not in Ernie.mods[mod].funs:
            raise ServerError("No such function '" + mod + ":" + fun + "'")
        return Ernie.mods[mod].funs[fun](*args)

    def read_4(self, input):
        raw = input.read(4)
        if len(raw) == 0:
            return None
        return struct.unpack('!L', raw)[0]

    def read_berp(self, input):
        packet_size = self.read_4(input)
        if packet_size == None:
            return None
        ber = input.read(packet_size)
        return bert.decode(ber)

    def write_berp(self, output, obj):
        data = bert.encode(obj)
        output.write(struct.pack("!L", len(data)))
        output.write(data)
        output.flush()

    def handle_input(self, input, output):
        ipy = self.read_berp(input)
        if ipy == None:
            print 'Could not read BERP length header.'
            return

        if len(ipy) == 4 and ipy[0] == bert.Atom('call'):
            mod, fun, args = ipy[1:4]
            self.log("-> " + ipy.__str__())
            try:
                res = self.dispatch(mod, fun, args)
                opy = (bert.Atom('reply'), res)
                self.log("<- " + opy.__str__())
                self.write_berp(output, opy)
            except ServerError, e:
                opy = (bert.Atom('error'), (bert.Atom('server'), 0,
                       str(type(e)), str(e), ''))
                self.log("<- " + opy.__str__())
                self.write_berp(output, opy)
            except Exception, e:
                opy = (bert.Atom('error'), (bert.Atom('user'), 0, str(type(e)),
                       str(e), ''))
                self.log("<- " + opy.__str__())
                self.write_berp(output, opy)

        elif len(ipy) == 4 and ipy[0] == bert.Atom('cast'):
            mod, fun, args = ipy[1:4]
            self.log("-> " + ipy.__str__())
            try:
                res = self.dispatch(mod, fun, args)
            except:
                pass
            self.write_berp(output, (bert.Atom('noreply')))
        else:
            self.log("-> " + ipy.__str__())
            opy = (bert.Atom('error'), (bert.Atom('server'), 0,
                   "Invalid request: " + ipy.__str__()))
            self.log("<- " + opy.__str__())
            self.write_berp(output, opy)


class ServerError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Mod:

    def __init__(self, name):
        self.name = name
        self.funs = {}

    def fun(self, name, func):
        self.funs[name] = func


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass


class ThreadedErnie(object):
    def start(self, daemon=False, host='', port=50007, kill_threads=False):
        Ernie.log("Starting")
        server = ThreadedTCPServer((host, port), ErnieTCPHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = daemon
        # Kill all threads or wait for them to finnish on exit, False = wait
        server_thread.daemon_threads = kill_threads
        server_thread.start()
        print "Server running..."
