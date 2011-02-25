from meta_has_traits import MetaHasTraits


VERSION = 'Cython'


class HasTraits(object):
    """ The base class for all classes that have traits! """

    __metaclass__ = MetaHasTraits


class TraitError(Exception):
    pass


cdef class TraitType:
    #### 'TraitType' protocol #################################################

    # The name of the attribbute that the trait is 'bound' to. This is
    # set during class instantiation time due to the poor design of the
    # descriptor protocol.
    cdef public bytes name

    cpdef validate(TraitType self, object value):
        """ Validate the given value.

        Raise a TraitError if the value is not valid for this type.

        """
        
        raise NotImplemented

    #### 'Descriptor' protocol ################################################

    def __get__(self, obj, cls):
        """ Get the value of the descriptor. """

        return obj.__dict__[self.name]
    
    def __set__(self, obj, value):
        """ Set the value of the descriptor. """

        actual_value = self.validate(value)

        obj.__dict__[self.name] = actual_value

        return


cdef class Int(TraitType):
    #### 'TraitType' protocol #################################################

    cpdef inline validate(Int self, object value):
        if not type(value) is int:
            raise TraitError

        return value

#### EOF ######################################################################
