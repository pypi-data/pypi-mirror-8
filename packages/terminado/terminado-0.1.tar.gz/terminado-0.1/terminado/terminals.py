#!/usr/bin/env python

""" pyxshell.py: pseudo-tty shell wrapper for terminals

Derived from the public-domain Ajaxterm code, v0.11 (2008-11-13).
  https://github.com/antonylesuisse/qweb
  http://antony.lesuisse.org/software/ajaxterm/
and susequently modified for GraphTerm as lineterm.py, v0.57.0 (2014-07-18)
  https://github.com/mitotic/graphterm

The contents of this file remain in the public-domain.

To test, run:

  ./pyxshell.py

Type exactly two Control-D's to exit the shell

"""

from __future__ import absolute_import, print_function, with_statement


import sys
if sys.version_info[0] < 3:
    byte_code = ord
else:
    byte_code = lambda x: x
    unicode = str

import codecs
import errno
import fcntl
import itertools
import logging
import os
import pty
import signal
import struct
import subprocess
import time
import termios
import tty

import random
try:
    random = random.SystemRandom()
except NotImplementedError:
    import random


ENV_PREFIX = "PYXTERM_"         # Environment variable prefix
NO_COPY_ENV = set([])         # Do not copy these environment variables

DEFAULT_TERM_TYPE = "xterm"

IDLE_TIMEOUT = 300            # Idle timeout in seconds
UPDATE_INTERVAL = 0.05        # Fullscreen update time interval
CHUNK_BYTES = 4096            # Chunk size for receiving data in stdin

# Helper functions
def make_term_cookie():
    return "%016d" % random.randrange(10**15, 10**16)

def set_tty_speed(fd, baudrate=termios.B230400):
    tem_settings = termios.tcgetattr(fd)
    tem_settings[4:6] = (baudrate, baudrate)
    termios.tcsetattr(fd, termios.TCSADRAIN, tem_settings)

def set_tty_echo(fd, enabled):
    tem_settings = termios.tcgetattr(fd)
    if enabled:
        tem_settings[3] |= termios.ECHO
    else:
        tem_settings[3] &= ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, tem_settings)

def match_program_name(name):
    """ Return full path to command name, if running. else null string"""
    std_out = subprocess.check_output(["ps", "aux"], timeout=1, universal_newlines=True)
    for line in std_out.split('\n'):
        comps = line.split(None, 10)
        if not comps or not comps[-1].strip():
            continue
        cmd_comps = comps[-1].split()
        if cmd_comps[0].endswith("/"+name):
            return cmd_comps[0]
    return ""

def _exec_new_terminal(cmd, env, working_dir="~"):
    """This is run in the child process after forking.
    
    It ends by calling :func:`os.execvpe` to launch the desired process.
    """
    try:
        os.chdir(working_dir)
    except Exception:
        os.chdir(os.path.expanduser("~"))

    # Close all open fd (except stdin, stdout, stderr)
    os.closerange(3, subprocess.MAXFD)

    # Exec shell
    os.execvpe(cmd[0], cmd, env)

class WithEvents(object):
    event_names = []
    def __init__(self):
        self._event_callbacks = {name:set() for name in self.event_names}

    def register(self, event, callback):
        self._event_callbacks[event].add(callback)

    def register_multi(self, events_callbacks):
        for event, callback in events_callbacks:
            self.register(event, callback)

    def unregister(self, event, callback):
        self._event_callbacks[event].discard(callback)

    def unregister_multi(self, events_callbacks):
        for event, callback in events_callbacks:
            self.unregister(event, callback)

    def unregister_all(self, event):
        self._event_callbacks[event].clear()

    def trigger(self, event, *args):
        err = None
        for callback in self._event_callbacks[event]:
            try:
                callback(*args)
            except Exception as e:
                err = e

        if err is not None:
            raise err

