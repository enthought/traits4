""" Tests general 'HasTraits' functionality. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, Int
    

class HasTraitsTestCase(unittest.TestCase):
    """ Tests general 'HasTraits' functionality. """

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

    def test_attribute_error(self):
        """ attribute error """

        class Foo(HasTraits):
            x = Int

        f = Foo()
        self.failUnlessRaises(AttributeError, getattr, f, 'xxx')

        return

    def test_set_non_trait(self):
        """ set non-trait """

        class Foo(HasTraits):
            x = Int

        f = Foo()
        f.y = 'xxx'
        self.assertEqual(f.y, 'xxx')

        return

#### EOF ######################################################################
