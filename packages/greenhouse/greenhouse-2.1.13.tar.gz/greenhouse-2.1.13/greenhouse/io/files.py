from __future__ import absolute_import, with_statement

import contextlib
import errno
import fcntl
import os
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from .. import scheduler, util


__all__ = ["File", "stdin", "stdout", "stderr"]

_open = open
_file = file
_read = os.read
_write = os.write
_fdopen = os.fdopen
_osopen = os.open
_osclose = os.close
_fcntl = fcntl.fcntl


class FileBase(object):
    CHUNKSIZE = 8192
    NEWLINE = "\n"

    def __init__(self):
        self._rbuf = StringIO()
        self.encoding = None

    def __iter__(self):
        line = self.readline()
        while line:
            yield line
            line = self.readline()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def read(self, size=-1):
        """read a number of bytes from the file and return it as a string

        .. note:: this method will block if there is no data already available

        :param size:
            the maximum number of bytes to read from the file. < 0 means read
            the file to the end
        :type size: int

        :returns: a string of the read file contents
        """
        chunksize = size < 0 and self.CHUNKSIZE or min(self.CHUNKSIZE, size)

        buf = self._rbuf
        buf.seek(0, os.SEEK_END)
        collected = buf.tell()

        while 1:
            if size >= 0 and collected >= size:
                # we have read enough already
                break

            output = self._read_chunk(chunksize)
            if output is None:
                continue

            if not output:
                # nothing more to read
                break

            collected += len(output)
            buf.write(output)

        # get rid of the old buffer
        rc = buf.getvalue()
        buf.seek(0)
        buf.truncate()

        if size >= 0:
            # leave the overflow in the buffer
            buf.write(rc[size:])
            return rc[:size]
        return rc

    def readline(self, max_len=-1):
        """read from the file until a newline is encountered

        .. note::

            this method will block if there isn't already a full line available
            from the data source

        :param max_len: stop reading a single line after this many bytes
        :type max_len: int

        :returns:
            a string of the line it read from the file, including the newline
            at the end
        """
        buf = self._rbuf
        newline, chunksize = self.NEWLINE, self.CHUNKSIZE
        buf.seek(0)

        text = buf.read()
        if len(text) >= max_len >= 0:
            buf.seek(0)
            buf.truncate()
            buf.write(text[max_len:])
            return text[:max_len]

        while text.find(newline) < 0:
            text = self._read_chunk(chunksize)
            if text is None:
                text = ''
                continue
            if buf.tell() + len(text) >= max_len >= 0:
                text = buf.getvalue() + text
                buf.seek(0)
                buf.truncate()
                buf.write(text[max_len:])
                return text[:max_len]
            if not text:
                break
            buf.write(text)
        else:
            # found a newline
            rc = buf.getvalue()
            index = rc.find(newline) + len(newline)

            buf.seek(0)
            buf.truncate()
            buf.write(rc[index:])
            return rc[:index]

        # hit the end of the file, no more newlines
        rc = buf.getvalue()
        buf.seek(0)
        buf.truncate()
        return rc

    def readlines(self, bufsize=-1):
        """reads the entire file, producing the lines one at a time

        .. note:: this method will block until the data source is exhausted

        :param bufsize: the read buffer size to use
        :type bufsize: int

        :returns: a list of all the lines in the file to the end
        """
        return list(self.__iter__())

    def write(self, data):
        """write data to the file

        :param data:
            the data to write into the file, at the descriptor's current
            position
        :type data: str
        """
        while data:
            went = self._write_chunk(data)
            if went is None:
                continue
            data = data[went:]

    def writelines(self, lines):
        """write a sequence of strings into the file

        :meth:`writelines` does not add newlines to the strings

        :param lines: a sequence of strings to write to the file
        :type lines: iterable
        """
        self.write("".join(lines))

    @staticmethod
    def _mode_to_flags(mode):
        flags = os.O_RDONLY | os.O_NONBLOCK  # always non-blocking
        if (('w' in mode or 'a' in mode) and 'r' in mode) or '+' in mode:
            # both read and write
            flags |= os.O_RDWR
        elif 'w' in mode or 'a' in mode:
            # else just write
            flags |= os.O_WRONLY

        if 'a' in mode:
            # append-write mode
            flags |= os.O_APPEND

        # builtin open() also creates the file on writable opens
        if flags & (os.O_WRONLY|os.O_RDWR):
            flags |= os.O_CREAT

        return flags


