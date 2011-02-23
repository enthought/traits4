

cdef class _Trait:
    cdef bytes py_name
    cdef object py_dispatcher
    cdef object py_default_value
    cdef object py_validator

    cdef inline __c_get__(self, object, object)

    cdef inline __c_set__(self, object, object)

    cdef inline __c_del__(self, object)
