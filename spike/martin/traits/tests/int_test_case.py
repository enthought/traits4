""" Tests 'HasTraits' functionality using the 'Int' trait type. """


# Martin library imports.
from martin.traits.api import HasTraits, Int, TraitError
    
# Local imports.
from builtin_test_case import BuiltinTestCase


def listener(obj, trait_name, old, new):
    """ A listener that remembers what it was called with! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new
    
    return


class IntTestCase(BuiltinTestCase):
    """ Tests 'HasTraits' functionality using the 'Int' trait type. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.trait_type = Int
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_default_value(self):
        """ default value (Int) """

        class Foo(HasTraits):
            x = Int
            y = Int(99)
            
        f = Foo()
        self.assertEqual(f.x, 0)
        self.assertEqual(f.y, 99)

        return

    def test_validation_on_assignment(self):
        """ validation on assignment (Int) """

        class Foo(HasTraits):
            x = Int

        f = Foo()
        f.x = 10
        self.assertEqual(f.x, 10)
        self.failUnlessRaises(TraitError, setattr, f, 'x', 'sss')

        return

    def test_validation_on_construction(self):
        """ validation on construction (Int) """

        class Foo(HasTraits):
            x = Int

        f = Foo(x=10)
        self.assertEqual(f.x, 10)
        self.failUnlessRaises(TraitError, Foo, x='sss')

        return

    def XXXtest_on_trait_change(self):
        """ on trait change (Int) """

        class Foo(HasTraits):
            x = Int

        f = Foo()

        # Hook up a listener.
        f.on_trait_change('x', listener)
        
        # Change f.x and make sure the listener got called.
        f.x = 20

        self.assertEqual(f, listener.obj)
        self.assertEqual('x', listener.trait_name)
        self.assertEqual(0, listener.old)
        self.assertEqual(20, listener.new)

        return
    
#### EOF ######################################################################
