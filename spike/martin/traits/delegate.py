""" Property trait type modifier. """


# Standard library imports.
import pickle

# Martin library imports.
from martin.traits.builtin.any import Any
from martin.traits.builtin.instance import Instance
from martin.traits.trait_modifier import TraitModifier
from martin.traits.trait_type import TraitType


class Delegate(TraitModifier):
    """ Delegate trait placeholder. """

    def __init__(self, delegate_trait_name):
        """ Constructor. """

        self.delegate_trait_name = delegate_trait_name

        return

    ###########################################################################
    # 'TraitModifier' interface.
    ###########################################################################
    
    def install(self, obj, trait_name):
        """ Install the trait type. """

        # Find the trait that we delegate to.
        delegate = getattr(obj, self.delegate_trait_name)

        # Create the trait type that we install.
        #
        # fixme: We would really like to clone the actual trait type.
        # Find the trait type associated with it.
        delegate_trait_type = delegate.get_trait_type(trait_name)
        
        # Clone it.
        #
        # fixme: We need a clone interface!
        trait_type = type(delegate_trait_type)()
        
        def delegate_getter(trait_type, obj, trait_name):
            """ Gets the value of a delegated attribute on an object. """

            return getattr(delegate, trait_name)

        def delegate_setter(trait_type, obj, trait_name, value):
            """ Sets the value of a delegated attribute on an object. """

            return setattr(delegate, trait_name, value)

        trait_type.getter = delegate_getter
        trait_type.setter = delegate_setter
        
        return trait_type
    
#### EOF ######################################################################
