""" List trait type. """


# Martin library imports.
from martin.traits.trait_error import TraitError
from martin.traits.trait_type import TraitType
from martin.traits.undefined import Undefined

# Local imports.
from martin.traits.builtin.any import Any
from martin.traits.builtin.instance import Instance


class List(TraitType):
    """ List trait type. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, item_type=Any,
                 default_value=Undefined, allow_none=False, **metadata):
        """ Constructor.

        'item_type' can be a trait type, a class/interface or the *name* of a
        class/interface in the form 'package.module:ClassOrInterface'.

        """

        if default_value is Undefined:
            default_value = []

        super(List, self).__init__(default_value, allow_none, **metadata)

        # If the item type is a 'TraitType' *class* then instantiate it.
        if TraitType.is_trait_type_class(item_type):
            item_type = TraitType.instantiate_trait_type_class(item_type)
            
        # For now we assume that if the item type is *not* a trait type, then
        # it is a class/interface or the *name* of a class/interface. Obviously
        # we should probably force that here!
        elif not isinstance(item_type, TraitType):
            item_type = Instance(item_type)
            
        self.item_type = item_type
        
        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get_default_value(self, obj, trait_name):
        """ Returns the default value for the trait type. """

        return self.default_value

    def info(self):
        """ Returns a string that describes the type. """

        return 'a list containing items of type %s' % str(self.item_type)
    
    def validate(self, value):
        """ Validates a value. """

        if value is None:
            if not self.allow_none:
                raise TraitError

        elif not isinstance(value, list):
            raise TraitError

        else:
            value = [self.item_type.validate(item) for item in value]

        return value

#### EOF ######################################################################
