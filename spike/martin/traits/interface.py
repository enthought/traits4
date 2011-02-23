""" The base class for all interfaces. """


# Major package imports.
from enthought.traits.protocols.protocols import AbstractBaseMeta

# Local imports.
from martin.traits.has_traits import HasTraits, MetaHasTraits


class _Interface(HasTraits):
    """ The PRIVATE base class for all interfaces.

    This is just a 'forward declaration' of the 'Interface' class. We need it
    because in the 'MetaInterface' class' '__new__' method, we want to make
    sure that an interface only inherits from other interfaces (or simply the
    'Interface' class itself), but we cannot reference 'Interface' until it
    has been created!

    Do not USE this class outside of this module!
    
    """
    

class MetaInterface(MetaHasTraits, AbstractBaseMeta):
    """ The meta-class for interfaces.

    Used to prevent instantiation of interfaces.

    """

    def __new__(cls, name, bases, dict):
        """ Creates a *class*. """

        # Make sure that the interface does not imherit from any implementation
        # (i.e. non-interface) classes.
        for base in bases:
            if not issubclass(base, _Interface):
                raise ValueError('Interfaces cannot inherit implementation')
            
        # Create the class as normal.
        return super(MetaHasTraits, cls).__new__(cls, name, bases, dict)

    def __call__(cls, *args, **kw):
        """ Creates an instance of the class. """

        raise ValueError('Cannot instantiate interface %s' % cls)


class Interface(_Interface):
    """ The base class for all interfaces.

    Interfaces CANNOT be instantiated, and there are either:-

    a) Derived from 'Interface' *only*
    
    e.g. class IFoo(Interface)
             pass
    
    or
    
    b) Derived from other interfaces:-
    
    e.g. class IBaz(IFoo, IBar):
             pass
    
    """
    
    __metaclass__ = MetaInterface

    ###########################################################################
    # 'Interface' class interface.
    ###########################################################################

    def get_bases(cls):
        """ Returns a tuple of the interfaces inherited by this one.        

        Note that this returns *only* those interfaces explicitly listed in
        the interface definition, not any interfaces implicitly implemented
        via inheritance.

        If the interface inherits from 'Interface' only, then an empty tuple is
        returned.

        e.g.

        class IFoo(Interface):
            pass

        IFoo.get_bases() -> []

        class IBar(IFoo):
            pass

        IBar.get_bases() -> [IFoo]

        class IBaz(IBar):
            pass

        IBaz.get_bases() -> [IBar]

        """

        if len(cls.__bases__) == 1 and cls.__bases__[0] is Interface:
            bases = ()

        else:
            bases = cls.__bases__
            
        return bases

    get_bases = classmethod(get_bases)

#### EOF ######################################################################
