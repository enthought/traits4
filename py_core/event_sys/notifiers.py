from weakref import ref, WeakKeyDictionary

      
class weak_method(object):
    """ Creates a weak reference to bound method.

    This class works around the typical issue of taking a weakref to 
    a bound method, which is that the bound method will be immediately
    collected if it has no other strong refs (often the case). 

    Calling a weak_method is semantically equivalent to calling the method
    itself. 

    Calling weak_method(...) multiple times with the same *equivalent*
    bound method will return the same weak_method object. Thus, the 
    following behavior is supported:

    class Foo(object):
        
        def bar(self):
            pass

    >>> f = Foo()
    >>> weak_method(f.bar) is weak_method(f.bar)
    True

    A strong reference to each weak_method is maintained for the lifetime
    of the object. Thus, weak_methods themselves may be weakref'd and the
    client need not be concerned with keeping a strong ref to the 
    weak_method.

    """
    _weak_cache = WeakKeyDictionary()

    def __new__(cls, bound_method):
        obj = bound_method.im_self
        func = bound_method.im_func

        obj_cache = cls._weak_cache
        if obj in obj_cache:
            func_cache = obj_cache[obj]
        else:
            func_cache = {}
            obj_cache[obj] = func_cache

        if func in func_cache:
            res = func_cache[func]
        else:
            res = object.__new__(cls, bound_method)
            func_cache[func] = res

        return res

    def __init__(self, bound_method):
        self._func = bound_method.im_func
        self._obj = ref(bound_method.im_self)

    def __call__(self, *args, **kwargs):
        obj = self._obj()
        if obj is not None:
            return self._func(obj, *args, **kwargs)