class File(FileBase):
    """the greenhouse drop-in replacement for the built-in ``file`` type

    this class will use non-blocking file descriptors for its IO, so that
    whatever readystate information the OS and filesystem provide will be used
    to block only a single coroutine rather than the whole process.
    unfortunately filesystems tend to be very unreliable in this regard.
    """
    def __init__(self, name, mode='rb'):
        super(File, self).__init__()
        self.mode = mode
        self.name = name
        self._closed = False

        # translate mode into the proper open flags
        flags = self._mode_to_flags(mode)

        # open the file, get a descriptor
        try:
            self._fileno = _osopen(name, flags)
        except OSError, exc:
            # stdlib open() raises IOError if the file doesn't exist, os.open
            # raises OSError. pfft, whatever.
            raise IOError(*exc.args)

        # try to drive the asyncronous waiting off of the polling interface,
        # but epoll doesn't seem to support filesystem descriptors, so fall
        # back to waiting with a simple yield
        self._set_up_waiting()

    @contextlib.contextmanager
    def _registered(self, read=True, write=True):
        rd = self._on_readable if read else None
        wr = self._on_writable if write else None
        try:
            reg = scheduler._register_fd(self._fileno, rd, wr)
        except EnvironmentError, exc:
            if exc.args and exc.args[0] in errno.errorcode:
                raise IOError, IOError(*exc.args), sys.exc_info()[2]
            raise

        try:
            yield
        finally:
            try:
                scheduler._unregister_fd(self._fileno, rd, wr, reg)
            except EnvironmentError, exc:
                if exc.args and exc.args[0] in errno.errorcode:
                    raise IOError, IOError(*exc.args), sys.exc_info()[2]
                raise

    def _set_up_waiting(self):
        if scheduler.state.poller.supports(self):
            self._wait = self._wait_event
            self._readable = util.Event()
            self._writable = util.Event()
        else:
            self._wait = self._wait_yield

    def _on_readable(self):
        self._readable.set()
        self._readable.clear()

    def _on_writable(self):
        self._writable.set()
        self._writable.clear()

    def _wait_event(self, reading):
        "wait on our events"
        with self._registered(reading, not reading):
            (self._readable if reading else self._writable).wait()

        if scheduler.state.interrupted:
            raise IOError(errno.EINTR, "interrupted system call")

    def _wait_yield(self, reading):
        "generic busy wait, for when polling won't work"
        scheduler.pause()

    def _read_chunk(self, size):
        try:
            return _read(self._fileno, size)
        except EnvironmentError, err:
            if err.args[0] in (errno.EAGAIN, errno.EINTR):
                self._wait(reading=True)
                return None
            raise

    def _write_chunk(self, data):
        try:
            return _write(self._fileno, data)
        except EnvironmentError, err:
            if err.args[0] in (errno.EAGAIN, errno.EINTR):
                self._wait(reading=False)
                return None
            raise

    @staticmethod
    def _add_flags(fd, flags):
        fdflags = _fcntl(fd, fcntl.F_GETFL)
        if fdflags | flags != fdflags:
            _fcntl(fd, fcntl.F_SETFL, flags | fdflags)

    @classmethod
    def fromfd(cls, fd, mode='rb', bufsize=-1):
        """create a cooperating greenhouse file from an existing descriptor

        :param fd: the file descriptor to wrap in a new file object
        :type fd: int
        :param mode: the file mode
        :type mode: str
        :param bufsize:
            the size of read buffer to use. 0 indicates unbuffered, and < 0
            means use the system default. defaults to -1

        :returns: a new :class:`File` object connected to the descriptor
        """
        fp = object.__new__(cls)  # bypass __init__
        fp._rbuf = StringIO()
        fp.encoding = None
        fp.mode = mode
        fp._fileno = fd
        fp._closed = False

        cls._add_flags(fd, cls._mode_to_flags(mode))
        fp._set_up_waiting()

        return fp

    def close(self):
        "close the file, and its underlying descriptor"
        self._closed = True
        _osclose(self._fileno)

    @property
    def closed(self):
        "return True if the file descriptor is closed"
        return self._closed

    def fileno(self):
        "get the file descriptor integer"
        return self._fileno

    def flush(self):
        """flush buffered writes to disk immediately

        this is provided for compatibility -- this class does no write
        buffering itself, so it is a no-op
        """
        return None

    def isatty(self):
        "return whether the file is connected to a tty or not"
        try:
            return os.isatty(self._fileno)
        except OSError, e:
            raise IOError(*e.args)

    def seek(self, position, modifier=0):
        """move the cursor on the file descriptor to a different location

        :param position:
            an integer offset from the location indicated by the modifier
        :type position: int
        :param modifier:
            an indicator of how to find the seek location.

            - ``os.SEEK_SET`` means start from the beginning of the file
            - ``os.SEEK_CUR`` means start wherever the cursor already is
            - ``os.SEEK_END`` means start from the end of the file

            the default is ``os.SEEK_SET``
        """
        os.lseek(self._fileno, position, modifier)

        # clear out the buffer
        buf = self._rbuf
        buf.seek(0)
        buf.truncate()

    def tell(self):
        "get the file descriptor's position relative to the file's beginning"
        with _fdopen(os.dup(self._fileno)) as fp:
            return fp.tell()


