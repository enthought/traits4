""" The base class for all test cases for built-in trait types. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import Any, HasTraits, TraitError
    

class BuiltinTestCase(unittest.TestCase):
    """ The base class for all test cases for built-in trait types. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # The trait type that we will use to do the tests.
        self.trait_type = Any
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_allow_none(self):
        """ allow none """

        class Foo(HasTraits):
            x = self.trait_type(allow_none=True)
            
        f = Foo()

        f.x = None
        self.assertEqual(f.x, None)
        
        return

    def test_disallow_none(self):
        """ disallow none """

        class Foo(HasTraits):
            x = self.trait_type(allow_none=False)
            
        f = Foo()
        self.failUnlessRaises(TraitError, setattr, f, 'x', None)

        return

    def test_disallow_none_with_none_as_default_value(self):
        """ disallow none with none as default value """

        # fixme: This is an interesting case. Because we don't actually set the
        # value of a trait until it is accessed, an exception is *not* raised
        # at class creation time, but only when the trait is accessed. This
        # means that until this is discovered, the object is actually in an
        # internally inconsistent state. Obviously, this is plain ol' bad
        # programming but still... do we like the lazy initialization part?
        class Foo(HasTraits):
            x = self.trait_type(default_value=None, allow_none=False)

        f = Foo()
        self.failUnlessRaises(TraitError, getattr, f, 'x')
         
        return

    def test_get_traits(self):
        """ get traits """

        class Foo(HasTraits):
            x = self.trait_type

        traits = Foo.get_traits()
        self.assertEqual(len(traits), 1)
        self.assert_('x' in traits)
        self.assert_(type(traits['x']) is self.trait_type)

        return

    def test_get_inherited_traits(self):
        """ get inherited traits """

        class Foo(HasTraits):
            x = self.trait_type

        class Bar(Foo):
            y = self.trait_type
            
        traits = Bar.get_traits(inherited=False)
        self.assertEqual(len(traits), 1)
        self.assert_('y' in traits)
        self.assert_(type(traits['y']) is self.trait_type)
        
        traits = Bar.get_traits(inherited=True)
        self.assertEqual(len(traits), 2)
        self.assert_('x' in traits)
        self.assert_('y' in traits)

        return

    def test_get_trait_names(self):
        """ get trait names """

        class Foo(HasTraits):
            x = self.trait_type

        trait_names = Foo.get_trait_names()
        self.assertEqual(len(trait_names), 1)
        self.assert_('x' in trait_names)

        return

    def test_get_inherited_trait_names(self):
        """ get inherited trait names """

        class Foo(HasTraits):
            x = self.trait_type

        class Bar(Foo):
            y = self.trait_type
            
        trait_names = Bar.get_trait_names(inherited=False)
        self.assertEqual(len(trait_names), 1)
        self.assert_('y' in trait_names)
        
        trait_names = Bar.get_trait_names(inherited=True)
        self.assertEqual(len(trait_names), 2)
        self.assert_('x' in trait_names)
        self.assert_('y' in trait_names)

        return

    def test_metadata(self):
        """ metadata """

        class Foo(HasTraits):
            x = self.trait_type(transient=True)
            y = self.trait_type
            z = self.trait_type(transient=False)

        f = Foo()

        traits = f.get_traits(transient=True)
        self.assertEqual(len(traits), 1)
        self.assert_('x' in traits)

        traits = f.get_traits(transient=False)
        self.assertEqual(len(traits), 1)
        self.assert_('z' in traits)

        return

#### EOF ######################################################################
