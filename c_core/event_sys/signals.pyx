# pxd imports
from cpython.weakref cimport PyWeakref_NewRef, PyWeakref_GET_OBJECT
from messages cimport Message

# stdlib imports
from bisect import insort


class KillSignalException(Exception):
    pass


class _NullContext(object):
    pass

_null_context = _NullContext()


cdef class NotifierManager:

    def __cinit__(self):
        self._conn_count = 0
        self._notifiers = []

    def _dead_notifier(self, wr):
        self._c_dead_notifier(wr)

    cdef _c_dead_notifier(self, wr):
        cdef list remove = []
        cdef list notifiers = self._notifiers
        cdef int i
        cdef tuple item

        for i, item in enumerate(notifiers):
            if item[2] == wr:
                remove.append(i)

        remove.reverse()
        for i in remove:
            notifiers.pop(i)

    cpdef add_notifier(self, notifier, priority):
        cb = self._dead_notifier
        item = (priority, self._conn_count, PyWeakref_NewRef(notifier, cb))
        insort(self._notifiers, item)
        self._conn_count += 1

    cpdef remove_notifier(self, notifier):
        self._c_dead_notifier(PyWeakref_NewRef(notifier, None))

    cpdef notifiers(self):
        cdef tuple item
        cdef list res = []
        
        for item in self._notifiers:
            res.append(<object>PyWeakref_GET_OBJECT(item[2]))

        return res
    

cdef class Signal:

    def __cinit__(self):
        self._mgrs = {}

    def _dead_context(self, wr):
        del self._mgrs[wr]

    cpdef connect(self, notifier, priority=16, context=_null_context):
        cdef NotifierManager mgr
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, self._dead_context)

        if wr_context not in mgrs:
            mgr = NotifierManager()
            mgrs[wr_context] = mgr
        else:
            mgr = mgrs[wr_context]

        mgr.add_notifier(notifier, priority)

    cpdef disconnect(self, notifier, context=_null_context):
        cdef NotifierManager mgr
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, None)

        if wr_context in mgrs:
            mgr = mgrs[wr_context]
            mgr.remove_notifier(notifier)

    cpdef emit(self, Message message, context=_null_context):
        cdef NotifierManager mgr
        cdef list notifiers
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, None)

        if wr_context in mgrs:
            mgr = mgrs[wr_context]
            notifiers = mgr.notifiers()

            if notifiers:
                message.initialize()
                
                if context is _null_context:

                    for notifier in notifiers:
                        try:
                            notifier(message)
                        except KillSignalException:
                            break
                        finally:
                            message.update()

                else:

                    for notifier in notifiers:
                        try:
                            notifier(context, message)
                        except KillSignalException:
                            break
                        finally:
                            message.update()

                message.finalize()

   
