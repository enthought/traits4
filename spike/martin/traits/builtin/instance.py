""" Instance trait type. """


# Major package imports.
from enthought.traits.protocols.api import adapt

# Martin library imports.
from martin.traits.has_traits import HasTraits
from martin.traits.interface import Interface
from martin.traits.trait_error import TraitError
from martin.traits.trait_type import TraitType
from martin.traits.undefined import Undefined


class Instance(TraitType):
    """ Instance trait type. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, class_or_name=HasTraits,
                 default_value=Undefined, allow_none=False, **metadata):
        """ Constructor.

        'class_or_name' can be a class/interface, or the *name* of a
        class/interface in the form 'package.module:ClassOrInterface'.

        If 'allow_none' is True and 'default_value' is Undefined, a default
        value of None is used instead.
        
        """

        if allow_none and default_value is Undefined:
            default_value = None
            
        super(Instance, self).__init__(default_value, allow_none, **metadata)
            
        self.class_or_name = class_or_name

        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_klass(self):
        """ Property getter. """

        if not hasattr(self, '_class'):
            self._class = self._resolve_class_or_name(self.class_or_name)

        return self._class

    klass = property(_get_klass)
    
    #### Methods ##############################################################
    
    def get_default_value(self, obj, trait_name):
        """ Returns the default value for the trait type. """

        if type(self.default_value) is tuple:
            default_value = self.klass(*self.default_value)

        else:
            default_value = self.default_value

        return default_value

    def info(self):
        """ Returns a string that describes the type. """

        return 'an instance of %s' % str(self.class_or_name)
    
    def validate(self, value):
        """ Validates a value. """

        if value is None:
            if not self.allow_none:
                raise TraitError

        elif self.default_value == value:
            pass

        else:
            value = adapt(value, self.klass, Undefined)
            if value is Undefined:
                raise TraitError

        return value

##     def validate(self, value):
##         """ Validates a value. """

##         if value is None:
##             if not self.allow_none:
##                 raise TraitError

##         else:
##             if issubclass(self.klass, Interface):
##                 value = self._validate_interface(value, klass)

##             else:
##                 value = self._validate_class(value, klass)

##         return value

    ###########################################################################
    # Private interface.
    ###########################################################################

##     def _validate_interface(self, value, interface):
##         """ Validates a value to see if it implements an interface. """

##         if not isinstance(value, HasTraits) or not value.implements(interface):
##             raise TraitError

##         return value

##     def _validate_class(self, value, klass):
##         """ Validates a value to see if it is an instance of a class. """

##         if not isinstance(value, klass):
##             raise TraitError

##         return value

#### EOF ######################################################################
