import unittest
from traits import *


class Foo(HasTraits):
    a = Int
    b = Int(lambda *args: 20)
    c = Int

    @on_trait_change('c')
    def printer(self, obj, name, old, new):
        self.testcase.assertEquals(obj, self)
        self.testcase.assertEquals(name, 'c')
        self.testcase.assertEquals(old, 0)
        self.testcase.assertEquals(new, 12)
        self.testcase.class_listener_fired = True


def printer(*args):
    print 'dynamic printer', args


class BasicTraitsTestCase(unittest.TestCase):
    def test_default(self):
        f = Foo()
        self.assertEquals(f.a, 0)
        self.assertEquals(f.b, 20)

    def test_initialize(self):
        f = Foo(a=12)
        self.assertEquals(f.a, 12)

    def test_set(self):
        f = Foo()
        f.a = 12
        self.assertEquals(f.a, 12)

    def test_reset(self):
        f = Foo(b=40)
        f.a = 12        
        
        self.assertEquals(f.a, 12)        
        del f.a
        self.assertEquals(f.a, 0)

        del f.b
        self.assertEquals(f.b, 20)


    def listener(self, new, old, name, obj):
        self.assertEquals(obj, self.f)
        self.assertEquals(name, 'a')
        self.assertEquals(old, 0)
        self.assertEquals(new, 12)
        self.listener_fired = True

    def test_listener(self):
        self.listener_fired = False
        f = Foo()
        self.f = f
        f.on_trait_change('a', self.listener)
        f.a = 12
        self.assertTrue(self.listener_fired)


    def test_class_listener(self):
        self.class_listener_fired = False
        f = Foo()
        f.testcase = self   # bit of a hack
        f.c = 12
        self.assertTrue(self.class_listener_fired)

    
    def bad_assignment(self):
        f = Foo()
        f.a = 'k'
        
    def test_validation(self):
        self.assertRaises(ValidationError, self.bad_assignment) # will raise ValidationError

if __name__ == '__main__':
    unittest.main()
