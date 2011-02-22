""" Integer trait types. """


# Martin library imports.
from martin.traits.trait_error import TraitError
from martin.traits.trait_type import TraitType

            
class Int(TraitType):
    """ Integer trait type. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, default_value=0, allow_none=False, **metadata):
        """ Constructor. """

        super(Int, self).__init__(default_value, allow_none, **metadata)
        
        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################
 
    def info(self):
        """ Returns a string that describes the type. """

        return 'an integer'
       
    def validate(self, value):
        """ Validates a value. """

        if value is None:
            if not self.allow_none:
                raise TraitError

        elif not type(value) is int:
            raise TraitError

        return value

#### EOF ######################################################################
