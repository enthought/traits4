

cdef extern from "Python.h":
    object PyObject_GenericGetAttr(object, object)
    int PyObject_GenericSetAttr(object, object, object) except -1
    long PyObject_Hash(object)

    # generic delattr doesnt really exist. This alias is to make Cython
    # refcounts work properly so NULL is decref'd
    int PyObject_GenericDelAttr "PyObject_GenericSetAttr" (object, object, PyObject*) except -1

    ctypedef struct PyDictEntry:
        Py_ssize_t me_hash
        PyObject* me_key
        PyObject* me_value

    ctypedef struct PyDictObject:
        PyDictEntry* ma_lookup(PyDictObject*, object, long)

    ctypedef struct PyStringObject:
        long ob_shash


cdef class _HasTraits:

    cdef dict obj_dict
    cdef dict itrait_dict
