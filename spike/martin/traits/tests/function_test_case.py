""" Tests for function decorators. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, Int, TraitError, function
    

class FunctionTestCase(unittest.TestCase):
    """ Tests for function decorators. """

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

        @function(x=Int, y=Int, _returns_=Int)
        def add(x, y):
            """ Add two numbers """
            
            return x + y

        self.assertEqual(add.__doc__, " Add two numbers ")

        return
    
    def test_args_validation_with_trait_type_classes(self):
        """ args validation with trait type classes """

        @function(x=Int, y=Int, _returns_=Int)
        def add(x, y):
            return x + y

        self.assertEqual(add(8, 2), 10)
        self.failUnlessRaises(TraitError, add, 2, 'xxx')

        return

    def test_kw_validation_with_trait_type_classes(self):
        """ kw validation with trait type classes """

        @function(x=Int, y=Int, _returns_=Int)
        def add(**kw):
            return kw['x'] + kw['y']

        self.assertEqual(add(x=8, y=2), 10)
        self.failUnlessRaises(TraitError, add, x=2, y='xxx')

        return

    def test_args_validation_with_trait_type_instances(self):
        """ args validation with trait type instances """

        @function(x=Int(10), y=Int(20), _returns_=Int(30))
        def add(x, y):
            return x + y

        self.assertEqual(add(8, 2), 10)
        self.failUnlessRaises(TraitError, add, 2, 'xxx')

        return

    def test_kw_validation_with_trait_type_instances(self):
        """ kw validation with trait type instances """

        @function(x=Int(10), y=Int(20), _returns_=Int(30))
        def add(**kw):
            return kw['x'] + kw['y']

        self.assertEqual(add(x=8, y=2), 10)
        self.failUnlessRaises(TraitError, add, x=2, y='xxx')

        return

    def test_return_validation_with_trait_type_classes(self):
        """ return validation with trait type instances """

        @function(x=Int, y=Int, _returns_=Int)
        def add(x, y):
            return 'xxx'

        self.failUnlessRaises(TraitError, add, 2, 8)

        return
    
    def test_return_validation_with_trait_type_instances(self):
        """ return validation with trait type instances """

        @function(x=Int(10), y=Int(20), _returns_=Int(30))
        def add(x, y):
            return 'xxx'

        self.failUnlessRaises(TraitError, add, 2, 8)

        return

#### EOF ######################################################################
