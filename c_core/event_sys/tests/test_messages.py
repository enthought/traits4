from ..signals import Signal
from ..messages import Message


def test_message():
    res = []
    def cb(msg, ctxt):
        res.append(msg.contents)
    s = Signal()
    s.connect(cb)
    s.emit(Message('foo'))
    assert res[0] == 'foo'
