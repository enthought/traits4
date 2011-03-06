from bisect import insort
from weakref import ref, WeakKeyDictionary


__all__ = ['KillSignalException', 'NoneContext', 'Signal']


class KillSignalException(Exception):
    pass


class NoneContext(object):
    
    __slots__ = ('__weakref__')

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()

NoneContext = NoneContext()


class _NotifierManager(object):
    
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
            

class _BlockingManager(object):
    
    __slots__ = ('_blocked_notifiers', '_notifier_stack')

    def __init__(self):
        self._blocked_notifiers = set()
        self._notifier_stack = []
    
    def __call__(self, *notifiers):
        self.block(*notifiers)
        self._notifier_stack.append(notifiers)
        return self

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        stack = self._notifier_stack
        if stack:
            self.unblock(*stack.pop())

    def block(self, *notifiers):
        self._blocked_notifiers.update(notifiers)

    def unblock(self, *notifiers):
        self._blocked_notifiers.difference_update(notifiers)

    def is_blocked(self, notifier):
        return notifier in self._blocked_notifiers


class _ContextManager(object):

    __slots__ = ('current', '_ctxt_stack')

    def __init__(self, default):
        self.current = default
        self._ctxt_stack = []

    def __call__(self, ctxt):
        self._ctxt_stack.append(self.current)
        self.current = ctxt
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        stack = self._ctxt_stack
        if stack:
            self.current = stack.pop()

    
class Signal(object):
    
    __slots__ = ('blocking', 'context', '_mgrs', '__weakref__')

    def __init__(self, default_context=NoneContext):
        self.blocking = _BlockingManager()
        self.context = _ContextManager(default_context)
        self._mgrs = WeakKeyDictionary()
        
    def block(self, *notifiers):
        self.blocking.block(*notifiers)

    def unblock(self, *notifiers):
        self.blocking.unblock(*notifiers)

    def connect(self, notifier, priority=16):
        self._mgr.add_notifier(notifier, priority)

    def disconnect(self, notifier):
        self._mgr.remove_notifier(notifier)

    def emit(self, message):
        notifiers = self._mgr.notifiers()
        if notifiers:
            message.signal = self
            message.initialize()
            is_blocked = self.blocking.is_blocked
            for notifier in notifiers:
                if is_blocked(notifier):
                    continue
                else:
                    try:
                       notifier(message)
                    except KillSignalException:
                        break
                    finally:
                        message.update()
            message.finalize()
            message.signal = None
    
    @property
    def _mgr(self):
        ctxt = self.ctxt
        mgrs = self._mgrs

        if ctxt in mgrs:
            res = mgrs[ctxt]
        else:
            res = _NotifierManager()
            mgrs[ctxt] = res

        return res

    @property
    def ctxt(self):
        return self.context.current

