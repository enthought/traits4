from ctraits import *
from weakref import ref, WeakKeyDictionary
import types

class Notifier(object):

    __slots__ = ('handler_ref', 'arg_handler')

    def __init__(self, handler):
        self.handler_ref = ref(handler)
        arg_count = handler.func_code.co_argcount
        
        if arg_count == 0:
            arg_handler = lambda obj, name, old, new: ()
        elif arg_count == 1:
            arg_handler = lambda obj, name, old, new: (obj,)
        elif arg_count == 2:
            arg_handler = lambda obj, name, old, new: (obj, new)
        elif arg_count == 3:
            arg_handler = lambda obj, name, old, new: (obj, old, new)
        elif arg_count == 4:
            arg_handler = lambda obj, name, old, new: (obj, name, old, new) 
        else:
            raise TypeError('Handler %s takes incompatible number of args: %s'
                            % (handler, arg_count))

        self.arg_handler = arg_handler

    def __call__(self, obj, name, old, new):
        handler = self.handler_ref()
        if handler is None:
            return False
        handler(*self.arg_handler(obj, name, old, new))
        return True


class NotificationMgr(object):

    def __init__(self):
        self.static_notifiers = WeakKeyDictionary()
        self.dynamic_notifiers = WeakKeyDictionary()

    def __call__(self, trait, obj, name, old, new):
        static_notifiers = self.static_notifiers
        dynamic_notifiers = self.dynamic_notifiers

        # dispatch static handlers
        if trait in static_notifiers:
            notifiers = static_notifiers[trait]
            dead_notifiers = []
            for notifier in notifiers:
                if not notifier(obj, name, old, new):
                    dead_notifiers.append(notifier)
            if dead_notifiers:
                for notifier in dead_notifiers:
                    notifiers.remove(notifier)
                if not notifiers:
                    del static_notifiers[trait]

        # dispatch dynamic handlers
        if trait in dynamic_notifiers:
            inner = dynamic_notifiers[trait]
            if obj in inner:
                notifiers = inner[obj]
                dead_notifiers = []
                for notifier in notifiers:
                    if not notifier(obj, name, old, new):
                        dead_notifiers.append(notifier)
                if dead_notifiers:
                    for notifier in dead_notifiers:
                        notifiers.remove(notifier)
                    if not notifiers:
                        del inner[obj]
                        if not inner:
                            del dynamic_notifiers[trait]

    def add_static_notifier(self, trait, notifier):
        if trait not in self.static_notifiers:
            self.static_notifiers[trait] = set()
        self.static_notifiers[trait].add(notifier)

    def add_dynamic_notifier(self, trait, obj, notifier):
        if trait not in self.dynamic_notifiers:
            self.dynamic_notifiers[trait] = WeakKeyDictionary()
        inner = self.dynamic_notifiers[trait]
        if obj not in inner:
            inner[obj] = set()
        inner[obj].add(notifier)


notification_mgr = NotificationMgr()


class StaticChangeBinder(object):
    """ This is just a convienence sentinel. The instances
    are discarded in the MetaHasTraits class. So no worries
    about maintaining false refs to things.

    """
    def __init__(self, names, func):
        names = names.split(',')
        self.names = set([name.strip() for name in names])
        self.func = func

    def __call__(self, traits):
        names = self.names
        for name, trait in traits:
            if name in names:
                trait.notifier = notification_mgr
                notification_mgr.add_static_notifier(trait, Notifier(self.func))
        return self.func


class MetaHasTraits(type):

    def __new__(meta, name, bases, dct):
        for base in bases:
            # this hack is because HasTraits won't be defined
            # the first time the metaclass is called.
            if base.__name__ == 'HasTraits':
                if base is HasTraits:
                    traits = []
                    for key, val in dct.items():
                        if isinstance(val, CTrait):
                            val.name = key
                            traits.append((key, val))
                        elif (type(val) is type) and issubclass(val, CTrait):
                            trait = val()
                            dct[key] = trait
                            trait.name = key
                            traits.append((key, trait))

                    traits_tuple = tuple(traits)
                    for key, val in dct.items():
                        if isinstance(val, StaticChangeBinder):
                            dct[key] = val(traits_tuple)

        return type.__new__(meta, name, bases, dct)


class HasTraits(CHasTraits):
    
    __metaclass__ = MetaHasTraits

    def on_trait_change(self, name, cb):
        trait = self.__class__.__dict__[name]
        trait.notifier = notification_mgr
        notification_mgr.add_dynamic_notifier(trait, self, Notifier(cb))


def on_trait_change(names):
    if not isinstance(names, basestring):
        raise TypeError('Names must be a comma separated string.')

    def closure(func):
        return StaticChangeBinder(names, func)

    return closure


class Int(CInt): 
    pass


class Float(CFloat):
    pass


class Long(CLong):
    pass


class Str(CStr):
    pass


class List(CList):
    pass


class Tuple(CTuple):
    pass


class Dict(CDict):
    pass


class Any(CAny):
    pass
