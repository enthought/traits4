

Undefined = object()


class ValidationError(Exception):
    pass


cdef validation_error(obj, name, val, type_):
    msg = ('The `%s` trait of a `%s` object must be of type `%s` '
           'but a value of type `%s` was received.'
           % (name, obj.__class__.__name__, type_.__name__, 
              type(val).__name__))
    raise ValidationError(msg)


cdef class _Trait:

    def __init__(self, default_value=None, validator=None, dispatcher=None):
        self.py_default_value = default_value
        self.py_validator = validator
        self.py_dispatcher = dispatcher

    def __get__(self, obj, cls):
        return self.__c_get__(obj, cls)

    def __set__(self, obj, val):
        self.__c_set__(obj, val)

    def __delete__(self, obj):
        self.__c_del__(obj)

    cdef inline __c_get__(self, obj, cls):
        # C-level implementation of the `get` descriptor for fast
        # manual dispatching
        #
        # If obj is None, then the descriptor was called via 
        # attribute access on the class. In that case the behavior
        # is undefined and we raise an AttributeError (same behavior
        # as current traits)
        #
        # Otherwise, we check to see if the value is in the object's
        # __dict__. This is a bit of a redundant check because if it's
        # True, then the value would have already been returned in
        # _HasTraits.__getattribute__, but better to play it safe.
        # The usual behavior is that this method computes the default
        # value of the trait and stuffs it in the object's __dict__
        # 
        # This method (along with __c_set__ and __c_del__) will
        # need to be overridden by non-standard traits like delegates.
        cdef dict obj_dict

        name = self.py_name
        if obj is None:
            raise AttributeError('type object `%s` has no attribute `%s`'
                                 % (cls.__name__, name))
        
        obj_dict = (<_HasTraits>obj).obj_dict
        if name in obj_dict:
            res = obj_dict[name]
        else:
            res = self._validate(obj, name, self._default_value(obj, name))
            obj_dict[name] = res
        
        return res

    cdef inline __c_set__(self, obj, val):
        # C-level implementation of the  `set` descriptor for 
        # fast manual dispatching
        #
        # The semantics here are simple. Validate the new 
        # val. Once validation is complete, retrieve the old
        # value from the object's __dict__ or the default if not
        # present. Stuff the new value in the dict and call
        # the notifier.
        cdef dict obj_dict = (<_HasTraits>obj).obj_dict
        name = self.py_name
        new = self._validate(obj, name, val)
        if name in obj_dict:
            old = obj_dict[name]
        else:
            old = self._default_value(obj, name)
        obj_dict[name] = new
        self._dispatch(obj, name, old, new)

    cdef inline __c_del__(self, obj):
        # C-level implementation of the  `del` descriptor for 
        # fast manual dispatching. 
        #
        # The semantics for del foo.a where 'a' is a trait attribute
        # is actually to just reset to the default value of the
        # trait, then call the notifier.
        cdef dict obj_dict = (<_HasTraits>obj).obj_dict
        name = self.py_name
        if name in obj_dict:
            old = obj_dict[name]
        else:
            # already have the default value, no need to do more
            return
        new = self._validate(obj, name, self._default_value(obj, name))
        obj_dict[name] = new
        self._dispatch(obj, name, old, new)

    property name:
        
        def __get__(self):
            return self.py_name

        def __set__(self, bytes val):
            self.py_name = val
   
    property dispatcher:
        
        def __get__(self):
            return self.py_dispatcher

        def __set__(self, val):
            self.py_dispatcher = val

    property default_value:

        def __get__(self):
            return self.py_default_value

        def __set__(self, val):
            self.py_default_value = val

    property validator:

        def __get__(self):
            return self.py_validator

        def __set__(self, val):
            self.py_validator = val

    cdef inline _default_value(self, obj, name):
        if self.py_default_value is not None:
            return self.py_default_value(obj, name)
        return self.c_default_value(obj, name)

    cdef inline _validate(self, obj, name, val):
        if self.py_validator is not None:
            return self.py_validator(obj, name, val)
        return self.c_validate(obj, name, val)
    
    cdef inline _dispatch(self, obj, name, old, new):
        if self.py_dispatcher is not None:
            return self.py_dispatcher(self, obj, name, old, new)
        return self.c_dispatch(self, obj, name, old, new)

    cdef inline c_default_value(self, obj, name):
        raise NotImplementedError

    cdef inline c_validate(self, obj, name, val):
        raise NotImplementedError

    cdef inline c_dispatch(self, trait, obj, name, old, new):
        raise NotImplementedError


cdef class _Int(_Trait):

    cdef inline c_default_value(self, obj, name):
        return 0

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, int):
            return val
        validation_error(obj, name, val, int)


cdef class _Float(_Trait):

    cdef inline c_default_value(self, obj, name):
        return 0.0

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, float):
            return val
        validation_error(obj, name, val, float)


cdef class _Long(_Trait):

    cdef inline c_default_value(self, obj, name):
        return 0L

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, long):
            return val
        validation_error(obj, name, val, long)


cdef class _Str(_Trait):

    cdef inline c_default_value(self, obj, name):
        return ''

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, basestring):
            return val
        validation_error(obj, name, val, basestring)


cdef class _List(_Trait):

    cdef inline c_default_value(self, obj, name):
        return []

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, list):
            return val
        validation_error(obj, name, val, list)


cdef class _Tuple(_Trait):

    cdef inline c_default_value(self, obj, name):
        return ()

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, tuple):
            return val
        validation_error(obj, name, val, tuple)


cdef class _Dict(_Trait):

    cdef inline c_default_value(self, obj, name):
        return {}

    cdef inline c_validate(self, obj, name, val):
        if isinstance(val, dict):
            return val
        validation_error(obj, name, val, dict)


cdef class _Any(_Trait):

    cdef inline c_default_value(self, obj, name):
        return None

    cdef inline c_validate(self, obj, name, val):
        return val

