""" Any trait type. """


# Martin library imports.
from martin.traits.trait_error import TraitError
from martin.traits.trait_type import TraitType


class Any(TraitType):
    """ Any trait type. """

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def info(self):
        """ Returns a string that describes the type. """

        return 'any value'
    
    def validate(self, value):
        """ Validates a value. """

        if value is None:
            if not self.allow_none:
                raise TraitError
            
        return value

#### EOF ######################################################################
