from meta_has_traits import MetaHasTraits

from cpython cimport PyObject


cdef extern from "Python.h":
    object PyObject_GenericGetAttr(object, object)
    # XXX - By declaring PyObject*, nothing gets incref'd. This *may*
    # be a problem, but doesn't seem to be so far. Can't declare as
    # object or then <object>NULL gets increfd and segfaults.
    int PyObject_GenericSetAttr(PyObject*, PyObject*, PyObject*) except -1
    int PyObject_DelAttr(object, object) except -1
    long PyObject_Hash(object)

    ctypedef struct PyDictEntry:
        Py_ssize_t me_hash
        PyObject* me_key
        PyObject* me_value

    ctypedef struct PyDictObject:
        PyDictEntry* ma_lookup(PyDictObject*, object, long)

    ctypedef struct PyStringObject:
        long ob_shash




VERSION = 'Cython with getattr'

# If the implementation hooks the 'getattr' mechanism, then
# we need to remove the trait type from the class dictionary.
hooks_getattr = True


cdef class CHasTraits:
    """ The base class for all classes that have traits! """

    cdef dict obj_dict
    cdef dict itrait_dict
    cdef dict traits
    
    def __cinit__(self):
        # grab a reference to the object's dict
        # need to call the generic getattr here because 
        # __getattribute__ depends on this dict existing
        self.obj_dict = <dict>PyObject_GenericGetAttr(self, '__dict__')
        self.traits = <dict>PyObject_GenericGetAttr(self, '__traits__')

    def __getattribute__(self, bytes name):
        # short circuit the normal lookup chain if the value
        # is in the obj_dict. This means that delegates cannot 
        # set values in the obj_dict but must return the values 
        # from the delegated object instead (as one would expect).
        cdef PyDictObject* dct = <PyDictObject*>self.obj_dict
        cdef long hash_
        cdef PyObject* value
        cdef PyDictObject* traits = <PyDictObject*>self.traits
    
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

        # fixme: Here we need to see if there is a trait type with this name
        # and if so use it to get the default value...
        value = traits.ma_lookup(traits, name, hash_).me_value
        if value != NULL:
            print 'Get the default value!'
            return 42
    
        # This will properly propagate to the __get__ method
        # if the attribute is a class-level data descriptor.
        return PyObject_GenericGetAttr(self, name)

    def __getattrXXXXXX__(self, name):
        """ Gets the value of an attribute on the object. """

        trait_type = self.__traits__[name]
            
        # If the object has a trait with the specified name then use the
        # corresponding trait type to get the value.
        if trait_type is not None:
            value = trait_type.get_default_value(self, name)
            
        # Otherwise, this is just a regular Python attribute so let Python do
        # its thang (this will actually just raise an 'AttributeError' since
        # Python only calls '__getattr__' when it can't find an attribute).
        else:
            # fixme: It seems a little wierd to me but the 'object' type
            # doesn't have a '__getattr__' method. However, it *does* have
            # '__setattr__', '__delattr__' and '__getattribute__'.
            value = object.__getattribute__(self, name)

        return value

    def __setattr__(self, name, value):
        """ Sets the value of an attribute on the object. """

        cdef PyDictObject* traits = <PyDictObject*>self.traits
        cdef PyObject* trait_type
        
        hash_ = (<PyStringObject*>name).ob_shash
        if hash_ == -1:
            hash_ = PyObject_Hash(name)
        trait_type = traits.ma_lookup(traits, name, hash_).me_value
        if trait_type != NULL:
            #print '-------------', trait_type
            self.obj_dict[name] = (<TraitType>trait_type).validate(value)

        else:
            # This will properly propagate to the __set__
            # method if the attribute is a class-level
            # data descriptor.
            PyObject_GenericSetAttr(
                <PyObject*>self, <PyObject*>name, <PyObject*>value
            )

##         trait_type = self.__traits__.get(name, None)
        
##         # If the object has a trait with the specified name then use the
##         # corresponding trait type to set the value.
##         if trait_type is not None:
##             self.__dict__[name] = trait_type.validate(value)

##         # Otherwise, this is just a regular Python attribute so let Python do
##         # its thang.
##         else:
##             #object.__setattr__(self, name, value)

            
        return


class HasTraits(CHasTraits):
    __metaclass__ = MetaHasTraits

    
class TraitError(Exception):
    pass


cdef class TraitType:
    #### 'TraitType' protocol #################################################

    # The name of the attribbute that the trait is 'bound' to. This is
    # set during class instantiation time due to the poor design of the
    # descriptor protocol.
    cdef public bytes name

    cpdef inline validate(TraitType self, object value):
        """ Validate the given value.

        Raise a TraitError if the value is not valid for this type.

        """
        
        raise NotImplemented


cdef class Int(TraitType):
    #### 'TraitType' protocol #################################################

    cpdef inline validate(Int self, object value):
        if not type(value) is int:
            raise TraitError

        return value

#### EOF ######################################################################
