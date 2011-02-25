# pxd imports
from messages cimport Message


cdef class NotifierManager:
    
    cdef object __weakref__
    cdef unsigned long _conn_count
    cdef list _notifiers
    cdef object _remove
   
    cdef _c_remove(self, object)

    cpdef add_notifier(self, object, object)

    cpdef remove_notifier(self, object)

    cpdef notifiers(self)


cdef class Signal:
    
    cdef object __weakref__
    cdef dict _mgrs
    cdef object _remove

    cpdef connect(self, object, object priority=*, object context=*)

    cpdef disconnect(self, object, object context=*)

    cpdef emit(self, Message, object context=*)

