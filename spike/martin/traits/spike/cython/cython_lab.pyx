

cdef class Foo:
    cdef public dict stuff
    cdef public list l
    
    def __init__(self):
        print 'Constructor!!!!'
        self.stuff = {}

#### EOF ######################################################################
