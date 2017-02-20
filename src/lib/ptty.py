import os
import select
import sys
import signal
from ptyprocess import PtyProcessUnicode

STDIN_FD = 0 # default stdin file number
STDOUT_FD = 1 # default stdout file nuumber

class PTY(object):
    def __init__(self):
        self.log = ''
        self.pty = None

    def set_quit_signal(self):
        oldsignal = signal.getsignal(signal.SIGINT)
        import types
        if isinstance(oldsignal, types.BuiltinFunctionType):
            signal.signal(signal.SIGINT, self.quit)

    def spawn(self, argv):
        self.set_quit_signal()
        self.pty = PtyProcessUnicode.spawn(argv)
        self._copy()
        self.pty.wait()
        return (self.pty.exitstatus, self.log)

    def quit(self, *args, **kwargs):
        sys.exit(1)  # must exit with something not '0'

    def write_log(self, b):
        assert isinstance(b, str), 'log only str'
        self.log += b

    def _copy(self):
        '''
        Main select loop. Passes all data to self.master_read() or self.stdin_read().
        '''
        assert isinstance(self.pty, PtyProcessUnicode)
        while True:
            rfds, wfds, xfds = select.select([self.pty.fd, STDIN_FD], [], [])

            anything = False

            if self.pty.fd in rfds:
                anything |= self._has_child_response()
            if STDIN_FD in rfds:
                anything |= self._has_user_input()

            if not anything:
                break

    def _has_child_response(self):
        assert isinstance(self.pty, PtyProcessUnicode)
        try:
            data = self.pty.read(1024)
        except EOFError:
            return False

        # redirect the child's output to the stdout
        self._write_stdout(data.encode('utf-8'))
        self.write_log(data)

        return True

    def _has_user_input(self):
        assert isinstance(self.pty, PtyProcessUnicode)
        data = self._read_stdin(1024)
        if not data:
            return False
        self.pty.write(data.decode('utf-8'))
        return True

    def _read_stdin(self, bufsize):
        return os.read(STDIN_FD, bufsize)

    def _write_stdout(self, data):
        assert isinstance(data, bytes), '`data` must be a bytes'
        os.write(STDOUT_FD, data)
