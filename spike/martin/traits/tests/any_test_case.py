""" Tests 'HasTraits' functionality using the 'Any' trait type. """


# Martin library imports.
from martin.traits.api import Any, HasTraits, Undefined
    
# Local imports.
from builtin_test_case import BuiltinTestCase


class AnyTestCase(BuiltinTestCase):
    """ Tests 'HasTraits' functionality using the 'Any' trait type. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.trait_type = Any

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_default_value(self):
        """ default value (Any) """

        class Foo(HasTraits):
            x = Any
            y = Any('hello')
            z = Any(default_value=[1, 2, 3])

        f = Foo()
        self.assertEqual(f.x, Undefined)
        self.assertEqual(f.y, 'hello')
        self.assertEqual(len(f.z), 3)

        return

    def test_validation_on_assignment(self):
        """ validation on assignment (Any) """

        class Foo(HasTraits):
            x = Any
            y = Any
            z = Any

        f = Foo()

        f.x = 1.0
        f.y = 'hello'
        f.z = [1, 2, 3]
        
        self.assertEqual(f.x, 1.0)
        self.assertEqual(f.y, 'hello')
        self.assertEqual(len(f.z), 3)
        
        return

    def test_validation_on_construction(self):
        """ validation on consruction (Any) """

        class Foo(HasTraits):
            x = Any
            y = Any
            z = Any

        f = Foo(x=1.0, y='hello', z=[1, 2, 3])

        self.assertEqual(f.x, 1.0)
        self.assertEqual(f.y, 'hello')
        self.assertEqual(len(f.z), 3)
        
        return

#### EOF ######################################################################
