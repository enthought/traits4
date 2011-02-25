from bisect import insort
from weakref import ref, WeakKeyDictionary


class KillSignalException(Exception):
    pass


class NoneContext(object):
    
    def __repr__(self):
        return 'NoneContext'

    def __str__(self):
        return self.__repr__()

NoneContext = NoneContext()


class NotifierManager(object):
    
    __slots__ = ('_conn_count', '_notifiers', '_remove', '__weakref__')

    def __init__(self):
        self._conn_count = 0
        self._notifiers = []
        
        def remove(wr, selfref=ref(self)):
            self = selfref()
            if self is not None:
                remove_idx = []
                notifiers = self._notifiers
                for i, item in enumerate(notifiers):
                    if item[2] == wr:
                        remove_idx.append(i)
                for i in reversed(remove_idx):
                    notifiers.pop(i)

        self._remove = remove

    def add_notifier(self, notifier, priority):
        count = self._conn_count
        item = (priority, count, ref(notifier, self._remove))
        insort(self._notifiers, item)
        self._conn_count = count + 1

    def remove_notifier(self, notifier):
        self._remove(ref(notifier))

    def notifiers(self):
        return [item[2]() for item in self._notifiers]
            

class Signal(object):
    
    __slots__ = ('_mgrs', '__weakref__')

    def __init__(self):
        self._mgrs = WeakKeyDictionary()        
        
    def connect(self, notifier, priority=16, context=NoneContext):
        mgr = self._mgrs.setdefault(context, NotifierManager())
        mgr.add_notifier(notifier, priority)

    def disconnect(self, notifier, context=NoneContext):
        mgrs = self._mgrs
        if context in mgrs:
            mgr = mgrs[context]
            mgr.remove_notifier(notifier)

    def emit(self, message, context=NoneContext):
        mgrs = self._mgrs
        if context in mgrs:
            mgr = mgrs[context]
            notifiers = mgr.notifiers()
            if notifiers:
                message.initialize()
                for notifier in notifiers:
                    try:
                        notifier(message, context)
                    except KillSignalException:
                        break
                    finally:
                        message.update()
                message.finalize()

