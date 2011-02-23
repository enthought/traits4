""" Example of how we might do the 'TraitType' refactor. """


# Standard library imports.
import inspect, sys

# Major package imports.
from enthought.traits.protocols.api import adapt, addClassAdvisor
from enthought.traits.protocols.api import declareImplementation

# Local imports.
from martin.traits.trait_modifier import TraitModifier
from martin.traits.trait_type import TraitType

print 'object dir', dir(object)
class MetaHasTraits(type):
    """ Example meta-class. """

    def __new__(cls, name, bases, dict):
        """ Creates a class.

        Note that here, 'cls' is a a reference to 'MetaHasTraits', *not* the
        class being created.

        """

        # Create the class as normal.
        klass = type.__new__(cls, name, bases, dict)

        # If the class does *not* have an 'implements' clause, then this makes
        # sure the list of implemented interfaces is initialized. If the class
        # *does* have an implements clause, then the list is set in the
        # 'implements' class advisor (see the function at the bottom of this
        # module).
        klass.__implements__ = []

        # Harvest any traits defined in the class dictionary.
        klass.__traits__ = cls.harvest_traits(klass)
        
##         # Attach any implemented interfaces to the class.
##         frame = sys._getframe(1)
##         klass.__implements__ = frame.f_locals.get('__implements__', [])

##         # Make sure that we clear out the 'implements' information from the
##         # frame so that the next class defined in this thread doesn't get the
##         # same ones!
##         frame.f_locals.pop('__implements__', None)

##         # As recommended in the Python documentation make sure that we get rid
##         # of our frame reference immediately (see the 'inspect' module for more
##         # details).
##         del frame

        # Harvest trait modifiers.
        klass.__trait_modifiers__ = cls.harvest_trait_modifiers(klass)
        
        return klass

    ###########################################################################
    # 'MetaHasTraits' CLASS interface.
    ###########################################################################

    def harvest_traits(cls, klass):
        """ Harvest any traits defined in the class' dictionary.

        Traits can be specified as either:-

        a) A class derived from 'TraitType'
        b) An instance of a class derived from 'TraitType'

        Internally we always store 'TraitType' *instances*, so if a class is
        found we will call it with no arguments.

        """
        
        traits = {}
        for key, value in klass.__dict__.items():
            # a) A class derived from 'TraitType'
            if TraitType.is_trait_type_class(value):
                traits[key] = TraitType.instantiate_trait_type_class(value)
                delattr(klass, key)
                
            # b) An instance of a class derived from 'TraitType'
            elif isinstance(value, TraitType):
                traits[key] = value
                delattr(klass, key)

        return traits

    harvest_traits = classmethod(harvest_traits)

    def harvest_trait_modifiers(cls, klass):
        """ Harvest any trait modifiers defined in the class' dictionary.

        Trait modifierss can be specified as either:-

        a) A class derived from 'TraitModifier'
        b) An instance of a class derived from 'TraitModifier'

        Internally we always store 'TraitModifier' *instances*, so if a class
        is found we will call it with no arguments.

        """

        trait_modifiers = {}
        for key, value in klass.__dict__.items():
            if isinstance(value, TraitModifier):
                trait_modifiers[key] = value
                delattr(klass, key)

        return trait_modifiers

    harvest_trait_modifiers = classmethod(harvest_trait_modifiers)

    
