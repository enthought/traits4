

class _HasTraits:

    def __init__(self):
        object.__setattr__(self, 'itrait_dict', None)

    def __getattribute__(self, name):
        itrait_dict = object.__getattribute__(self, 'itrait_dict')

        if itrait_dict is not None:
            if name in itrait_dict:
                value = itrait_dict[name]
                return value.__get__(self, object.__getattribute__(self, '__class__'))

        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, val):
        itrait_dict = object.__getattribute__(self, 'itrait_dict')

        if itrait_dict is not None:
            if name in itrait_dict:
                value = itrait_dict[name]
                value.__set__(self, val)
                return 

        object.__setattr__(self, name, val)

    def __delattr__(self, name):
        itrait_dict = object.__getattribute__(self, 'itrait_dict')

        if itrait_dict is not None:
            if name in itrait_dict:
                value = itrait_dict[name]
                value.__del__(self)
                return

        object.__delattr__(self, name)

    def add_trait(self, name, trait):
        itrait_dict = object.__getattribute__(self, 'itrait_dict')
        if itrait_dict is None:
            itrait_dict = {}
            object.__setattr__(self, 'itrait_dict', itrait_dict)

        trait._name = name
        itrait_dict[name] = trait

        # we need to remove the current value in the obj_dict
        # for the new instance trait, so that the new trait
        # can compute and return its value.
        obj_dict = object.__getattribute__(self, '__dict__')
        if name in obj_dict:
            del obj_dict[name]

    def get_trait(self, name):
        itrait_dict = object.__getattribute__(self, '__dict__')
        if itrait_dict is not None:
            if name in itrait_dict:
                return itrait_dict[name]

        cls_dict = object.__getattribute__(self, '__class__').__dict__
        if name in cls_dict:
            trait = cls_dict[name]
            if isinstance(trait, _Trait):
                return trait

        raise ValueError('Object has no trait named %s' % name)


