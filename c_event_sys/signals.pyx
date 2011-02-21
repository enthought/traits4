# pxd imports
from cpython.weakref cimport PyWeakref_NewRef, PyWeakref_GET_OBJECT
from messages cimport Message

# stdlib imports
from heapq import heapify, heappush, nsmallest


class KillSignalException(Exception):
    pass


cdef class Signal:

    def __cinit__(self):
        self._heap = []
        self._conn_count = 0

    cpdef connect(self, notifier, int priority=16):
        cdef long count = self._conn_count
        cdef list heap = self._heap
        heappush(heap, (priority, count, PyWeakref_NewRef(notifier, None)))
        self._conn_count = count + 1

    cpdef disconnect(self, notifier):
        cdef tuple item
        cdef int i
        cdef list remove_indices = []
        cdef list heap = self._heap

        wr_notifier = PyWeakref_NewRef(notifier, None)

        for i, item in enumerate(heap):
            if item[2] is wr_notifier:
                remove_indices.append(i)
        
        remove_indices.reverse()
        for i in remove_indices:
            heap.pop(i)

    cpdef emit(self, Message message):
        cdef list notifiers
        cdef list heap = self._heap
        cdef tuple item

        notifiers = nsmallest(len(heap), heap)

        message.initialize()

        for item in notifiers:
            notifier = <object>PyWeakref_GET_OBJECT(item[2])
            if notifier is None:
                heap.remove(item)
            else:
                try:
                    notifier(message)
                except KillSignalException:
                    break
                finally:
                    message.update()
        
        message.finalize()

    property heap:

        def __get__(self):
            return self._heap

        def __set__(self, list val):
            self._heap = heapify(val)

    property conn_count:

        def __get__(self):
            return self._conn_count

        def __set__(self, unsigned long val):
            self._conn_count = val