class HasTraits(object):
    """ An example of the proposed traits implementation. """
    
    __metaclass__ = MetaHasTraits

    ###########################################################################
    # 'HasTraits' CLASS interface.
    ###########################################################################

    def get_trait_type(cls, name):
        """ Returns the type of the trait with the specified name.

        Returns None if no such trait exists.

        """

        # fixme: For now we do it the stupid, slow way, but obviously in
        # future we can created a cached dictionary of all traits in an
        # object's type hierarchy and reduce this to a single dictionary
        # lookup.
        return cls.get_traits(inherited=True).get(name)

    get_trait_type = classmethod(get_trait_type)

    def get_traits(cls, inherited=False, **metadata):
        """ Returns all traits that (optionally) contain the metadata.

        The return value is a dictionary where the keys are the trait names
        and the values are the corresponding trait type instrances:-

        { Str trait_name : Instance(TraitType) trait_type }

        """

        # fixme: Looooong method... factor out metadata matching?
        if inherited:
            traits = {}
            for base in inspect.getmro(cls):
                traits.update(base.__traits__)
                if base is HasTraits:
                    break

        else:
            traits = cls.__traits__.copy()

        if len(metadata) > 0:
            result = {}
            for trait_name, trait_type in traits.items():
                for name, value in metadata.items():
                    if name not in trait_type.metadata:
                        break

                    if trait_type.metadata[name] != value:
                        break

                else:
                    result[trait_name] = trait_type

        else:
            result = traits
            
        return result

    get_traits = classmethod(get_traits)

    def get_trait_names(cls, inherited=False):
        """ Returns the names of all traits on this object. """

        return cls.get_traits(inherited).keys()

    get_trait_names = classmethod(get_trait_names)

    def get_trait_interfaces(cls):
        """ Returns a list of the interfaces implemented by the class.

        Note that this returns *only* those interfaces explicitly listed in
        the class' 'implements' clause, not any interfaces implicitly
        implemented via inheritance (remember that an interface can be
        inherited via both class and interface inheritance).
        
        """

        return cls.__implements__[:]

    get_trait_interfaces = classmethod(get_trait_interfaces)

    def implements(cls, interface):
        """ Returns True if the class implements the interface. """

        for cls in inspect.getmro(cls):
            for implemented in cls.get_trait_interfaces():
                if issubclass(implemented, interface):
                    return True

            if cls is HasTraits:
                break
            
        return False

    implements = classmethod(implements)

    ###########################################################################
    # 'object' interface.
    ###########################################################################
    
    def __init__(self, **kw):
        """ Constructor. """

        # fixme: We have to assign this via the dict as we override setattr and
        # we need to access the instance traits in there!
        self.__dict__['_instance_traits_'] = {}
        
        for name, value in kw.items():
            setattr(self, name, value)

        # Initialize any trait modifiers.
        for name, value in type(self).__trait_modifiers__.items():
            self._instance_traits_[name] = value.install(self, name)

        return

    def __getattr__(self, name):
        """ Gets the value of an attribute on the object. """

        trait_type = self.get_trait_type(name)
        if trait_type is None:
            trait_type = self.__dict__['_instance_traits_'].get(name)
            
        # If the object has a trait with the specified name then use the
        # corresponding trait type to get the value.
        if trait_type is not None:
            value = trait_type.getter(trait_type, self, name)
            
        # Otherwise, this is just a regular Python attribute so let Python do
        # its thang (this will actually just raise an 'AttributeError' since
        # Python only calls '__getattr__' when it can't find an attribute).
        else:
            # fixme: It seems a little wierd to me but the 'object' type
            # doesn't have a '__getattr__' method. However, it *does* have
            # '__setattr__', '__delattr__' and '__getattribute__'.
            value = object.__getattribute__(self, name)

        return value

    def __setattr__(self, name, value):
        """ Sets the value of an attribute on the object. """

        trait_type = self.get_trait_type(name)
        if trait_type is None:
            trait_type = self.__dict__['_instance_traits_'].get(name)

        # If the object has a trait with the specified name then use the
        # corresponding trait type to set the value.
        if trait_type is not None:
            trait_type.setter(trait_type, self, name, value)

        # Otherwise, this is just a regular Python attribute so let Python do
        # its thang.
        else:
            object.__setattr__(self, name, value)
            
        return

    
def implements(*args):
    """ Convenience class advisor for declaring provided interfaces. """
    
    def callback(klass):
        """ Called when the class has been created. """
        
        # This puts in the information required by the first implementation
        # of our traits 'Interface'. This may not be required eventually as
        # to determine whether or not an object implements an interface, we
        # can simply call adapt and see if we get the object itself back.
        klass.__implements__ = list(args)
        
        # This adds the information required by PyProtocols for adaptation.
        declareImplementation(klass, instancesProvide=list(args))
        
        return klass
    
    addClassAdvisor(callback)
    
    return

## def implements(*args):
##     """ Used to declare that a class implements one or more interfaces.

##     e.g.

##     class IFoo(Interface):
##         pass

##     class IBar(Interface):
##         pass

##     class Foobar(HasTraits):
##         implements(IFoo, IBar)

##     """

##     # 1 level up gives us the frame that called 'implements'
##     # 2 levels up gives us the frame that the class is being created in
##     frame = sys._getframe(2)
##     frame.f_locals['__implements__'] = args

##     # As recommended in the Python documentation make sure that we get rid of
##     # our frame reference immediately (see the 'inspect' module for details).
##     del frame

##     return

#### EOF ######################################################################

