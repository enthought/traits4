

cdef class Foo:
    cdef public dict d
    cdef public list l
    cdef public object o
    cdef public unicode u

    def __cinit__(self):
        print '__cinit__'
        return
    
    def __init__(self):
        """ Constructor. """

        print '__init__'

        self.d = {}
        self.l = []
        self.o = None
        self.u = u''

        return
    
#### EOF ######################################################################
