from weakref import ref


class WeakMethod(object):
    """ Creates a callable object which weakly wraps a bound
    method. An internal reference to each instance in kept until
    the wrapped object dies. Thus, the WeakMethod instance is also
    weakly referenceable for the lifetime of the wrapped object. 

    """
    _instances = set()

    def __init__(self, bound_method):

        def remove(wr, selfref=ref(self)):
            self = selfref()
            if self is not None:
                self._instances.remove(self)

        self._remove = remove
        self._func = bound_method.im_func
        self._obj = ref(bound_method.im_self, self._remove)

        self._instances.add(self)

    def __call__(self, *args, **kwargs):
        obj = self._obj()
        if obj is not None:
            return self._func(obj, *args, **kwargs)

