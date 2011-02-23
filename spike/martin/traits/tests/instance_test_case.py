""" Tests 'HasTraits' functionality using the 'Instance' trait type. """


# Martin library imports.
from martin.traits.api import HasTraits, Instance, Int, Interface, TraitError
from martin.traits.api import Undefined, implements

    
# Local imports.
from builtin_test_case import BuiltinTestCase


class InstanceTestCase(BuiltinTestCase):
    """ Tests 'HasTraits' functionality using the 'Instance' trait type. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.trait_type = Instance
        
        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_default_value(self):
        """ default value (Instance) """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar)

        f = Foo()
        self.assertEqual(f.x, Undefined)

        return

    def test_default_value_when_allow_none(self):
        """ default value when allow none """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar, allow_none=True)

        f = Foo()
        self.assertEqual(f.x, None)

        return

    def test_default_value_is_instance(self):
        """ default value is instance """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar, Bar(z=45))

        f = Foo()
        self.assertNotEqual(f.x, None)
        self.assertEqual(type(f.x), Bar)
        self.assertEqual(f.x.z, 45)

        g = Foo()
        self.assert_(g.x is f.x)

        return

    def test_default_value_with_empty_constructor(self):
        """ default value with empty constructor """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar, ())

        f = Foo()
        self.assertNotEqual(f.x, None)
        self.assertEqual(type(f.x), Bar)
        self.assertEqual(f.x.z, 42)

        g = Foo()
        self.assert_(g.x is not f.x)

        return

    def test_default_value_with_empty_constructor_when_allow_none(self):
        """ default value with empty constructor when allow none """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar, (), allow_none=True)

        f = Foo()
        self.assertNotEqual(f.x, None)
        self.assertEqual(type(f.x), Bar)
        self.assertEqual(f.x.z, 42)

        return

    # fixme: We can't do keyword arguments to the constructor!!!!!!!
    def test_default_value_with_constructor_arguments(self):
        """ default value with constructor areguments """

        class Bar(HasTraits):
            z = Int(42)

        class Foo(HasTraits):
            x = Instance(Bar, ())

        f = Foo()
        self.assertNotEqual(f.x, None)
        self.assertEqual(type(f.x), Bar)
        self.assertEqual(f.x.z, 42)

        return

    def test_validation_on_assignment(self):
        """ validation on assignment (Instance) """

        class Bar(HasTraits):
            pass

        class Baz(HasTraits):
            pass
        
        class Foo(HasTraits):
            x = Instance(Bar)

        f = Foo()
        f.x = Bar()
        self.failUnlessRaises(TraitError, setattr, f, 'x', 'sss')
        self.failUnlessRaises(TraitError, setattr, f, 'x', Baz())

        return

    # fixme: this is the only place that interfaces are tested!
    def test_validation_on_construction(self):
        """ validation on construction (Instance) """

        class IBar(Interface):
            y = Int

        class Foo(HasTraits):
            x = Instance(IBar)

        class Bar(HasTraits):
            implements(IBar)

        class Baz(HasTraits):
            pass
        
        f = Foo(x=Bar(y=10))
        self.assertEqual(f.x.y, 10)
        self.failUnlessRaises(TraitError, Foo, x=Baz())

        return

    def test_class_name(self):
        """ class name """

        class Foo(HasTraits):
            x = Instance('martin.traits.api:HasTraits')

        f = Foo()
        self.assertEqual(f.x, Undefined)

        f.x = f
        self.assertEqual(f.x, f)

        return

    def test_unicode_class_name(self):
        """ unicode class name """

        class Foo(HasTraits):
            x = Instance(u'martin.traits.api:HasTraits')

        f = Foo()
        self.assertEqual(f.x, Undefined)

        f.x = f
        self.assertEqual(f.x, f)

        return

#### EOF ######################################################################
