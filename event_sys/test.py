from signals import Signal, KillSignalException
from dispatchers import QueueDispatcher
from messages import Message


dispatcher = QueueDispatcher()

s1 = Signal()
s2 = Signal()
s3 = Signal()

def s1p(msg):
    print 's1'
    dispatcher.dispatch(s3, msg)
    dispatcher.dispatch(s2, msg)

def s2p(msg):
    print 's2'
    dispatcher.dispatch(s3, msg)

def s3p(msg):
    print 's3'
    print msg

s1.connect(s1p)
s2.connect(s2p)
s3.connect(s3p)

dispatcher.dispatch(s1, Message('foo'))


def printer1(msg):
    print 'printer 1'

def printer2(msg):
    print 'printer 2'

def printer3(msg):
    print 'printer 3'
    raise KillSignalException

s4 = Signal()

s4.connect(printer3, priority=5)
s4.connect(printer2, priority=6)
s4.connect(printer1, priority=4)


s4.emit(Message('foo'))
