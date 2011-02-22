""" Tests for interfaces. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, Interface, implements
    
    
class InterfaceTestCase(unittest.TestCase):
    """ Tests for interfaces. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_cannot_instantiate(self):
        """ cannot instantiate """

        class IFoo(Interface):
            pass

        self.failUnlessRaises(ValueError, IFoo)
        
        return

    def test_cannot_inherit_from_non_interface(self):
        """ cannot inherit from non-interface """

        class Bar(HasTraits):
            pass
        
        class IFoo(Interface):
            pass

        try:
            class IBar(IFoo, Bar):
                pass

            # The class definition itself should raise a 'ValueError' exception
            # so if we get here it failed!
            self.fail('Interface inherited from implementation!')
            
        except ValueError:
            pass
        
        return
    
    def test_no_bases(self):
        """ no bases """

        class IFoo(Interface):
            pass
        
        bases = IFoo.get_bases()
        self.assertEqual(len(bases), 0)

        return

    def test_single_base(self):
        """ single base """

        class IFoo(Interface):
            pass

        class IBar(IFoo):
            pass

        class IBaz(IBar):
            pass
        
        bases = IBar.get_bases()
        self.assertEqual(len(bases), 1)
        self.assert_(IFoo in bases)

        return

    def test_single_base_with_inheritance(self):
        """ single base with inheritance """

        class IFoo(Interface):
            pass

        class IBar(IFoo):
            pass

        class IBaz(IBar):
            pass
        
        bases = IBaz.get_bases()
        self.assertEqual(len(bases), 1)
        self.assert_(IBar in bases)

        return

    def test_multiple_bases(self):
        """ multiple bases """

        class IFoo(Interface):
            pass

        class IBar(Interface):
            pass

        class IBaz(IFoo, IBar):
            pass
        
        bases = IBaz.get_bases()
        self.assertEqual(len(bases), 2)
        self.assert_(IFoo in bases)
        self.assert_(IBar in bases)

        return

    def test_implements(self):
        """ implements """

        class IFoo(Interface):
            pass

        class Foo(HasTraits):
            implements(IFoo)

        self.assert_(Foo.implements(IFoo))

        return

    def test_implements_via_class_inheritance(self):
        """ implements via class inheritance """

        class IFoo(Interface):
            pass

        class Foo(HasTraits):
            implements(IFoo)

        class Bar(Foo):
            pass

        self.assert_(Bar.implements(IFoo))

        return

    def test_implements_via_interface_inheritance(self):
        """ implements via interface inheritance """

        class IFoo(Interface):
            pass

        class IBar(IFoo):
            pass
        
        class Foo(HasTraits):
            pass

        class Bar(Foo):
            implements(IBar)

        self.assert_(not Foo.implements(IFoo))
        self.assert_(Bar.implements(IFoo))
        self.assert_(Bar.implements(IBar))

        return
        
    def test_implements_using_classes(self):
        """ implements using classes  """

        class IFoo(Interface):
            pass

        class FooSuper(HasTraits):
            pass

        class Foo(FooSuper):
            implements(IFoo)

        class FooSub(Foo):
            pass

        self.assert_(not FooSuper.implements(IFoo))
        self.assert_(Foo.implements(IFoo))
        self.assert_(FooSub.implements(IFoo))

        class IBar(Interface):
            pass
        
        class Bar(Foo):
            implements(IBar)
            
        self.assert_(Bar.implements(IFoo))
        self.assert_(Bar.implements(IBar))

        return

    def test_implements_using_instance(self):
        """ implements using instances  """
        
        class IFoo(Interface):
            pass

        class FooSuper(HasTraits):
            pass

        class Foo(FooSuper):
            implements(IFoo)

        class FooSub(Foo):
            pass

        foo_super = FooSuper()
        foo       = Foo()
        foo_sub   = FooSub()
        
        self.assert_(not foo_super.implements(IFoo))
        self.assert_(foo.implements(IFoo))
        self.assert_(foo_sub.implements(IFoo))

        class IBar(Interface):
            pass
        
        class Bar(Foo):
            implements(IBar)

        bar = Bar()
        
        self.assert_(bar.implements(IFoo))
        self.assert_(bar.implements(IBar))

        return
    
#### EOF ######################################################################
