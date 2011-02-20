

cdef class Signal:
    
    cdef list _heap
    cdef unsigned long _conn_count

    cpdef connect(self, object, int priority=*)

    cpdef disconnect(self, object)

    cpdef emit(self, object)

