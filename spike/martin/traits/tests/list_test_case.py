""" Tests 'HasTraits' functionality using the 'List' trait type. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, Int, List, TraitError
    
# Local imports.
from builtin_test_case import BuiltinTestCase


class ListTestCase(BuiltinTestCase):
    """ Tests 'HasTraits' functionality using the 'List' trait type. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.trait_type = List
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_default_value(self):
        """ default value (List) """

        class Foo(HasTraits):
            x = List
            y = List(default_value=[1, 2, 3])

        f = Foo()
        self.assertEqual(len(f.x), 0)
        self.assertEqual(len(f.y), 3)

        return

    def test_validation_on_assignment(self):
        """ validation on assignment (List) """

        class Foo(HasTraits):
            x = List(HasTraits)

        f = Foo()
        f.x = []
        self.failUnlessRaises(TraitError, setattr, f, 'x', 'xxx')
        self.failUnlessRaises(TraitError, setattr, f, 'x', ['xxx'])

        return

    def test_validation_on_construction(self):
        """ validation on construction (List) """

        class Foo(HasTraits):
            x = List(HasTraits)
        
        f = Foo(x=[])
        self.assertEqual(len(f.x), 0)
        self.failUnlessRaises(TraitError, Foo, x='xxx')
        self.failUnlessRaises(TraitError, Foo, x=['xxx'])

        return

    def test_class_name(self):
        """ class name """

        class Foo(HasTraits):
            x = List('martin.traits.api.HasTraits')

        f = Foo()
        self.assertEqual(f.x, [])

        return

#### EOF ######################################################################
