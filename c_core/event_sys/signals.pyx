# pxd imports
from cpython.weakref cimport PyWeakref_NewRef, PyWeakref_GET_OBJECT
from messages cimport Message

# stdlib imports
from bisect import insort


class KillSignalException(Exception):
    pass


class NoneContext(object):
    
    def __repr__(self):
        return 'NoneContext'

    def __str__(self):
        return self.__repr__()

NoneContext = NoneContext()


cdef class NotifierManager:

    def __cinit__(self):
        self._conn_count = 0
        self._notifiers = []
        
        def remove(wr, selfref=PyWeakref_NewRef(self, None)):
            cdef NotifierManager _self = <object>PyWeakref_GET_OBJECT(selfref)
            if _self is not None:
                _self._c_remove(wr)

        self._remove = remove

    cdef _c_remove(self, wr):
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
        cb = self._remove
        item = (priority, self._conn_count, PyWeakref_NewRef(notifier, cb))
        insort(self._notifiers, item)
        self._conn_count += 1

    cpdef remove_notifier(self, notifier):
        self._c_remove(PyWeakref_NewRef(notifier, None))

    cpdef notifiers(self):
        cdef tuple item
        cdef list res = []
        
        for item in self._notifiers:
            res.append(<object>PyWeakref_GET_OBJECT(item[2]))

        return res
    

cdef class Signal:

    def __cinit__(self):
        self._mgrs = {}
        
        def remove(wr, selfref=PyWeakref_NewRef(self, None)):
            cdef Signal _self = <object>PyWeakref_GET_OBJECT(selfref)
            if _self is not None:
                del _self._mgrs[wr]
        
        self._remove = remove

    cpdef connect(self, notifier, priority=16, context=NoneContext):
        cdef NotifierManager mgr
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, self._remove)
        if wr_context not in mgrs:
            mgr = NotifierManager()
            mgrs[wr_context] = mgr
        else:
            mgr = mgrs[wr_context]
        mgr.add_notifier(notifier, priority)

    cpdef disconnect(self, notifier, context=NoneContext):
        cdef NotifierManager mgr
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, None)
        if wr_context in mgrs:
            mgr = mgrs[wr_context]
            mgr.remove_notifier(notifier)

    cpdef emit(self, Message message, context=NoneContext):
        cdef NotifierManager mgr
        cdef list notifiers
        cdef dict mgrs = self._mgrs
        
        wr_context = PyWeakref_NewRef(context, None)
        if wr_context in mgrs:
            mgr = mgrs[wr_context]
            notifiers = mgr.notifiers()
            if notifiers:
                message.initialize()
                for notifier in notifiers:
                    try:
                        notifier(message, context)
                    except KillSignalException:
                        break
                    finally:
                        message.update()
                message.finalize()

   
