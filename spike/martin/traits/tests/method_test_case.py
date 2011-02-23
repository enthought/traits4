""" Tests for method decorators. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, Int, TraitError, method
    

class MethodTestCase(unittest.TestCase):
    """ Tests for method decorators. """

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

    def test_docstring_on_wrapper(self):
        """ docstring on wrapper """

        class Foo(HasTraits):
            x = Int

            @method(y=Int, _returns_=Int)
            def bar(self, y):
                """ Bar it! """
                
                return self.x + y

        self.assertEqual(Foo.bar.__doc__, " Bar it! ")

        return
    
    def test_args_validation_with_trait_type_classes(self):
        """ args validation with trait type classes """

        class Foo(HasTraits):
            x = Int

            @method(y=Int, _returns_=Int)
            def bar(self, y):
                return self.x + y
            
        f = Foo(x=2)
        self.assertEqual(f.bar(8), 10)
        self.failUnlessRaises(TraitError, f.bar, 'xxx')

        return

    def test_kw_validation_with_trait_type_classes(self):
        """ kw validation with trait type classes """

        class Foo(HasTraits):
            x = Int

            @method(y=Int, _returns_=Int)
            def bar(self, **kw):
                return self.x + kw['y']
            
        f = Foo(x=2)
        self.assertEqual(f.bar(y=8), 10)
        self.failUnlessRaises(TraitError, f.bar, y='xxx')

        return

    def test_args_validation_with_trait_type_instances(self):
        """ args validation with trait type instances """

        class Foo(HasTraits):
            x = Int

            @method(y=Int(10), _returns_=Int(20))
            def bar(self, y):
                return self.x + y
            
        f = Foo(x=2)
        self.assertEqual(f.bar(8), 10)
        self.failUnlessRaises(TraitError, f.bar, 'xxx')

        return

    def test_kw_validation_with_trait_type_instances(self):
        """ kw validation with trait type instances """

        class Foo(HasTraits):
            x = Int

            @method(y=Int(10), _returns_=Int(20))
            def bar(self, **kw):
                return self.x + kw['y']
            
        f = Foo(x=2)
        self.assertEqual(f.bar(y=8), 10)
        self.failUnlessRaises(TraitError, f.bar, y='xxx')

        return

    def test_output_validation_with_trait_type_classes(self):
        """ output validation with trait type instances """

        class Foo(HasTraits):
            x = Int

            @method(y=Int, _returns_=Int)
            def bar(self, y):
                return 'xxx'
            
        f = Foo(x=2)
        self.failUnlessRaises(TraitError, f.bar, 8)

        return
    
    def test_output_validation_with_trait_type_instances(self):
        """ output validation with trait type instances """

        class Foo(HasTraits):
            x = Int

            @method(y=Int(10), _returns_=Int(20))
            def bar(self, y):
                return 'xxx'
            
        f = Foo(x=2)
        self.failUnlessRaises(TraitError, f.bar, 8)

        return

#### EOF ######################################################################
