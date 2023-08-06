from __future__ import absolute_import

import errno
import functools
import time

from .. import compat, scheduler


__all__ = ["wait_fds"]


def wait_fds(fd_events, inmask=1, outmask=2, timeout=None):
    """wait for the first of a number of file descriptors to have activity

    .. note:: this method can block

        it will return once there is relevant activity on the file descriptors,
        or the timeout expires

    :param fd_events:
        two-tuples, each one a file descriptor and a mask made up of the inmask
        and/or the outmask bitwise-ORd together
    :type fd_events: list
    :param inmask: the mask to use for readable events (default 1)
    :type inmask: int
    :param outmask: the mask to use for writable events (default 2)
    :type outmask: int
    :param timeout:
        the maximum time to wait before raising an exception (default None)
    :type timeout: int, float or None

    :returns:
        a list of two-tuples, each is a file descriptor and an event mask (made
        up of inmask and/or outmask bitwise-ORd together) representing readable
        and writable events
    """
    current = compat.getcurrent()
    activated = {}
    poll_regs = {}
    callback_refs = {}

    def activate(fd, event):
        if not activated and timeout != 0:
            # this is the first invocation of `activated` for a blocking
            # `wait_fds` call, so re-schedule the blocked coroutine
            scheduler.schedule(current)

            # if there was a timeout then also have to pull
            # the coroutine from the timed_paused structure
            if timeout:
                scheduler._remove_timer(waketime, current)

        # in any case, set the event information
        activated.setdefault(fd, 0)
        activated[fd] |= event

    for fd, events in fd_events:
        readable = None
        writable = None
        if events & inmask:
            readable = functools.partial(activate, fd, inmask)
        if events & outmask:
            writable = functools.partial(activate, fd, outmask)

        callback_refs[fd] = (readable, writable)
        poll_regs[fd] = scheduler._register_fd(fd, readable, writable)

    if timeout:
        # real timeout value, schedule ourself `timeout` seconds in the future
        waketime = time.time() + timeout
        scheduler.pause_until(waketime)
    elif timeout == 0:
        # timeout == 0, only pause for 1 loop iteration
        scheduler.pause()
    else:
        # timeout is None, it's up to _hit_poller->activate to bring us back
        scheduler.state.mainloop.switch()

    for fd, reg in poll_regs.iteritems():
        readable, writable = callback_refs[fd]
        scheduler._unregister_fd(fd, readable, writable, reg)

    if scheduler.state.interrupted:
        raise IOError(errno.EINTR, "interrupted system call")

    return activated.items()