class Terminal(WithEvents):
    event_names = ['read', 'died']

    def __init__(self, fd, pid, height=25, width=80, winheight=0, winwidth=0,
                 cookie=0, access_code="", encoding='utf-8'):
        super(Terminal, self).__init__()
        self.fd = fd
        self.pid = pid
        self.width = width
        self.height = height
        self.winwidth = winwidth
        self.winheight = winheight
        self.cookie = cookie
        self.access_code = access_code
        self.term_encoding = encoding
        self._decoder = codecs.getincrementaldecoder(encoding)(errors='replace')

        self.current_dir = ""
        self.update_buf = ""

        self.rpc_set_size(height, width, winheight, winwidth)

        self.output_time = time.time()
    
    @classmethod
    def spawn(cls, shell_command, env, working_dir="~", **kwargs):
        pid, fd = pty.fork()
        if pid == 0:
            _exec_new_terminal(shell_command, env, working_dir)
            # This will never return, because the process will turn into
            # whatever shell_command specifies.
        else:
            return cls(fd, pid, **kwargs)

    def resize_buffer(self, height, width, winheight=0, winwidth=0, force=False):
        reset_flag = force or (self.width != width or self.height != height)
        self.winwidth = winwidth
        self.winheight = winheight
        if reset_flag:
            self.width = width
            self.height = height

    def rpc_set_size(self, height, width, winheight=0, winwidth=0):
        # python bug http://python.org/sf/1112949 on amd64
        self.resize_buffer(height, width, winheight=winheight, winwidth=winwidth)
        # Hack for buggy TIOCSWINSZ handling: treat large unsigned positive int32 values as negative (same bits)
        winsz = termios.TIOCSWINSZ if termios.TIOCSWINSZ < 0 else struct.unpack('i',struct.pack('I',termios.TIOCSWINSZ))[0]
        fcntl.ioctl(self.fd, winsz, struct.pack("HHHH",height,width,0,0))

    def remote_call(self, method, *args, **kwargs):
        bound_method = getattr(self, "rpc_"+method, None)
        if not bound_method:
            raise Exception("Invalid remote method "+method)
        logging.info("Remote term call %s", method)
        return bound_method(*args, **kwargs)

    def pty_write(self, data):
        assert isinstance(data, unicode), "Must write unicode data"
        raw_data = data.encode(self.term_encoding)
        nbytes = len(raw_data)
        offset = 0
        while offset < nbytes:
            # Need to break data up into chunks; otherwise it hangs the pty
            count = min(CHUNK_BYTES, nbytes-offset)
            retry = 50
            while count > 0:
                try:
                    sent = os.write(self.fd, raw_data[offset:offset+count])
                    if not sent:
                        raise Exception("Failed to write to terminal")
                    offset += sent
                    count -= sent
                except OSError as excp:
                    if excp.errno != errno.EAGAIN:
                        raise excp
                    retry -= 1
                    if retry > 0:
                        time.sleep(0.01)
                    else:
                        raise excp

    def read_ready(self, fd, events):
        assert fd == self.fd
        data = os.read(self.fd, 65536)
        text = self._decoder.decode(data, final=False)
        self.trigger('read', text)

    def kill(self):
        try:
            os.close(self.fd)
            os.kill(self.pid, signal.SIGTERM)
        except (IOError, OSError):
            pass

        self.trigger('died')

class TermManagerBase(object):
    def __init__(self, shell_command, server_url="", term_settings={},
                 ioloop=None):
        self.shell_command = shell_command
        self.server_url = server_url
        self.term_settings = term_settings

        if ioloop is not None:
            self.ioloop = ioloop
        else:
            import tornado.ioloop
            self.ioloop = tornado.ioloop.IOLoop.instance()
        
    def make_term_env(self, height=25, width=80, winheight=0, winwidth=0, **kwargs):
        env = os.environ.copy()
        env["TERM"] = self.term_settings.get("type",DEFAULT_TERM_TYPE)
        dimensions = "%dx%d" % (width, height)
        if winwidth and winheight:
            dimensions += ";%dx%d" % (winwidth, winheight)
        env[ENV_PREFIX+"DIMENSIONS"] = dimensions
        env["COLUMNS"] = str(width)
        env["LINES"] = str(height)

        if self.server_url:
            env[ENV_PREFIX+"URL"] = self.server_url

        return env

    def new_terminal(self, **kwargs):
        options = self.term_settings.copy()
        options['shell_command'] = self.shell_command
        options.update(kwargs)
        options['env'] = self.make_term_env(**options)
        return Terminal.spawn(**options)

    def start_reading(self, term):
        term.register('died', lambda : self.ioloop.remove_handler(term.fd))
        self.ioloop.add_handler(term.fd, term.read_ready, self.ioloop.READ)

    def get_terminal(self, url_component=None):
        raise NotImplementedError

    def shutdown(self):
        self.kill_all()

    def kill_all(self):
        raise NotImplementedError


class SingleTermManager(TermManagerBase):
    def __init__(self, **kwargs):
        super(SingleTermManager, self).__init__(**kwargs)
        self.terminal = None

    def get_terminal(self, url_component=None):
        if self.terminal is None:
            self.terminal = self.new_terminal()
            self.start_reading(self.terminal)
        return self.terminal

    def kill_all(self):
        if self.terminal is not None:
            self.terminal.kill()

