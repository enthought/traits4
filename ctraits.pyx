

#------------------------------------------------------------------------------
# CHasTraits class
#------------------------------------------------------------------------------

cdef class CHasTraits(object):

    cdef dict trait_dict

    def __cinit__(self):
        self.trait_dict = {}


#------------------------------------------------------------------------------
# cTrait Types
#------------------------------------------------------------------------------
class ValidationError(Exception):
    pass


cdef validation_error(obj, name, val, type_):
    msg = ('The `%s` trait of a `%s` object must be of type `%s` '
           'but a value of type `%s` was received.'
           % (name, obj.__class__.__name__, type_.__name__, 
              type(val).__name__))
    raise ValidationError(msg)


cdef class CTrait:

    cdef str _name
    cdef object _notifier
    cdef object py_default_value
    cdef object py_validate

    def __init__(self, default_value=None, validate=None):
        self.py_default_value = default_value
        self.py_validate = validate

    def __get__(self, obj, cls):
        cdef dict trait_dict
        name = self._name

        if obj is None:
            raise AttributeError('type object `%s` has no attribute `%s`'
                                 % (cls.__name__, name))
        else:
            trait_dict = (<CHasTraits>obj).trait_dict
            try:
                res = trait_dict[name]
            except KeyError:
                res = self._validate(obj, name, self._default_value(obj, name))
                trait_dict[name] = res
        
        return res

    def __set__(self, obj, val):
        cdef dict trait_dict = (<CHasTraits>obj).trait_dict
        name = self._name
        new = self._validate(obj, name, val)
        old = trait_dict[name]
        trait_dict[name] = new
        self.notify(obj, name, old, new)

    property name:
        
        def __get__(self):
            return self._name

        def __set__(self, str val):
            self._name = val
   
    property notifier:
        
        def __get__(self):
            return self._notifier

        def __set__(self, val):
            self._notifier = val

    cdef inline _default_value(self, obj, name):
        if self.py_default_value is not None:
            return self.py_default_value(obj, name)
        return self.default_value(obj, name)

    cdef inline _validate(self, obj, name, val):
        if self.py_validate is not None:
            return self.py_validate(obj, name, val)
        return self.validate(obj, name, val)

    cdef inline default_value(self, obj, name):
        raise NotImplementedError

    cdef inline validate(self, obj, name, val):
        raise NotImplementedError

    cdef inline void notify(self, obj, name, old, new):
        if self._notifier is not None:
            self._notifier(self, obj, name, old, new)


cdef class CInt(CTrait):

    cdef inline default_value(self, obj, name):
        return 0

    cdef inline validate(self, obj, name, val):
        if isinstance(val, int):
            return val
        validation_error(obj, name, val, int)


cdef class CFloat(CTrait):

    cdef inline default_value(self, obj, name):
        return 0.0

    cdef inline validate(self, obj, name, val):
        if isinstance(val, float):
            return val
        validation_error(obj, name, val, float)


cdef class CLong(CTrait):

    cdef inline default_value(self, obj, name):
        return 0L

    cdef inline validate(self, obj, name, val):
        if isinstance(val, long):
            return val
        validation_error(obj, name, val, long)


cdef class CStr(CTrait):

    cdef inline default_value(self, obj, name):
        return ''

    cdef inline validate(self, obj, name, val):
        if isinstance(val, basestring):
            return val
        validation_error(obj, name, val, basestring)


cdef class CList(CTrait):

    cdef inline default_value(self, obj, name):
        return []

    cdef inline validate(self, obj, name, val):
        if isinstance(val, list):
            return val
        validation_error(obj, name, val, list)


cdef class CTuple(CTrait):

    cdef inline default_value(self, obj, name):
        return ()

    cdef inline validate(self, obj, name, val):
        if isinstance(val, tuple):
            return val
        validation_error(obj, name, val, tuple)


cdef class CDict(CTrait):

    cdef inline default_value(self, obj, name):
        return {}

    cdef inline validate(self, obj, name, val):
        if isinstance(val, dict):
            return val
        validation_error(obj, name, val, dict)



