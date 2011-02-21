# pxd imports
from messages cimport Message
from signals cimport Signal


cdef class Dispatcher:

    cpdef dispatch(self, Signal, Message)


cdef class QueueDispatcher(Dispatcher):

    cdef object _queue
    cdef bint _working

    cpdef dispatch(self, Signal, Message)


cdef class StackDispatcher(Dispatcher):

    cdef list _stack
    cdef bint _working

    cpdef dispatch(self, Signal, Message)
