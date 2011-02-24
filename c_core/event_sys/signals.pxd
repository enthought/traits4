# pxd imports
from messages cimport Message


cdef class NotifierManager:
    
    cdef unsigned long _conn_count
    cdef list _notifiers
    
    cdef _c_dead_notifier(self, object)

    cpdef add_notifier(self, object, object)

    cpdef remove_notifier(self, object)

    cpdef notifiers(self)


cdef class Signal:
    
    cdef dict _mgrs

    cpdef connect(self, object, object priority=*, object context=*)

    cpdef disconnect(self, object, object context=*)

    cpdef emit(self, Message, object context=*)

