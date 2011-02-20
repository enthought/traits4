from weakref import ref


VALID_ARG_NAMES = set(('obj', 'name', 'old', 'new'))


class FunctionNotifier(object):
    
    __slots__ = ('func_ref', 'arg_names')

    def __init__(self, func):
        self.func_ref = ref(func)
           
        arg_names = func.func_code.co_varnames
        for name in arg_names:
            if name not in VALID_ARG_NAMES:
                raise TypeError('Handler `%s` has invalid argument `%s`'
                                % (func, name))

        self.arg_names = tuple(arg_names)

    def __call__(self, **kwargs):
        func = self.func_ref()
        if func is None:
            return False
        call_kwargs = {}
        for name in self.arg_names:
            call_kwargs[name] = kwargs[name]
        func(**call_kwargs)
        return True


class BoundMethodNotifier(object):

    __slots__ = ('self_ref', 'func_ref', 'arg_names')

    def __init__(self, method):
        self.func_ref = ref(method.im_func)
        self.self_ref = ref(method.im_self)

        arg_names = method.im_func.func_code.co_varnames[1:]
        for name in arg_names:
            if name not in VALID_ARG_NAMES:
                raise TypeError('Handler `%s` has invalid argument `%s`'
                                % (method, name))

        self.arg_names = tuple(arg_names)

    def __call__(self, **kwargs):
        func = self.func_ref()
        if func is None:
            return False
        other_self = self.self_ref()
        if other_self is None:
            return False
        call_kwargs = {}
        for name in self.arg_names:
            call_kwargs[name] = kwargs[name]
        func(other_self, **call_kwargs)
        return True
        

