import unittest

from ..dispatchers import (_immediate_dispatcher, _queue_dispatcher,
                           _collapsing_queue_dispatcher, _stack_dispatcher)
from ..traits import HasTraits, Int


class Foo(HasTraits):
    a = Int(dispatcher=_immediate_dispatcher)
    b = Int(dispatcher=_immediate_dispatcher)
    c = Int(dispatcher=_immediate_dispatcher)
    d = Int(dispatcher=_immediate_dispatcher)


class TestImmediateDispatcher(unittest.TestCase):

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
        f = Foo()
        f.on_trait_change('a', self.a_listener)
        f.on_trait_change('b', self.b_listener)
        f.on_trait_change('c', self.c_listener)
        f.on_trait_change('d', self.d_listener)
        f.a = 1
        self.assertEquals(self.order, ['a', 'b', 'd', 'c'])


class Bar(HasTraits):
    a = Int(dispatcher=_queue_dispatcher)
    b = Int(dispatcher=_queue_dispatcher)
    c = Int(dispatcher=_queue_dispatcher)
    d = Int(dispatcher=_queue_dispatcher)


class TestQueueDispatcher(unittest.TestCase):

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
        self.assertEquals(self.order, ['a', 'b', 'c', 'd'])


class Baz(HasTraits):
    a = Int(dispatcher=_collapsing_queue_dispatcher)
    b = Int(dispatcher=_collapsing_queue_dispatcher)
    c = Int(dispatcher=_collapsing_queue_dispatcher)
    d = Int(dispatcher=_collapsing_queue_dispatcher)


class TestCollapsingQueueDispatcher(unittest.TestCase):
    
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
        f = Baz()
        f.on_trait_change('a', self.a_listener)
        f.on_trait_change('b', self.b_listener)
        f.on_trait_change('c', self.c_listener)
        f.on_trait_change('d', self.d_listener)
        f.a = 1
        self.assertEquals(self.order, ['a', 'b', 'c', 'd'])


class Spam(HasTraits):
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
        f = Spam()
        f.on_trait_change('a', self.a_listener)
        f.on_trait_change('b', self.b_listener)
        f.on_trait_change('c', self.c_listener)
        f.on_trait_change('d', self.d_listener)
        f.a = 1
        self.assertEquals(self.order, ['a', 'b', 'd', 'c'])
 
