""" Tests to work out how to use Cython for Trait types! """


import time, unittest

from martin.traits.spike.cython import cython_traits
from martin.traits.spike.cython import python_traits
from martin.traits.spike.cython import meta_has_traits


class TraitsTestCase(unittest.TestCase):
    """ Tests to work out how to use Cython for Trait types! """

    __test__ = False
    
    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        # fixme: Hack to plug the appropriate implementation into the meta
        # class for 'HasTraits'...
        meta_has_traits.MetaHasTraits.implementation = self.implementation

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_standalone_validation_speed(self):
        
        def timeit(trait_type, N=pow(10, 6)):
            start = time.time()
            for i in range(N):
                trait_type.validate(i)
            stop = time.time()

            return stop - start

        print
        print self.implementation.VERSION, 'took',
        print timeit(self.implementation.Int())

        return

    def test_attribute_access_speed(self):

        class Foo(self.implementation.HasTraits):
            x = self.implementation.Int()

        f = Foo()
        f.x = 42

        def timeit(N=pow(10, 6)):
            start = time.time()
            for i in range(N):
                x = f.x
            stop = time.time()

            return stop - start

        print
        print self.implementation.VERSION, 'took', timeit()

        return

    def test_attribute_validation_speed(self):

        class Foo(self.implementation.HasTraits):
            x = self.implementation.Int()

        f = Foo()
        f.x = 42

        def timeit(N=pow(10, 6)):
            start = time.time()
            for i in range(N):
##                 try:
##                     f.x = 'X'

##                 except self.implementation.TraitError:
##                     pass
                f.x = 10
            stop = time.time()

            return stop - start

        print
        print self.implementation.VERSION, 'took', timeit()

        self.failUnlessRaises(
            self.implementation.TraitError, setattr, f, 'x', 'I am not an int!'
        )
            
        return


class PythonTraitsTestCase(TraitsTestCase):
    """ Tests to work out how to use Cython for Trait types! """

    __test__ = True

    # The traits implementation to test.
    implementation = python_traits


class CythonTraitsTestCase(TraitsTestCase):
    """ Tests to work out how to use Cython for Trait types! """

    __test__ = True

    # The traits implementation to test.
    implementation = cython_traits
    
#### EOF ######################################################################
