from cpython cimport PyObject


cdef extern from "Python.h":
    object PyObject_GenericGetAttr(object, object)
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


#------------------------------------------------------------------------------
# CHasTraits class
#------------------------------------------------------------------------------

cdef class CHasTraits:

    cdef dict obj_dict

    def __cinit__(self):
        # grab a reference to the object's dict
        # need to call the generic getattr here because 
        # __getattribute__ depends on this dict existing
        self.obj_dict = <dict>PyObject_GenericGetAttr(self, '__dict__')

    def __getattribute__(self, name):
        # short circuit the normal lookup chain if the value
        # is in the obj_dict. This means that 
        # delegates cannot set values in the obj_dict
        # but must return the values from the delegated object
        # instead (as one would expect).
        cdef PyDictObject* obj_dict = <PyDictObject*>self.obj_dict
        cdef long hash_
        cdef PyObject* value

        # This hack is basically just the innards of PyDict_GetItem.
        # The saving is in not making the function call.
        if PyString_CheckExact(name):
            hash_ = (<PyStringObject*>name).ob_shash
            if hash_ == -1:
                hash_ = PyObject_Hash(name)
            value = obj_dict.ma_lookup(obj_dict, name, hash_).me_value
            if value != NULL:
                return <object>value

        # we don't really need the rest of the original traits
        # performance hack. This generic getattr will handle the
        # edge cases it was handling.
        return PyObject_GenericGetAttr(self, name)


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
        cdef dict obj_dict
        name = self._name

        if obj is None:
            raise AttributeError('type object `%s` has no attribute `%s`'
                                 % (cls.__name__, name))
        else:
            obj_dict = (<CHasTraits>obj).obj_dict
            try:
                res = obj_dict[name]
            except KeyError:
                res = self._validate(obj, name, self._default_value(obj, name))
                obj_dict[name] = res
        
        return res

    def __set__(self, obj, val):
        cdef dict obj_dict = (<CHasTraits>obj).obj_dict
        name = self._name
        new = self._validate(obj, name, val)
        old = obj_dict[name]
        obj_dict[name] = new
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


cdef class CAny(CTrait):

    cdef inline default_value(self, obj, name):
        return None

    cdef inline validate(self, obj, name, val):
        return val

