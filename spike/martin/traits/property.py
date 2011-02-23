""" Property trait type modifier. """


# Martin library imports.
from martin.traits.builtin.instance import Instance
from martin.traits.trait_type import TraitType


def Property(trait_type):
    """ Property trait type modifier.

    'trait_type' can be:-
    
    1) a trait type instance
    
    e.g. Property(Int(20))
    
    2), a trait type class
    
    e.g. Property(Int)
    
    3) a class/interface
    
    e.g. from package.module import Foo
    
    Property(Foo)
    
    4) the *name* of a class/interface
    
    e.g. Property('package.module:Foo')
    
    """
    
    # If the trait type is a 'TraitType' *class* then instantiate it.
    if TraitType.is_trait_type_class(trait_type):
        trait_type = TraitType.instantiate_trait_type_class(trait_type)
            
    # For now we assume that if the trait type is *not* a trait type, then
    # it is a class/interface or the *name* of a class/interface that we can
    # use to make an 'Instance' trait type. Obviously we should probably force
    # that here!
    elif not isinstance(trait_type, TraitType):
        trait_type = Instance(trait_type)

    trait_type.getter = property_getter
    trait_type.setter = property_setter
    
    return trait_type


def property_getter(trait_type, obj, trait_name):
    """ Gets the value of a property attribute on an object. """
    
    getter = getattr(obj, '_get_%s' % trait_name)
    
    return getter()

    
def property_setter(trait_type, obj, trait_name, value):
    """ Sets the value of a a property attribute on an object. """
    
    # Validate the value.
    actual_value = trait_type.validate_attribute(obj, trait_name, value)

    setter = getattr(obj, '_set_%s' % trait_name)
    setter(actual_value)
        
    return
    
#### EOF ######################################################################
