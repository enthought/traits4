from ..signals import Signal
from ..messages import Message
from ..dispatchers import Dispatcher, QueueDispatcher, StackDispatcher


class TestDispatchers(object):

    def runner(self, dispatcher):
        res = []

        s1 = Signal()
        s2 = Signal()
        s3 = Signal()

        def cb1(msg):
            res.append('foo')
            dispatcher.dispatch(s2, msg)
            dispatcher.dispatch(s3, msg)
            res.append('foo2')

        def cb2(msg):
            res.append('bar')
            dispatcher.dispatch(s3, msg)
            res.append('bar2')

        def cb3(msg):
            res.append('baz')

        s1.connect(cb1)
        s2.connect(cb2)
        s3.connect(cb3)

        dispatcher.dispatch(s1, Message())

        return res 

    def test_dispatcher(self):
        dispatcher = Dispatcher()
        res = self.runner(dispatcher)
        assert res == ['foo', 'bar', 'baz', 'bar2', 'baz', 'foo2']
        
    def test_queue_dispatcher(self):
        dispatcher = QueueDispatcher()
        res = self.runner(dispatcher)
        assert res == ['foo', 'foo2', 'bar', 'bar2', 'baz', 'baz']
        
    def test_stack_dispatcher(self):
        dispatcher = StackDispatcher()
        res = self.runner(dispatcher)
        assert res == ['foo', 'foo2', 'baz', 'bar', 'bar2', 'baz']


