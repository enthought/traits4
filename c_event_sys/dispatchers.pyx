# pxd imports
from messages cimport Message
from signals cimport Signal

# stdlib imports
from collections import deque


cdef class QueueDispatcher:

    def __cinit__(self):
        self._queue = deque() # XXX - use the cgraph.c_collections Queue
        self._working = False

    cpdef dispatch(self, Signal signal, Message message):
        cdef Signal op_signal
        cdef Message op_message

        queue = self._queue
        queue.append((signal, message))
        
        if self._working:
            return 
        
        self._working = True
        
        while queue:
            item = queue.popleft()
            op_signal = <Signal>item[0]
            op_message = <Message>item[1]
            op_signal.emit(op_message)

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

