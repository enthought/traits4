from weakref import ref, WeakKeyDictionary


VALID_ARG_NAMES = {'obj', 'name', 'old', 'new'}


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
        call_kwargs = {name: kwargs[name] for name in self.arg_names}
        func(**call_kwargs)
        return True


class BoundMethodNotifier(object):

    __slots__ = ('obj_ref', 'func_ref', 'arg_names')

    def __init__(self, method):
        self.func_ref = ref(method.im_func)
        self.self_ref = ref(method.im_self)

        arg_names = method.im_func.func_code.co_varnames[1:]
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
        other_self = self.self_ref()
        if other_self is None:
            return False
        call_kwargs = {name: kwargs[name] for name in self.arg_names}
        func(other_self, **call_kwargs)
        return True
        

class Dispatcher(object):

    def __init__(self):
        self.notifiers = WeakKeyDictionary()

    def __call__(self, trait, obj, name, old, new):
        all_notifiers = self.notifiers
        if trait in all_notifiers:
            inner = all_notifiers[trait]
            if obj in inner:
                notifiers = inner[obj]
                dead_notifiers = []
                for notifier in notifiers:
                    if not notifier(obj=obj, name=name, old=old, new=new):
                        dead_notifiers.append(notifier)
                if dead_notifiers:
                    for notifier in dead_notifiers:
                        notifiers.remove(notifier)
                    if not notifiers:
                        del inner[obj]
                        if not inner:
                            del all_notifiers[trait]

    def add_notifier(self, trait, obj, notifier):
        if trait not in self.notifiers:
            self.notifiers[trait] = WeakKeyDictionary()
        inner = self.notifiers[trait]
        if obj not in inner:
            inner[obj] = set()
        inner[obj].add(notifier)


#------------------------------------------------------------------------------
# Instances used by the traits framework
#------------------------------------------------------------------------------

# The main dispatch callable that is registered with each trait.
_dispatcher = Dispatcher()


