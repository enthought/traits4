from ctraits import *
import types

from notifiers import FunctionNotifier, BoundMethodNotifier, _dispatcher


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

                    for name, trait in traits:
                        if trait.dispatcher is None:
                            trait.dispatcher = _dispatcher

        return type.__new__(meta, name, bases, dct)


class HasTraits(CHasTraits):
    
    __metaclass__ = MetaHasTraits

    def __init__(self, *args, **kwargs):
        for attr_name, attr in self.__class__.__dict__.iteritems():
            if hasattr(attr, '__on_trait_change__'):
                names, kwargs = attr.__on_trait_change__
                for name in names:
                    self.on_trait_change(name, getattr(self, attr_name))

    def on_trait_change(self, name, cb):
        trait = self.__class__.__dict__[name]
        
        if isinstance(cb, types.MethodType):
            notifier = BoundMethodNotifier(cb)
        elif isinstance(cb, types.FunctionType):
            notifier = FunctionNotifier(cb)
        else:
            raise TypeError('not yet supported for this type %s' % type(cb))

        dispatcher = trait.dispatcher
        dispatcher.add_notifier(trait, self, notifier)


def on_trait_change(*names, **kwargs):
    for name in names:
        if not isinstance(name, basestring):
            raise TypeError('Names must be a string.')

    def closure(func):
        func.__on_trait_change__ = (names, kwargs)
        return func

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
