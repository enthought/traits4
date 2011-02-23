# pxd imports
from messages cimport Message


cdef class Signal:
    
    cdef list _heap
    cdef list _notifiers
    cdef unsigned long _conn_count

    cdef inline _heap_changed(self)

    cpdef connect(self, object, object priority=*)

    cpdef disconnect(self, object)

    cpdef emit(self, Message)

