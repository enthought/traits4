# pxd imports
from signal cimport Signal

# stdlib imports
from collections import deque


cdef class QueueDispatcher:

    def __cinit__(self):
        self._queue = deque() # XXX - use the cgraph.c_collections Queue
        self._working = False

    cpdef dispatch(self, Signal signal, message):
        cdef Signal op_signal
        
        queue = self._queue
        queue.append((signal, message))
        
        if self._working:
            return 
        
        self._working = True
        
        while queue:
            item = queue.popleft()
            op_signal = <Signal>item[0]
            messgae = item[1]
            op_signal.emit(message)

        self._working = False
    
    property queue:

        def __get__(self):
            return self._queue

        def __set__(self, val):
            self._queue = val

    property working:

        def __get__(self):
            return self._working

        def __set__(self, bint val):
            self._working = val

