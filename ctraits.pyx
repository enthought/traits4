import sys

from cpython cimport PyObject


cdef extern from "Python.h":
    object PyObject_GenericGetAttr(object, object)
    int PyObject_GenericSetAttr(object, object, object) except -1
    int PyObject_DelAttr(object, object) except -1
    long PyObject_Hash(object)
    int PyString_CheckExact(object)
    
    PyObject** _PyObject_GetDictPtr(PyObject*)

    ctypedef struct PyDictEntry:
        Py_ssize_t me_hash
        PyObject* me_key
        PyObject* me_value

    ctypedef struct PyDictObject:
        PyDictEntry* ma_lookup(PyDictObject*, object, long)

    ctypedef struct PyStringObject:
        long ob_shash


# Forward declarations
cdef class CTrait


#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------
Undefined = object()



#------------------------------------------------------------------------------
# CHasTraits class
#------------------------------------------------------------------------------

cdef class CHasTraits:

    cdef dict obj_dict
    cdef dict itrait_dict

    def __cinit__(self):
        # grab a reference to the object's dict
        # need to call the generic getattr here because 
        # __getattribute__ depends on this dict existing
        self.obj_dict = <dict>PyObject_GenericGetAttr(self, '__dict__')

    def __getattribute__(self, bytes name):
        # short circuit the normal lookup chain if the value
        # is in the obj_dict. This means that delegates cannot 
        # set values in the obj_dict but must return the values 
        # from the delegated object instead (as one would expect).
        cdef PyDictObject* dct = <PyDictObject*>self.obj_dict
        cdef long hash_
        cdef PyObject* value
    
        # This hack is basically just the innards of PyDict_GetItem.
        # The ~25% performance improvement (87ns vs 64ns) comes 
        # from not making the function call to PyDict_GetItem or 
        # first checking to see if the attribute is a data descriptor.
        hash_ = (<PyStringObject*>name).ob_shash
        if hash_ == -1:
            hash_ = PyObject_Hash(name)
        value = dct.ma_lookup(dct, name, hash_).me_value
        if value != NULL:
            return <object>value
    
        # if the object has instance traits, then self.itrait_dict
        # will be a dict instead of None. The instance traits
        # have priority over the class traits, so we need to 
        # manually fire the descriptor in that case. 
        cdef dict itrait_dict = self.itrait_dict

        if itrait_dict is not None:
            if name in itrait_dict:
                value_ = itrait_dict[name]
                return (<CTrait>value_).__c_get__(self, <object>((<PyObject*>self).ob_type))

        # This will properly propagate to the __get__ method
        # if the attribute is a class-level data descriptor.
        return PyObject_GenericGetAttr(self, name)
    
    def __setattr__(self, name, val):
        # if the object has instance traits, then self.itrait_dict
        # will be a dict instead of None. The instance traits
        # have priority over the class traits, so we need to 
        # manually fire the descriptor in that case.
        cdef dict itrait_dict = self.itrait_dict

        if itrait_dict is not None:
            if name in itrait_dict:
                value = itrait_dict[name]
                (<CTrait>value).__c_set__(self, val)
                return 
        
        # This will properly propagate to the __set__
        # method if the attribute is a class-level
        # data descriptor.
        PyObject_GenericSetAttr(self, name, val)

    def __delattr__(self, name):
        # if the object has instance traits, then self.itrait_dict
        # will be a dict instead of None. The instance traits
        # have priority over the class traits, so we need to 
        # manually fire the descriptor in that case.
        cdef dict itrait_dict = self.itrait_dict

        if itrait_dict is not None:
            if name in itrait_dict:
                value = itrait_dict[name]
                (<CTrait>value).__c_del__(self)
                return

        # There is no PyObject_GenericDelAttr, but you can trigger 
        # an equivalent by using the generic setattr with a NULL value.
        # Using PyObject_DelAttr here will cause infinite recursion.
        # This will properly propagate to the __delete__ method if the 
        # attribute is a class-level data descriptor.
        PyObject_GenericSetAttr(self, name, <object>NULL)

    def add_trait(self, bytes name, CTrait trait):
        # We lazily add the itrait dict to save memory and 
        # keep things faster. A None check is a just a pointer
        # comparison in C, so __getattribute__ remains fast 
        # for most objects which don't use instance traits.
        if self.itrait_dict is None:
            self.itrait_dict = {}
        trait._name = name
        self.itrait_dict[name] = trait

        # we need to remove the current value in the obj_dict
        # for the new instance trait, so that the new trait
        # can compute and return its value.
        if name in self.obj_dict:
            del self.obj_dict[name]


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

    cdef bytes _name
    cdef object _notifier
    cdef object py_default_value
    cdef object py_validate

    def __init__(self, default_value=None, validate=None):
        self.py_default_value = default_value
        self.py_validate = validate

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
        # CHasTraits.__getattribute__, but better to play it safe.
        # The usual behavior is that this method computes the default
        # value of the trait and stuffs it in the object's __dict__
        # 
        # This method (along with __c_set__ and __c_del__) will
        # need to be overridden by non-standard traits like delegates.
        cdef dict obj_dict

        name = self._name
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

    cdef inline __c_set__(self, obj, val):
        # C-level implementation of the  `set` descriptor for 
        # fast manual dispatching
        #
        # The semantics here are simple. Validate the new 
        # val. Once validation is complete, retrieve the old
        # value from the object's __dict__ or Undefined if not
        # present. Stuff the new value in the dict and call
        # the notifier.
        cdef dict obj_dict = (<CHasTraits>obj).obj_dict
        name = self._name
        new = self._validate(obj, name, val)
        if name in obj_dict:
            old = obj_dict[name]
        else:
            old = Undefined
        obj_dict[name] = new
        self.notify(obj, name, old, new)

    cdef inline __c_del__(self, obj):
        # C-level implementation of the  `del` descriptor for 
        # fast manual dispatching. 
        #
        # The semantics for del foo.a where 'a' is a trait attribute
        # is actually to just reset to the default value of the
        # trait, then call the notifier.
        cdef dict obj_dict = (<CHasTraits>obj).obj_dict
        name = self._name
        if name in obj_dict:
            old = obj_dict[name]
        else:
            old = Undefined
        new = self._validate(obj, name, self._default_value(obj, name))
        obj_dict[name] = new
        self.notify(obj, name, old, new)

    property name:
        
        def __get__(self):
            return self._name

        def __set__(self, bytes val):
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


cdef class CAny(CTrait):

    cdef inline default_value(self, obj, name):
        return None

    cdef inline validate(self, obj, name, val):
        return val

