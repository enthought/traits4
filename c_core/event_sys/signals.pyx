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
        self._notifiers = []        

    cdef inline _heap_changed(self):
        # keeps the list of notifiers in sorted sync
        # with the heap
        cdef list heap = self._heap
        self._notifiers = nsmallest(len(heap), heap)

    cpdef connect(self, notifier, priority=16):
        cdef long count = self._conn_count
        cdef list heap = self._heap
        heappush(heap, (priority, count, PyWeakref_NewRef(notifier, None)))
        self._conn_count = count + 1

        self._heap_changed()

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

        self._heap_changed()

    cpdef emit(self, Message message):
        cdef list notifiers
        cdef list heap = self._heap
        cdef tuple item
        cdef bint heap_changed = False

        message.initialize()

        for item in self._notifiers:
            notifier = <object>PyWeakref_GET_OBJECT(item[2])
            if notifier is None:
                heap.remove(item)
                heap_changed = True
            else:
                try:
                    notifier(message)
                except KillSignalException:
                    break
                finally:
                    message.update()
        
        message.finalize()

        if heap_changed:
            self._heap_changed()

    # Even though these are exposed, you probably shouldn't mess
    # with them. They are exposed so they can be used by subclasses.

    property heap:

        def __get__(self):
            return self._heap

        def __set__(self, list val):
            self._heap = heapify(val)
            self._heap_changed()

    property notifiers:

        def __get__(self):
            return self._notifiers

        def __set__(self, list val):
            self._notifiers = val

    property conn_count:

        def __get__(self):
            return self._conn_count

        def __set__(self, unsigned long val):
            self._conn_count = val

