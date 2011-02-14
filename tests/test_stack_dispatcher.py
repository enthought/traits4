import unittest
import notifiers
from stack_dispatcher import _stack_dispatcher

from test_traits import *

class Bar(HasTraits):
    a = Int(dispatcher=_stack_dispatcher)
    b = Int(dispatcher=_stack_dispatcher)
    c = Int(dispatcher=_stack_dispatcher)
    d = Int(dispatcher=_stack_dispatcher)

class TestStackDispatcher(unittest.TestCase):

    def a_listener(self, obj, new):
        self.order.append('a')
        obj.b = new+1
        obj.c = new+2

    def b_listener(self, obj, new):
        self.order.append('b')
        obj.d = new+3

    def c_listener(self, obj, new):
        self.order.append('c')

    def d_listener(self, obj, new):
        self.order.append('d')
        
    def test_order(self):
        self.order = []
        f = Bar()
        f.on_trait_change('a', self.a_listener)
        f.on_trait_change('b', self.b_listener)
        f.on_trait_change('c', self.c_listener)
        f.on_trait_change('d', self.d_listener)
        f.a = 1
        self.assertEquals(self.order, ['a', 'b', 'd', 'c'])
    

if __name__ == '__main__':
    unittest.main()

