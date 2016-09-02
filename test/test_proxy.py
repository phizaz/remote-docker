# Copyright (c) 2011 Joshua D. Bartlett
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Edited: Konpat Preechakul
# Note: Only supports unix based operating systems, not Windows

import array
import fcntl
import os
import pty
import select
import signal
import sys
import termios
import tty


class PTY(object):
    def __init__(self):
        self.old_handler = None
        self.master_fd = None
        self.mode = None
        self.log = b''
        self.loggable_chars = dict.fromkeys(range(32))

    def spawn(self, argv):
        '''
        Create a spawned process.
        Based on the code for pty.spawn().
        '''
        assert self.master_fd is None
        assert isinstance(argv, list)

        pid, master_fd = pty.fork()
        self.master_fd = master_fd

        if pid == pty.CHILD:
            os.execlp(argv[0], *argv)  # and not ever returned

        self._init()
        try:
            self._copy()  # start communication
        except Exception:
            # unexpected errors
            self._del()
            raise
        self._del()

        return self.log.decode()

    def write_log(self, b):
        assert isinstance(b, bytes), 'log only bytes'
        # self.log += str.translate(self.loggable_chars)
        self.log += b

    def _init(self):
        # unexpected quit
        signal.signal(signal.SIGINT, self._sig_quit)
        signal.signal(signal.SIGTERM, self._sig_quit)

        self.old_handler = signal.signal(signal.SIGWINCH, self._signal_winch)
        self._init_fd()
        self._init_tty()

    def _del(self):
        self._del_tty()
        self._del_fd()
        signal.signal(signal.SIGWINCH, self.old_handler)
        self.old_handler = None

    def _sig_quit(self, signum, frame):
        self._del()
        if signum == signal.SIGINT:
            sys.exit(0)
        else:
            sys.exit(1)

    def _init_tty(self):
        try:
            self.mode = tty.tcgetattr(pty.STDIN_FILENO)
            tty.setraw(pty.STDIN_FILENO)  # this seems to change the behavior of the stdout
        except tty.error:
            pass

    def _del_tty(self):
        if self.mode:
            # restore the tty mode for stdout
            tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, self.mode)

    def _init_fd(self):
        '''
        Called once when the pty is first set up.
        '''
        self._set_pty_size()

    def _del_fd(self):
        if self.master_fd:
            os.close(self.master_fd)
            self.master_fd = None

    def _copy(self):
        '''
        Main select loop. Passes all data to self.master_read() or self.stdin_read().
        '''
        assert self.master_fd is not None
        master_fd = self.master_fd
        while True:
            rfds, wfds, xfds = select.select([master_fd, pty.STDIN_FILENO], [], [])

            anything = False

            if master_fd in rfds:
                anything |= self._has_child_response()
            if pty.STDIN_FILENO in rfds:
                anything |= self._has_user_input()

            if not anything:
                break

    def _has_child_response(self):
        data = self._read_childin(1024)
        if not data:
            return False

        # redirect the child's output to the stdout
        self._write_stdout(data)
        self.write_log(data)

        return True

    def _has_user_input(self):
        data = self._read_stdin(1024)
        if not data:
            return False
        self._write_child_stdin(data)
        return True

    def _read_childin(self, bufsize):
        # childin --- connect --- child's stdout
        return os.read(self.master_fd, bufsize)

    def _read_stdin(self, bufsize):
        return os.read(pty.STDIN_FILENO, bufsize)

    def _write_child_stdin(self, data):
        master_fd = self.master_fd
        assert isinstance(data, bytes), '`data` must be a bytes'
        assert master_fd is not None
        while data != '':
            n = os.write(master_fd, data)
            data = data[n:]

    def _write_stdout(self, data):
        assert isinstance(data, bytes), '`data` must be a bytes'
        os.write(pty.STDOUT_FILENO, data)

    def _signal_winch(self, signum, frame):
        '''
        Signal handler for SIGWINCH - window size has changed.
        '''
        self._set_pty_size()

    def _set_pty_size(self):
        '''
        Sets the window size of the child pty based on the window size of our own controlling terminal.
        '''
        assert self.master_fd is not None

        # Get the terminal size of the real terminal, set it on the pseudoterminal.
        buf = array.array('h', [0, 0, 0, 0])
        fcntl.ioctl(pty.STDOUT_FILENO, termios.TIOCGWINSZ, buf, True)
        fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, buf)

if __name__ == '__main__':
    i = PTY()
    log = i.spawn(['echo', 'test'])
    print(('log:', log))
