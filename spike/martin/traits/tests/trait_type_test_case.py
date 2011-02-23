""" Tests general 'TraitType' functionality. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import HasTraits, TraitType, TraitError
    

class TraitTypeTestCase(unittest.TestCase):
    """ Tests general 'TraitType' functionality. """

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

    def test_info_not_implemented(self):
        """ info not implemented """

        trait_type = TraitType()
        self.failUnlessRaises(NotImplementedError, trait_type.info)

        return

    def test_validate(self):
        """ validate """

        trait_type = TraitType()
        self.failUnlessRaises(TraitError, trait_type.validate, None)

        return

#### EOF ######################################################################
