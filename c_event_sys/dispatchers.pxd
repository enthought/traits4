# pxd imports
from messages cimport Message
from signals cimport Signal


cdef class QueueDispatcher:

    cdef object _queue
    cdef bint _working

    cpdef dispatch(self, Signal, Message)
