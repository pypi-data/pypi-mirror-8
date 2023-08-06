from __future__ import absolute_import

import select

from .. import io, scheduler, util


def green_select(rlist, wlist, xlist, timeout=None):
    robjs = {}
    wobjs = {}
    fds = {}

    for fd in rlist:
        fdnum = fd if isinstance(fd, int) else fd.fileno()
        robjs[fdnum] = fd
        fds[fdnum] = 1

    for fd in wlist:
        fdnum = fd if isinstance(fd, int) else fd.fileno()
        wobjs[fdnum] = fd
        if fdnum in fds:
            fds[fdnum] |= 2
        else:
            fds[fdnum] = 2

    events = io.wait_fds(fds.items(), timeout=timeout, inmask=1, outmask=2)

    rlist_out, wlist_out = [], []
    for fd, event in events:
        if event & 1:
            rlist_out.append(robjs[fd])
        if event & 2:
            wlist_out.append(wobjs[fd])

    return rlist_out, wlist_out, []


if hasattr(select, "poll"):
    all_poll_evs = select.POLLIN | select.POLLOUT | select.POLLPRI
else:
    all_poll_evs = 0


class green_poll(object):
    def __init__(self):
        self._registry = {}

    def modify(self, fd, eventmask):
        fd = fd if isinstance(fd, int) else fd.fileno()
        if fd not in self._registry:
            raise IOError(2, "No such file or directory")
        self._registry[fd] = eventmask

    def poll(self, timeout=None):
        if timeout is not None:
            timeout = float(timeout) / 1000
        return io.wait_fds(self._registry.items(), timeout=timeout,
                           inmask=select.POLLIN, outmask=select.POLLOUT)

    def register(self, fd, eventmask=all_poll_evs):
        fd = fd if isinstance(fd, int) else fd.fileno()
        self._registry[fd] = eventmask

    def unregister(self, fd):
        fd = fd if isinstance(fd, int) else fd.fileno()
        del self._registry[fd]


if hasattr(select, 'epoll'):
    all_epoll_evs = select.EPOLLIN | select.EPOLLOUT | select.EPOLLPRI
else:
    all_epoll_evs = 0


class green_epoll(object):
    def __init__(self, sizehint=-1, from_ep=None):
        self._readable = util.Event()
        if from_ep:
            self._epoll = from_ep
        else:
            self._epoll = original_epoll(sizehint)

    def _on_readable(self):
        self._readable.set()
        self._readable.clear()

    def close(self):
        self._epoll.close()

    @property
    def closed(self):
        return self._epoll.closed
    _closed = closed

    def fileno(self):
        return self._epoll.fileno()

    @classmethod
    def fromfd(cls, fd):
        return cls(from_ep=original_epoll_fromfd(fd))

    def modify(self, fd, eventmask):
        self._epoll.modify(fd, eventmask)

    def poll(self, timeout=None, maxevents=-1):
        onr = self._on_readable
        reg = scheduler._register_fd(self._epoll.fileno(), onr, None)
        try:
            self._readable.wait(timeout=timeout)
            return self._epoll.poll(0, maxevents)
        finally:
            scheduler._unregister_fd(self._epoll.fileno(), onr, None, reg)

    def register(self, fd, eventmask=all_epoll_evs):
        self._epoll.register(fd, eventmask)

    def unregister(self, fd):
        self._epoll.unregister(fd)


class green_kqueue(object):
    def __init__(self, from_kq=None):
        self._readable = util.Event()
        self._writable = util.Event()
        if from_kq:
            self._kqueue = from_kq
        else:
            self._kqueue = original_kqueue()

    def _on_readable(self):
        self._readable.set()
        self._readable.clear()

    def _on_writable(self):
        self._writable.set()
        self._writable.clear()

    def close(self):
        self._kqueue.close()

    @property
    def closed(self):
        return self._kqueue.closed
    _closed = closed

    def control(self, events, max_events, timeout=None):
        if not max_events:
            return self._kqueue.control(events, max_events, 0)

        onr, onw = self._on_readable, self._on_writable
        reg = scheduler._register_fd(self._kqueue.fileno(), onr, onw)
        try:
            self._readable.wait(timeout=timeout)
            return self._kqueue.control(events, max_events, 0)
        finally:
            scheduler._unregister_fd(self._kqueue.fileno(), onr, onw, reg)

    def fileno(self):
        return self._kqueue.fileno()

    @classmethod
    def fromfd(cls, fd):
        return cls(from_kq=original_kqueue_fromfd(fd))


patchers = {'select': green_select}

if hasattr(select, "poll"):
    patchers['poll'] = green_poll

if hasattr(select, "epoll"):
    patchers['epoll'] = green_epoll
    original_epoll = select.epoll
    original_epoll_fromfd = select.epoll.fromfd

if hasattr(select, "kqueue"):
    patchers['kqueue'] = green_kqueue
    original_kqueue = select.kqueue
    original_kqueue_fromfd = select.kqueue.fromfd
