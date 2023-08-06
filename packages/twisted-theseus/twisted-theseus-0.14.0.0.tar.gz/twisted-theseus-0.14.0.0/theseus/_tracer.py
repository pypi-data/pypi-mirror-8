# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

import collections
import inspect
import sys

from twisted.internet import defer
from twisted.python import log


DeferredStatus = collections.namedtuple(
    'DeferredStatus', ['frame', 'deferred', 'returned_at'])
FunctionData = collections.namedtuple('FunctionData', ['calls', 'time'])
FunctionCall = collections.namedtuple('FunctionCall', ['count', 'time'])
EMPTY_CALL = FunctionCall(0, 0)
IGNORE = object()


class Function(collections.namedtuple('Function', ['filename', 'func'])):
    @classmethod
    def of_frame(cls, frame):
        return cls(frame.f_code.co_filename, frame.f_code.co_name)


class FakeFrame(object):
    def __init__(self, code, back):
        self.f_code = code
        self.f_back = back


class Tracer(object):
    """
    A tracer for Deferred-returning functions.

    The general idea is that if a function returns a Deferred, said Deferred
    will have a callback attached to it for timing how long it takes before the
    Deferred fires. Then, that time is recorded along with the function and all
    of its callers.
    """

    def __init__(self, reactor=None):
        if reactor is None:
            from twisted.internet import reactor
        self._reactor = reactor
        self._deferreds = {}
        self._unwindGenerator_frames = set()
        self._function_data = {}

    def _trace(self, frame, event, arg):
        meth = getattr(self, '_event_' + event, None)
        result = None
        if meth is not None:
            result = meth(frame, arg)
        if result is not IGNORE:
            return self._trace

    def _event_call(self, frame, arg):
        # Don't trace generators; inlineCallbacks is handled separately.
        if frame.f_code.co_flags & inspect.CO_GENERATOR:
            return IGNORE

        # Tracing functions from twisted.internet.defer adds a lot of noise, so
        # don't do that.
        if frame.f_globals.get('__name__') == 'twisted.internet.defer':
            # The only exception to the above is unwindGenerator, an
            # implementation detail of inlineCallbacks.
            if frame.f_code.co_name == 'unwindGenerator':
                self._unwindGenerator_frames.add(frame)
            else:
                return IGNORE

    def _event_return(self, frame, arg):
        if not isinstance(arg, defer.Deferred):
            return
        # Detect when unwindGenerator returns. unwindGenerator is part of the
        # inlineCallbacks implementation. If unwindGenerator is returning, it
        # means that the Deferred being returned is the Deferred that will be
        # returned from the wrapped function. Yank the wrapped function out and
        # fake a call stack that makes it look like unwindGenerator isn't
        # involved at all and the wrapped function is being called
        # directly. This /does/ involve Twisted implementation details, but as
        # far back as twisted 2.5.0 (when inlineCallbacks was introduced), the
        # name 'unwindGenerator' and the local 'f' are the same. If this ever
        # changes in the future, I'll have to update this code.
        if frame in self._unwindGenerator_frames:
            self._unwindGenerator_frames.remove(frame)
            wrapped_func = frame.f_locals['f']
            frame = FakeFrame(wrapped_func.func_code, frame.f_back)
        key = frame, arg
        self._deferreds[key] = DeferredStatus(
            frame, arg, self._reactor.seconds())
        arg.addBoth(self._deferred_fired, key)

    def _get_function(self, frame):
        func = Function.of_frame(frame)
        data = self._function_data.get(func)
        if data is None:
            data = self._function_data[func] = FunctionData({}, 0)
        return func, data

    def _deferred_fired(self, result, key):
        fired_at = self._reactor.seconds()
        status = self._deferreds.pop(key, None)
        if status is None:
            return
        delta = int((fired_at - status.returned_at) * 1000000)
        frame, _ = key
        try:
            self._record_timing(delta, frame)
        except Exception:
            log.err(None, 'an error occurred recording timing information')
        return result

    def _record_timing(self, delta, frame):
        frame_func, frame_data = self._get_function(frame)
        self._function_data[frame_func] = frame_data._replace(
            time=frame_data.time + delta)

        while frame.f_back is not None:
            caller = frame.f_back
            frame_func = Function.of_frame(frame)
            _, caller_data = self._get_function(caller)
            call = caller_data.calls.get(frame_func, EMPTY_CALL)
            caller_data.calls[frame_func] = call._replace(
                count=call.count + 1, time=call.time + delta)
            frame = caller

    def install(self):
        """
        Install this tracer as a global `trace hook
        <https://docs.python.org/2/library/sys.html#sys.settrace>`_.

        The old trace hook, if one is set, will be discarded.
        """
        sys.settrace(self._trace)

    def write_data(self, fobj):
        """
        Write profiling data in `callgrind format
        <http://valgrind.org/docs/manual/cl-format.html>`_ to an open file
        object.

        The file object will not be closed.
        """
        fobj.write('events: Nanoseconds\n')
        for func, data in sorted(self._function_data.iteritems()):
            fobj.write('fn={0.func} {0.filename}\n'.format(func))
            fobj.write('0 {0.time}\n'.format(data))
            for callee, call in sorted(data.calls.iteritems()):
                fobj.write('cfn={0.func} {0.filename}\n'.format(callee))
                fobj.write('calls={0.count} 0\n0 {0.time}\n'.format(call))
            fobj.write('\n')
