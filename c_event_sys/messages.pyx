

cdef class Message:

    def __init__(self, contents=None):
        self._contents = contents

    cpdef initialize(self):
        pass

    cpdef update(self):
        pass

    cpdef finalize(self):
        pass

    property contents:

        def __get__(self):
            return self._contents

        def __set__(self, val):
            self._contents = val

    def __repr__(self):
        return 'Message: %s' % self._contents

    def __str__(self):
        return self.__repr__()

   
