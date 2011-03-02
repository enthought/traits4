""" Tests to work out how to use Cython! """


import time, unittest


from martin.traits.spike.cython.cython_lab import Foo


class CythonLabTestCase(unittest.TestCase):
    """ Tests to work out how to use Cython! """

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

    def test_construction(self):

        f = Foo()

        self.assertEqual(0, len(f.d))
        self.assertEqual(0, len(f.l))
        self.assertEqual(None, f.o)
        self.assertEqual(0, len(f.u))
        
        return

#### EOF ######################################################################
