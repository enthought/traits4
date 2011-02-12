from ctraits import *
from weakref import ref, WeakKeyDictionary
import types


class ChangeBinder(object):
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
                notification_mgr.add_static_notifier(trait, FuncNotifier(self.func))
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
        if isinstance(cb, types.MethodType):
            notifier = BoundMethodNotifier(cb)
        elif isinstance(cb, types.FunctionType):
            notifiers = FuncNotifier(cb)
        else:
            raise TypeError('not yet supported for this type %s' % type(cb))
        notification_mgr.add_dynamic_notifier(trait, self, notifier)


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
