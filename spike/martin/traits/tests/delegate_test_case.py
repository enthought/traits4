""" Tests for delegates. """


# Standard library imports.
import unittest

# Martin library imports.
from martin.traits.api import Any, Delegate, HasTraits, Instance, Int
from martin.traits.api import TraitError, Undefined
    

class DelegateTestCase(unittest.TestCase):
    """ Tests for delegates. """

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

    def dont_XtestX_train_of_thought(self):
        """ possible syntax for delegation """

        class Foo(HasTraits):

            delegate(IFoo, to='_x')
            delegate(IBar, to='_y')
            delegate([IBaz, IBlargle], to='_z')

            delegate('name', to='ss')

            delegate(['x', 'y'], to='ddd')

        return
    
    def test_getter_called(self):
        """ getter called """

        class Foo(HasTraits):
            x = Int

        class Bar(HasTraits):
            f = Instance(Foo)
            x = Delegate('f')

        f = Foo(x=42)
        self.assertEqual(42, f.x)

        b = Bar(f=f)
        self.assertEqual(42, b.x)

        # Set via the delegate.
        f.x = 99
        self.assertEqual(99, f.x)
        self.assertEqual(99, b.x)

        # Set via the object.
        b.x = 50
        self.assertEqual(50, f.x)
        self.assertEqual(50, b.x)
        
        return

##     def test_setter_called(self):
##         """ setter called """
        
##         class Foo(HasTraits):
##             x = Property(Any)

##             # Shadow attribute for the property.
##             _x = Any
            
##             def __init__(self, **traits):
##                 """ Constructor. """

##                 super(Foo, self).__init__(**traits)

##                 # Used to count how many times the setter has been called.
##                 self.set_count = 0

##                 return
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self.set_count += 1

##                 self._x = x

##                 return

##         f = Foo()
##         self.assertEqual(f.set_count, 0)

##         f.x = 42
##         self.assertEqual(f.set_count, 1)

##         f.x = 'a string'
##         self.assertEqual(f.set_count, 2)

##         return

##     def test_inherited_getter_called(self):
##         """ inherited getter called """

##         class Foo(HasTraits):
##             x = Property(Any)

##             # Shadow attribute for the property.
##             _x = Any
            
##             def __init__(self, **traits):
##                 """ Constructor. """

##                 super(Foo, self).__init__(**traits)

##                 # Used to count how many times the getter has been called.
##                 self.get_count = 0

##                 return
            
##             def _get_x(self):
##                 """ Property getter. """

##                 self.get_count += 1

##                 return self._x

##         class Bar(Foo):
##             pass

##         b = Bar()
##         self.assertEqual(b.get_count, 0)

##         self.assertEqual(b.x, Undefined)
##         self.assertEqual(b.get_count, 1)

##         self.assertEqual(b.x, Undefined)
##         self.assertEqual(b.get_count, 2)

##         return

##     def test_inherited_setter_called(self):
##         """ inherited setter called """
        
##         class Foo(HasTraits):
##             x = Property(Any)

##             # Shadow attribute for the property.
##             _x = Any
            
##             def __init__(self, **traits):
##                 """ Constructor. """

##                 super(Foo, self).__init__(**traits)

##                 # Used to count how many times the setter has been called.
##                 self.set_count = 0

##                 return
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self.set_count += 1

##                 self._x = x

##                 return

##         class Bar(Foo):
##             pass

##         b = Bar()
##         self.assertEqual(b.set_count, 0)

##         b.x = 42
##         self.assertEqual(b.set_count, 1)

##         b.x = 'a string'
##         self.assertEqual(b.set_count, 2)

##         return

##     def test_getter_on_derived_class_called(self):
##         """ getter on derived class called """

##         class Foo(HasTraits):
##             x = Property(Any)

##             def _get_x(self):
##                 """ Property getter. """

##                 raise ValueError

##         class Bar(Foo):

##             # Shadow attribute for the property.
##             _x = Any
            
##             def __init__(self, **traits):
##                 """ Constructor. """

##                 super(Foo, self).__init__(**traits)

##                 # Used to count how many times the getter has been called.
##                 self.get_count = 0

##                 return
            
##             def _get_x(self):
##                 """ Property getter. """

##                 self.get_count += 1

##                 return self._x

##         b = Bar()
##         self.assertEqual(b.get_count, 0)

##         self.assertEqual(b.x, Undefined)
##         self.assertEqual(b.get_count, 1)

##         self.assertEqual(b.x, Undefined)
##         self.assertEqual(b.get_count, 2)

##         return

##     def test_setter_on_derived_class_called(self):
##         """ setter on derived class called """
        
##         class Foo(HasTraits):
##             x = Property(Any)

##             def _set_x(self, x):
##                 """ Property setter. """

##                 raise ValueError

##         class Bar(Foo):

##             # Shadow attribute for the property.
##             _x = Any
            
##             def __init__(self, **traits):
##                 """ Constructor. """

##                 super(Foo, self).__init__(**traits)

##                 # Used to count how many times the setter has been called.
##                 self.set_count = 0

##                 return
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self.set_count += 1

##                 self._x = x

##                 return

##         b = Bar()
##         self.assertEqual(b.set_count, 0)

##         b.x = 42
##         self.assertEqual(b.set_count, 1)

##         b.x = 'a string'
##         self.assertEqual(b.set_count, 2)

##         return

##     def test_any_property(self):
##         """ any property """
        
##         class Foo(HasTraits):
##             x = Property(Any)

##             # Shadow attribute for the property.
##             _x = Any
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self._x = x

##                 return

##         f = Foo()
##         self.assertEqual(f.x, Undefined)

##         f.x = 42
##         self.assertEqual(f.x, 42)

##         f.x = 'a string'
##         self.assertEqual(f.x, 'a string')

##         return

##     def test_instance_property(self):
##         """ instance property """

##         class Bar(HasTraits):
##             pass
        
##         class Foo(HasTraits):
##             x = Property(Instance(Bar))

##             # Shadow attribute for the property.
##             _x = None
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self._x = x

##                 return

##         f = Foo()
##         self.assertEqual(f.x, None)

##         b = Bar(); f.x = b
##         self.assertEqual(f.x, b)

##         self.failUnlessRaises(TraitError, setattr, f, 'x', 'a string')

##         return

##     def test_shorthand_instance_property(self):
##         """ shorthand instance property """

##         class Bar(HasTraits):
##             pass
        
##         class Foo(HasTraits):
##             x = Property(Bar)

##             # Shadow attribute for the property.
##             _x = None
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self._x = x

##                 return

##         f = Foo()
##         self.assertEqual(f.x, None)

##         b = Bar(); f.x = b
##         self.assertEqual(f.x, b)

##         self.failUnlessRaises(TraitError, setattr, f, 'x', 'a string')

##         return

##     def test_int_property(self):
##         """ int property """
        
##         class Foo(HasTraits):
##             x = Property(Int)

##             # Shadow attribute for the property.
##             _x = Int(42)
            
##             def _get_x(self):
##                 """ Property getter. """

##                 return self._x

##             def _set_x(self, x):
##                 """ Property setter. """

##                 self._x = x

##                 return

##         f = Foo()
##         self.assertEqual(f.x, 42)

##         f.x += 1
##         self.assertEqual(f.x, 43)

##         self.failUnlessRaises(TraitError, setattr, f, 'x', 'a string')

##         return

#### EOF ######################################################################
