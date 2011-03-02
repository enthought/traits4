""" Metaclasss for 'HasTraits'. """


class MetaHasTraits(type):
    """ Metaclasss for 'HasTraits'.

    The metaclass does the following:-

    1) Harvests traits.

    """

    # fixme: This is only required because we want to switch between the Cython
    # and pure Python implementations for testing and comparison. It should
    # be set to the *module* that contains the appropriate version.
    implementation = None
    
    def __new__(cls, name, bases, dict):
        """ Creates a class.

        Note that here, 'cls' is a a reference to 'MetaHasTraits', *not* the
        class being created.

        """

        # Harvest any traits defined in the class dictionary.
        if name != 'HasTraits':
            traits = cls.harvest_traits(dict)

        else:
            traits = {}
            
        # Create the class as normal.
        klass = type.__new__(cls, name, bases, dict)

        # Attach the trait namespace?
        klass.__traits__ = traits
        
        return klass

    ###########################################################################
    # 'MetaHasTraits' CLASS protocol.
    ###########################################################################

    @classmethod
    def harvest_traits(cls, dict):
        """ Harvest any traits defined in the class' dictionary.

        Traits can be specified as either:-

        a) A class derived from 'TraitType'
        b) An instance of a class derived from 'TraitType'

        Internally we *always* store 'TraitType' *instances*, so if a class is
        found we will call it with no arguments.

        """

        traits = {}
        for name, value in dict.items():
            # a) A class derived from 'TraitType'
            if MetaHasTraits.is_trait_type_class(value):
                trait_type = value()
                
            # b) An instance of a class derived from 'TraitType'
            elif isinstance(value, cls.implementation.TraitType):
                trait_type = value

            # c) Some other class attribute that we don't care about!
            else:
                trait_type = None
                
            if trait_type is not None:
                # Give the metaclass chance to wrap the trait type (used in the
                # accessor implementation).
                if hasattr(cls.implementation, 'trait_type_wrapper'):
                    dict[name] = cls.implementation.trait_type_wrapper(
                        name, trait_type
                    )

                else:
                    # The descriptor protocol doesn't pass in the name of the
                    # attribute being accessed (IMHO this is a major flaw in
                    # the descriptor API), so we have to set the name of the
                    # trait here.
                    trait_type.name = name

                traits[name] = trait_type
                
        return traits

    @classmethod
    def is_trait_type_class(cls, value):
        """ Returns True if 'value' is a class derived from 'TraitType'. """

        is_trait_type_class = (
            isinstance(value, type)
            and issubclass(value, cls.implementation.TraitType)
        )

        return is_trait_type_class
    
#### EOF ######################################################################
