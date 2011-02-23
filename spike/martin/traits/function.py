""" Type-checked functions. """


# Standard library imports.
import inspect

# Local imports.
from martin.traits.trait_type import TraitType


def function(**trait_types):
    """ Factory function for type-checking decorators. """

    for name, trait_type in trait_types.items():
        if TraitType.is_trait_type_class(trait_type):
            trait_type = TraitType.instantiate_trait_type_class(trait_type)
            
        trait_types[name] = trait_type
        ##trait_types[name] = TraitType.instantiate_trait_type(trait_type)

    def decorator(fn):
        """ Decorator that produces a type-checked function. """

        def wrapper(*args, **kw):
            """ Type-checking function wrapper. """

            actual_args = _validate_args(fn, trait_types, args)
            actual_kw   = _validate_kw(fn, trait_types, kw)

            return_value = fn(*actual_args, **actual_kw)

            return _validate_return_value(fn, trait_types, return_value)

        wrapper.__doc__ = fn.__doc__
        
        return wrapper

    return decorator

## class FunctionDecoratorFactory(object):
##     """ Factory for type-checking decorators. """

##     ###########################################################################
##     # 'object' interface.
##     ###########################################################################
    
##     def __call__(self, **trait_types):
##         """ Factory function for for type-checking decorators. """

##         for name, trait_type in trait_types.items():
##             trait_types[name] = TraitType.instantiate_trait_type(trait_type)

##         def decorator(fn):
##             """ Decorator that produces a type-checked function. """

##             def wrapper(*args, **kw):
##                 """ Type-checking function wrapper. """

##                 actual_args = self._validate_args(fn, trait_types, args)
##                 actual_kw   = self._validate_kw(fn, trait_types, kw)

##                 value = fn(*actual_args, **actual_kw)

##                 return self._validate_return_value(fn, trait_types, value)

##             return wrapper

##         return decorator

##     ###########################################################################
##     # Protected 'FunctionDecoratorFactory' interface.
##     ###########################################################################

##     def _validate_args(self, fn, trait_types, args):
##         """ Validates a positional argument list.

##         Returns the validated arguments.

##         """

##         argnames, varargs, varkw, defaults = inspect.getargspec(fn)

##         actual = []
##         for name, value in zip(argnames, args):
##             trait_type = trait_types.get(name)
##             if trait_type is not None:
##                 value = trait_type.validate_function_argument(fn, name, value)

##             actual.append(value)

##         return actual

##     def _validate_kw(self, fn, trait_types, kw):
##         """ Validates a keyword argument dictionary.

##         Returns the validated arguments.

##         """

##         actual = {}
##         for name, value in kw.items():
##             trait_type = trait_types.get(name)
##             if trait_type is not None:
##                 value = trait_type.validate_function_argument(fn, name, value)

##             actual[name] = value

##         return actual

##     def _validate_return_value(self, fn, trait_types, value):
##         """ Validates a return value.

##         Returns the validated value.

##         """

##         trait_type = trait_types.get('_returns_')
##         if trait_type is not None:
##             value = trait_type.validate_function_return_value(fn, value)

##         return value

## function = FunctionDecoratorFactory()

### Private functions #########################################################

def _validate_args(fn, trait_types, args):
    """ Validates a positional argument tuple.

    Returns the validated arguments.

    """

    argnames, varargs, varkw, defaults = inspect.getargspec(fn)
    
    actual = []
    for name, value in zip(argnames, args):
        trait_type = trait_types.get(name)
        if trait_type is not None:
            value = trait_type.validate_function_argument(fn, name, value)

        actual.append(value)

    return actual

def _validate_kw(fn, trait_types, kw):
    """ Validates a keyword argument dictionary.

    Returns the validated arguments.

    """

    actual = {}
    for name, value in kw.items():
        trait_type = trait_types.get(name)
        if trait_type is not None:
            value = trait_type.validate_function_argument(fn, name, value)

        actual[name] = value
        
    return actual

def _validate_return_value(fn, trait_types, value):
    """ Validates a return value.

    Returns the validated value.

    """

    trait_type = trait_types.get('_returns_')
    if trait_type is not None:
        value = trait_type.validate_function_return_value(fn, value)

    return value

#### EOF ######################################################################

## def function(argument_types, return_value_type):
##     """ Factory function for type-checking decorators. """

##     argument_types    = TraitType.create_trait_types(argument_types)
##     return_value_type = TraitType.create_trait_type(return_value_type)
        
##     def decorator(fn):
##         """ Decorator that produces a type-checked function. """

##         def wrapper(*args, **kw):
##             """ Type-checking function wrapper. """

##             args = _validate_arguments(fn, argument_types, args)
##             value = fn(*args, **kw)

##             return _validate_return_value(fn, return_value_type, value)

##         wrapper.__doc__ = fn.__doc__

##         return wrapper

##     return decorator

## def _validate_arguments(fn, trait_types, args):
##     """ Validates an argument list.

##     Returns the validated arguments.

##     """

##     arg_names, varargs, varkw, defaults = inspect.getargspec(fn)
    
##     actual = []
##     for name, trait_type, arg in zip(arg_names, trait_types, args):
##         actual.append(
##             trait_type.validate_function_argument(fn, name, arg)
##         )

##     return actual

## def _validate_return_value(fn, trait_type, value):
##     """ Validates a return value.

##     Returns the validated value.

##     """

##     return trait_type.validate_function_return_value(fn, value)