def MaxTerminalsReached(Exception):
    def __init__(self, max_terminals):
        self.max_terminals = max_terminals
    
    def __str__(self):
        return "Cannot create more than %d terminals" % self.max_terminals

class UniqueTermManager(TermManagerBase):
    """Give each websocket a unique terminal to use."""
    def __init__(self, max_terminals=None, **kwargs):
        super(UniqueTermManager, self).__init__(**kwargs)
        self.max_terminals = max_terminals
        self.terminals = []

    def get_terminal(self, url_component=None):
        term = self.new_terminal()
        self.start_reading(term)
        self.terminals.append(term)
        return term

    def kill_all(self):
        for term in self.terminals:
            term.kill()
    

class NamedTermManager(TermManagerBase):
    """Share terminals between websockets connected to the same endpoint.
    """
    def __init__(self, max_terminals=None, **kwargs):
        super(NamedTermManager, self).__init__(**kwargs)
        self.max_terminals = max_terminals
        self.terminals = {}

    def get_terminal(self, term_name):
        assert term_name is not None
        
        if term_name in self.terminals:
            return self.terminals[term_name]
        
        if self.max_terminals and len(self.terminals) >= self.max_terminals:
            raise MaxTerminalsReached(self.max_terminals)

        # Create new terminal
        logging.info("New terminal %s: %s", term_name)
        term = self.new_terminal()
        self.terminals[term_name] = term
        self.start_reading(term)
        return term

    def _next_available_name(self):
        for n in itertools.count(start=1):
            name = "tty%d" % n
            if name not in self.terminals:
                return name

    def new_named_terminal(self):
        name = self._next_available_name()
        term = self.new_terminal()
        self.terminals[name] = term
        self.start_reading(term)
        return name, term

    def kill_all(self):
        for term in self.terminals.values():
            term.kill()

if __name__ == "__main__":
    ## Code to test Terminal on regular terminal
    ## Re-size terminal to 80x25 before testing

    from optparse import OptionParser
    usage = "usage: %prog [<shell_command>]"
    parser = OptionParser(usage=usage)
    parser.add_option("-l", "--logging",
                  action="store_true", dest="logging", default=False,
                  help="Enable logging")

    (options, args) = parser.parse_args()

    shell_cmd = args[:] if args else ["bash"]

    # Determine terminal width, height
    height, width = struct.unpack("hh", fcntl.ioctl(pty.STDOUT_FILENO, termios.TIOCGWINSZ, "1234"))
    if not width or not height:
        try:
            height, width = [int(os.getenv(var)) for var in ("LINES", "COLUMNS")]
        except Exception:
            height, width = 25, 80

    Prompt = "> "
    Log_file = "pyxshell.log" if options.logging else ""
    def client_callback(term_name, response_id, command, *args):
        if command == "stdout":
            output = args[0]
            sys.stdout.write(output)
            sys.stdout.flush()

    Term_manager = TermManager(client_callback, shell_cmd, log_file=Log_file, log_level=logging.INFO)
    terminal, Term_name, term_cookie = Term_manager.terminal(height=height, width=width)

    print("**Type Control-D Control-D to exit**", file=sys.stderr)

    test_str = b'\xe2\x94\x80 \xe2\x94\x82 \xe2\x94\x8c \xe2\x94\x98 \xe2\x94\x90 \xe2\x94\x94 \xe2\x94\x9c \xe2\x94\xa4 \xe2\x94\xac \xe2\x94\xb4 \xe2\x94\xbc \xe2\x95\x90 \xe2\x95\x91 \xe2\x95\x94 \xe2\x95\x9d \xe2\x95\x97 \xe2\x95\x9a \xe2\x95\xa0 \xe2\x95\xa3 \xe2\x95\xa6 \xe2\x95\xa9 \xe2\x95\xac'.decode("utf-8")

    Term_attr = termios.tcgetattr(pty.STDIN_FILENO)
    try:
        tty.setraw(pty.STDIN_FILENO)
        expectEOF = False
        terminal.pty_write("echo '%s'\n" % test_str)
        while True:
            ##data = raw_input(Prompt)
            ##Term_manager.write(data+"\n")
            data = os.read(pty.STDIN_FILENO, 1024)
            if byte_code(data[0]) == 4:
                if expectEOF: raise EOFError
                expectEOF = True
            else:
                expectEOF = False
            if not data:
                raise EOFError
            str_data = data.decode("utf-8") if isinstance(data, bytes) else data
            terminal.pty_write(str_data)
    except EOFError:
        Term_manager.shutdown()
    finally:
        # Restore terminal attributes
        termios.tcsetattr(pty.STDIN_FILENO, termios.TCSANOW, Term_attr)
