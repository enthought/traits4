""" The base class for all trait types. """


# Standard library imports.
import inspect

# Local imports.
from martin.traits.trait_error import TraitError
from martin.traits.undefined import Undefined


class TraitType(object):
    """ The base class for all trait types.

    A trait type is like a Python type such as 'int', only smarter ;^) Trait
    types can be used to enforce type safety on instance attributes and on
    function and method signatures.

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, default_value=Undefined, allow_none=False,
                 getter=None, setter=None, **metadata):
        """ Constructor. """

        self.default_value = default_value
        self.allow_none    = allow_none
        self.metadata      = metadata

        self.getter        = getter or TraitType.default_getter
        self.setter        = setter or TraitType.default_setter
        
        return

    ###########################################################################
    # 'TraitType' CLASS interface.
    ###########################################################################

    def default_getter(cls, trait_type, obj, trait_name):
        """ Gets the value of an attribute on an object.

        Note that the getter is only called the first time a trait is
        accessed (via '__getattr__'). After that the attribute exists in the
        object's dictionary ('__dict__') and hence it is accessed like any
        other Python attribute.

        """

        value = trait_type.get_default_value(obj, trait_name)
        setattr(obj, trait_name, value)
        
        return value

    default_getter = classmethod(default_getter)
    
    def default_setter(cls, trait_type, obj, trait_name, value):
        """ Sets the value of an attribute on an object. """

        # Validate the value.
        actual_value = trait_type.validate_attribute(obj, trait_name, value)
        
        # Note that we cannot use 'setattr' here as this method is called
        # from '__setattr__' on 'HasTraits'. This smells a little, although
        # by making the trait type responsible for the setting of the
        # attribute we allow the type to implement delegation or
        # prototyping semantics.
        obj.__dict__[trait_name] = actual_value
        
        return
        
    default_setter = classmethod(default_setter)
    
    def instantiate_trait_type_class(cls, trait_type_class):
        """ Instantiates a trait type class. """

        return trait_type_class()

    instantiate_trait_type_class = classmethod(instantiate_trait_type_class)
    
    def is_trait_type_class(cls, value):
        """ Returns True if 'value' is a class derived from 'TraitType'. """

        return isinstance(value, type) and issubclass(value, TraitType)

    is_trait_type_class = classmethod(is_trait_type_class)

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get_default_value(self, obj, trait_name):
        """ Returns the default value for an attribute. """

        return self.default_value

    def info(self):
        """ Returns a string that describes the type.

        This string is used when reporting validation errors.

        """

        raise NotImplementedError
    
    def validate(self, value):
        """ Validates a value.

        If the value is valid then it (or a possibly coerced value) is simply
        returned.

        If the value is invalid then a 'TraitError' is raised like so:-

        raise TraitError
        
        Quite often this is the only method that a trait type will have to
        implement, unless there is specific validation dependent on the context
        in which the value is being used (i.e. the validation is dependent on
        the specific object, attribute, method, function or argument etc.)

        """

        raise TraitError

    def validate_attribute(self, obj, trait_name, value):
        """ Validates an attribute value.

        By default we assume that the validation is independent of the object
        and the attrubute that we are setting, and hence we call the generic
        'validate' method. Obviously, derived trait types are free to override
        this behaviour.

        """

        try:
            value = self.validate(value)

        # fixme: Trait error exception should have attributes for details,
        # otherwise tools would have to parse the string to work out what
        # happened!
        except TraitError:
            message = """
            
            Invalid value for the '%s' trait of '%s'.
            Expected %s, got %s which is of type '%s'.
            
            """ % (trait_name, str(obj), self.info(), repr(value), type(value))

            raise TraitError(message)

        return value
    
    def validate_function_argument(self, fn, argument_name, value):
        """ Validates a function argument.

        By default we assume that the validation is independent of the function
        and argument, and hence we call the generic 'validate' method.
        Obviously, derived trait types are free to override this behaviour.

        """

        try:
            value = self.validate(value)

        except TraitError:
            message = """
            
            Invalid value for argument '%s' of function '%s'.
            Expected %s, got %s which is of type '%s'.
            
            """ % (
                argument_name, str(fn), self.info(), repr(value), type(value)
            )
            
            raise TraitError(message)

        return value

    def validate_function_return_value(self, fn, value):
        """ Validates a function return value.

        By default we assume that the validation is independent of the function
        that we are calling, and hence we call the generic 'validate' method.
        Obviously, derived trait types are free to override this behaviour.

        """

        try:
            value = self.validate(value)

        except TraitError:
            message = """
            
            Invalid return value from function '%s'.
            Expected %s, got %s which is of type '%s'.
            
            """ % (
                str(fn), self.info(), repr(value), type(value)
            )
            
            raise TraitError(message)

        return value
    
    def validate_method_argument(self, obj, method_name, argument_name, value):
        """ Validates a method argument.

        By default we assume that the validation is independent of the object,
        method, and argument, and hence we call the generic 'validate' method.
        Obviously, derived trait types are free to override this behaviour.

        """

        try:
            value = self.validate(value)

        except TraitError:
            message = """
            
            Invalid value for argument '%s' of method '%s' on '%s'.
            Expected %s, got %s which is of type '%s'.
            
            """ % (
                argument_name, method_name, str(obj), self.info(), repr(value),
                type(value)
            )
            
            raise TraitError(message)

        return value

    def validate_method_return_value(self, obj, method_name, value):
        """ Validates a method return value.

        By default we assume that the validation is independent of the object
        and the method that we are calling, and hence we call the generic
        'validate' method. Obviously, derived trait types are free to override
        this behaviour.

        """

        try:
            value = self.validate(value)

        except TraitError:
            message = """
            
            Invalid return value from method '%s' on '%s'.
            Expected %s, got %s which is of type '%s'.
            
            """ % (
                method_name, str(obj), self.info(), repr(value), type(value)
            )
            
            raise TraitError(message)

        return value

    ###########################################################################
    # Protected 'TraitType' interface.
    ###########################################################################

    def _resolve_class_or_name(self, class_or_name):
        """ Resolves a class or the name of a class.

        If 'class_or_name' is a class then it is returned unchanged. If it is
        the *name* of a class then the class is imported and returned.

        """

        if inspect.isclass(class_or_name):
            klass = class_or_name

        else:
            klass = self._import_symbol(class_or_name)

        return klass
    
    def _import_symbol(self, symbol_path):
        """ Imports the symbol defined by 'symbol_path'.

        The parameter *symbol_path* is a string in the form 'foo.bar:baz',
        which is turned into an import statement 'from foo.bar import baz'
        (i.e., the last component of the name is the symbol name, the rest is
        the package/module path to load it from).

        """
        
        module_name, symbol_name = symbol_path.split(':')

        module = __import__(module_name, globals(), locals(), [symbol_name])
        symbol = getattr(module, symbol_name)

        return symbol

#### EOF ######################################################################