class _StdIOFile(FileBase):
    def __init__(self, fd):
        super(_StdIOFile, self).__init__()
        self._fileno = fd
        self._readable = util.Event()
        self._writable = util.Event()

    def _on_readable(self):
        self._readable.set()
        self._readable.clear()

    def _on_writable(self):
        self._writable.set()
        self._writable.clear()

    def _read_chunk(self, size):
        onr = self._on_readable
        reg = scheduler._register_fd(self._fileno, onr, None)
        try:
            self._readable.wait()
        finally:
            scheduler._unregister_fd(self._fileno, onr, None, reg)

        if scheduler.state.interrupted:
            raise IOError(errno.EINTR, "interrupted system call")

        return _read(self._fileno, size)

    def _write_chunk(self, data):
        onw = self._on_writable
        reg = scheduler._register_fd(self._fileno, None, onw)
        try:
            self._writable.wait()
        finally:
            scheduler._unregister_fd(self._fileno, None, onw, reg)

        if scheduler.state.interrupted:
            raise IOError(errno.EINTR, "interrupted system call")

        return _write(self._fileno, data)

    def close(self):
        _osclose(self._fileno)

    def fileno(self):
        return self._fileno

    def flush(self):
        return None

    def isatty(self):
        try:
            return os.isatty(self._fileno)
        except OSError, exc:
            raise IOError(*exc.args)

    def seek(self, position, modifier=0):
        raise IOError(errno.ESPIPE, "Illegal seek")

    def tell(self):
        raise IOError(errno.ESPIPE, "Illegal seek")


stdin = _StdIOFile(getattr(sys.stdin, "fileno", lambda: 0)())
"a non-blocking file object for cooperative stdin reading"

stdout = _StdIOFile(getattr(sys.stdout, "fileno", lambda: 1)())
"a non-blocking file object for cooperative stdout writing"

stderr = _StdIOFile(getattr(sys.stderr, "fileno", lambda: 2)())
"a non-blocking file object for cooperative stderr writing"
