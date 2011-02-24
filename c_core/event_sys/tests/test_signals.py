from ..signals import Signal, KillSignalException
from ..messages import Message


def test_signal():
    called_msg = []
    def cb(msg):
        called_msg.append(msg)
    s = Signal()
    s.connect(cb)
    msg = Message()
    s.emit(msg)
    assert called_msg[0] is msg


def test_connect_priority():
    res = []
    def cb1(msg):
        res.append('a')
    def cb2(msg):
        res.append('b')
    def cb3(msg):
        res.append('c')
    s = Signal()
    s.connect(cb1, priority=4)
    s.connect(cb2, priority=5)
    s.connect(cb3, priority=6)

    s.emit(Message())

    assert res == ['a', 'b', 'c']

    s.disconnect(cb2)
    s.disconnect(cb3)
    s.connect(cb3, priority=3)
    s.connect(cb2, priority=0)

    s.emit(Message())

    assert res == ['a', 'b', 'c', 'b', 'c', 'a']


def test_auto_disconnect():
    res = []
    def cb(msg):
        res.append('foo')
    s = Signal()
    s.connect(cb)
    s.emit(Message())
    s.emit(Message())
    del cb
    s.emit(Message())
    assert res == ['foo', 'foo']


def test_total_disconnect():
    res = []
    def cb(msg):
        res.append('foo')
    s = Signal()
    s.connect(cb)
    s.connect(cb)
    s.connect(cb)
    s.emit(Message())
    s.disconnect(cb)
    s.emit(Message())
    assert res == ['foo', 'foo', 'foo']


def test_context():
    class Foo(object): pass
    
    ctxt = Foo()
    res = []
    def cb(ctx, msg):
        res.append(ctx)
    s = Signal()
    s.connect(cb, context=ctxt)
    s.emit(Message(), context=ctxt)
    assert res[0] is ctxt


def test_bound_method_no_call():
    res = []

    class Foo(object):
        def cb(self, msg):
            res.append(msg)

    f = Foo()
    s = Signal()
    s.connect(f.cb)
    s.emit(Message())
    assert not res


def test_bound_method_context():
    res = []
    msg = Message()

    class Foo(object):
        def cb(self, msg):
            res.append(msg)

    def cb(msg):
        res.append('foo')

    f = Foo()
    s = Signal()
    s.connect(f.cb.im_func, context=f)
    s.connect(cb)

    s.emit(msg, context=f)
    assert res == [msg]

    s.emit(msg)
    assert res == [msg, 'foo']


