""" Tests to work out how to use Cython for Trait types! """


import time, unittest

from enthought.traits import api as old_traits
from martin.traits.spike.cython import cython_traits
from martin.traits.spike.cython import cython_traits_with_accessors
from martin.traits.spike.cython import cython_traits_with_getattr_hook
from martin.traits.spike.cython import python_traits
from martin.traits.spike.cython import meta_has_traits


# Old traits doesn't have a version identifier!
old_traits.VERSION = 'Traits 3'


IMPLEMENTATIONS = [
    old_traits,
    python_traits,
    cython_traits,
    cython_traits_with_accessors,
    cython_traits_with_getattr_hook
]


def set_implementation(implementation):
    """ Set the current traits implementation.

    fixme: Hack to plug the appropriate implementation into the meta
    class for 'HasTraits'...

    """
    
    meta_has_traits.MetaHasTraits.implementation = implementation

    return


def timeit(fn, N=pow(10, 6)):
    start = time.time()
    fn(N)
    stop = time.time()

    return stop - start


def print_results(results):
    for version, speed in sorted(results, key=lambda x: x[1]):
        print '%-20s' % version, '\t', speed

    return 

    
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

        results = []
        for traits in IMPLEMENTATIONS:
            # Old traits has a different API here...
            if traits is old_traits:
                continue
            
            set_implementation(traits)

            def fn(N):
                for i in range(N):
                    traits.Int().validate(i)

            results.append((traits.VERSION, timeit(fn)))

        print_results(results)
        
        return

    def test_attribute_access_speed(self):

        print

        results = []
        for traits in IMPLEMENTATIONS:
            set_implementation(traits)

            class Foo(traits.HasTraits):
                x = traits.Int()

            f = Foo()
            f.x = 42

            def fn(N):
                for i in range(N):
                    x = f.x

            results.append((traits.VERSION, timeit(fn)))

        print_results(results)
        
        return

    def test_valid_attribute_validation_speed(self):

        print

        results = []
        for traits in IMPLEMENTATIONS:
            set_implementation(traits)

            class Foo(traits.HasTraits):
                x = traits.Int()

            f = Foo()
            f.x = 42

            def fn(N):
                for i in range(N):
                    f.x = i

            results.append((traits.VERSION, timeit(fn)))
                           
        print_results(results)

        return

    def test_invalid_attribute_validation_speed(self):

        print

        results = []
        for traits in IMPLEMENTATIONS:
            set_implementation(traits)

            class Foo(traits.HasTraits):
                x = traits.Int()

            f = Foo()
            f.x = 42

            def fn(N):
                for i in range(N):
                    self.assertRaises(
                        traits.TraitError, setattr, f, 'x', 'I am not an int!'
                    )

            results.append((traits.VERSION, timeit(fn, N=pow(10, 4))))

        print_results(results)
        
        return

    def test_traits_does_not_intefere_with_other_descriptors(self):

        print
        
        for traits in IMPLEMENTATIONS:
            set_implementation(traits)

            print traits.VERSION
            
            class MyDescriptor(object):
                def __get__(self, obj, cls):
                    return obj.my_descriptor_value

                def __set(self, obj, value):
                    obj.my_descriptor_value = value
                    return
                
            class Foo(traits.HasTraits):
                y = MyDescriptor()

            f = Foo()
            f.y = 99

            self.assertEqual(99, f.y)

        return
        
#### EOF ######################################################################
