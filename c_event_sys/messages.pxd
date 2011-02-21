

cdef class Message:
    
    cdef object _contents

    cpdef initialize(self)

    cpdef update(self)

    cpdef finalize(self)


