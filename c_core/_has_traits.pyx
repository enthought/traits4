# pxd imports
from cpython cimport PyObject
from _trait_types cimport _Trait

# traits imports
from _trait_types import _Trait


cdef class _HasTraits:

    def __cinit__(self):
        # grab a reference to the object's dict
        # need to call the generic getattr here because 
        # __getattribute__ depends on this dict existing
        self.obj_dict = <dict>PyObject_GenericGetAttr(self, '__dict__')
        self.itrait_dict = None

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
                return (<_Trait>value_).__c_get__(self, <object>((<PyObject*>self).ob_type))

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
                (<_Trait>value).__c_set__(self, val)
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
                (<_Trait>value).__c_del__(self)
                return

        # There is no PyObject_GenericDelAttr, but you can trigger 
        # an equivalent by using the generic setattr with a NULL value.
        # Using PyObject_DelAttr here will cause infinite recursion.
        # This will properly propagate to the __delete__ method if the 
        # attribute is a class-level data descriptor.
        PyObject_GenericDelAttr(self, name, NULL)

    def add_trait(self, bytes name, _Trait trait):
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

    def get_trait(self, bytes name):
        if self.itrait_dict is not None:
            if name in self.itrait_dict:
                return self.itrait_dict[name]

        if name in self.__class__.__dict__:
            trait = self.__class__.__dict__[name]
            if isinstance(trait, _Trait):
                return trait

        raise ValueError('Object has no trait named %s' % name)


