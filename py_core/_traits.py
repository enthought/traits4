

Undefined = object()


class ValidationError(Exception):
    pass


def validation_error(obj, name, val, type_):
    msg = ('The `%s` trait of a `%s` object must be of type `%s` '
           'but a value of type `%s` was received.'
           % (name, obj.__class__.__name__, type_.__name__, 
              type(val).__name__))
    raise ValidationError(msg)


class _Trait:

    def __init__(self, default_value=None, validator=None, dispatcher=None):
        self.py_default_value = default_value
        self.py_validator = validator
        self.py_dispatcher = dispatcher
        self.name = ''

    def __get__(self, obj, cls):
        cdef dict obj_dict

        name = self.py_name
        if obj is None:
            raise AttributeError('type object `%s` has no attribute `%s`'
                                 % (cls.__name__, name))
        
        obj_dict = (<CHasTraits>obj).obj_dict
        if name in obj_dict:
            res = obj_dict[name]
        else:
            res = self._validate(obj, name, self._default_value(obj, name))
            obj_dict[name] = res
        
        return res

    def __set__(self, obj, val):
        cdef dict obj_dict = (<CHasTraits>obj).obj_dict
        name = self.py_name
        new = self._validate(obj, name, val)
        if name in obj_dict:
            old = obj_dict[name]
        else:
            old = self._default_value(obj, name)
        obj_dict[name] = new
        self._dispatch(obj, name, old, new)

    def __del__(self, obj):
        cdef dict obj_dict = (<CHasTraits>obj).obj_dict
        name = self.py_name
        if name in obj_dict:
            old = obj_dict[name]
        else:
            # already have the default value, no need to do more
            return
        new = self._validate(obj, name, self._default_value(obj, name))
        obj_dict[name] = new
        self._dispatch(obj, name, old, new)
    
    def _default_value(self, obj, name):
        if self.py_default_value is not None:
            return self.py_default_value(obj, name)
        return self.c_default_value(obj, name)

    def _validate(self, obj, name, val):
        if self.py_validator is not None:
            return self.py_validator(obj, name, val)
        return self.c_validate(obj, name, val)
    
    def _dispatch(self, obj, name, old, new):
        if self.py_dispatcher is not None:
            return self.py_dispatcher(self, obj, name, old, new)
        return self.c_dispatch(self, obj, name, old, new)

    def default_value(self, obj, name):
        raise NotImplementedError

    def validate(self, obj, name, val):
        raise NotImplementedError

    def dispatch(self, trait, obj, name, old, new):
        raise NotImplementedError


class CInt(CTrait):

    cdef inline c_default_value(self, obj, name):
        return 0

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, int):
            return val
        validation_error(obj, name, val, int)


class CFloat(CTrait):

    cdef inline c_default_value(self, obj, name):
        return 0.0

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, float):
            return val
        validation_error(obj, name, val, float)


class CLong(CTrait):

    cdef inline c_default_value(self, obj, name):
        return 0L

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, long):
            return val
        validation_error(obj, name, val, long)


class CStr(CTrait):

    cdef inline c_default_value(self, obj, name):
        return ''

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, basestring):
            return val
        validation_error(obj, name, val, basestring)


class CList(CTrait):

    cdef inline c_default_value(self, obj, name):
        return []

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, list):
            return val
        validation_error(obj, name, val, list)


class CTuple(CTrait):

    cdef inline c_default_value(self, obj, name):
        return ()

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, tuple):
            return val
        validation_error(obj, name, val, tuple)


class CDict(CTrait):

    cdef inline c_default_value(self, obj, name):
        return {}

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, dict):
            return val
        validation_error(obj, name, val, dict)


cdef class CAny(CTrait):

    cdef inline c_default_value(self, obj, name):
        return None

    cdef inline c_validate(self, obj, name, val):
        return val

