from ctraits import *
from cgraph import DAGraph
from weakref import ref


class NotificationMgr(object):

    def __init__(self):
        self.graph = DAGraph()

    def __call__(self, trait, obj, name, old, new):
        trait_ref = ref(trait)
        obj_ref = ref(obj)

        # static handlers
        if trait_ref in self.graph:
            for notifier_ref in self.graph.traverse(trait_ref, dfs=False):
                notifier = notifier_ref()
                if notifier is None:
                    self.graph.delete_node(notifier_ref)
                else:
                    notifier(obj, name, old, new)

        # dynamic handlers
        node = (trait_ref, obj_ref)
        if node in self.graph:
            for notifier_ref in self.graph.traverse(node, dfs=False):
                notifier = notifier_ref()
                if notifier is None:
                    self.graph.delete_node(notifier_ref)
                else:
                    notifier(obj, name, old, new)

    def add_static_notifier(self, trait, cb):
        self.graph.add_edge(ref(trait), ref(cb))

    def add_dynamic_notifier(self, trait, obj, cb):
        self.graph.add_edge((ref(trait), ref(obj)), ref(cb))


notification_mgr = NotificationMgr()


class StaticChangeBinder(object):

    def __init__(self, names, func):
        names = names.split(',')
        self.names = set([name.strip() for name in names])
        self.func = func

    def __call__(self, traits):
        names = self.names
        for name, trait in traits:
            if name in names:
                trait.notifier = notification_mgr
                notification_mgr.add_static_notifier(trait, self.func)
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
        notification_mgr.add_dynamic_notifier(trait, self, cb)


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
