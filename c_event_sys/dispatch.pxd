# pxd imports
from signal cimport Signal


cdef class QueueDispatcher:

    cdef object _queue
    cdef bint _working

    cpdef dispatch(self, Signal, object)
