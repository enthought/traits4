""" Tests to work out how to use Cython for Trait types! """


import unittest

from martin.traits.spike.cython import cython_traits
from martin.traits.spike.cython import python_traits
from martin.traits.spike.cython import meta_has_traits


# Implementations!
implementations = [cython_traits, python_traits]


class TraitsTestCase(unittest.TestCase):
    """ Tests to work out how to use Cython for Trait types! """

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

    def test_standalone_validation_speed(self):

        print
        
        def timeit(trait_type, N=pow(10, 6)):
            import time

            start = time.time()
            for i in range(N):
                trait_type.validate(i)
            stop = time.time()

            return stop - start

        for module in implementations:
            result = timeit(module.Int())
            print module.VERSION, 'took', result

        return

    def test_attribute_access_speed(self):

        print
        
        for module in implementations:
            meta_has_traits.MetaHasTraits.implementation = module

            class Foo(module.HasTraits):
                x = module.Int()

            f = Foo()
            f.x = 42

            def timeit(N=pow(10, 6)):
                import time

                start = time.time()
                for i in range(N):
                    x = f.x
                stop = time.time()

                return stop - start

            print module.VERSION, 'took', timeit()

        return

    def test_attribute_validation_speed(self):

        print
        
        for module in implementations:
            meta_has_traits.MetaHasTraits.implementation = module

            class Foo(module.HasTraits):
                x = module.Int()

            f = Foo()
            f.x = 42

            def timeit(N=pow(10, 6)):
                import time

                start = time.time()
                for i in range(N):
##                     try:
##                         f.x = 'X'

##                     except module.TraitError:
##                         pass
                    f.x = 10
                stop = time.time()

                return stop - start

            print module.VERSION, 'took', timeit()
            self.failUnlessRaises(
                module.TraitError, setattr, f, 'x', 'I am not an int!'
            )
            
        return
    
#### EOF ######################################################################
