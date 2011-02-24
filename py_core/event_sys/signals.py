from bisect import insort
from weakref import ref, WeakKeyDictionary


class KillSignalException(Exception):
    pass


class _NullContext(object):
    pass

_null_context = _NullContext()


class NotifierManager(object):
    
    def __init__(self):
        self._conn_count = 0
        self._notifiers = []

    def _dead_notifier(self, wr):
        remove = []
        notifiers = self._notifiers
        
        for i, item in enumerate(notifiers):
            if item[2] == wr:
                remove.append(i)

        for i in reversed(remove):
            notifiers.pop(i)

    def add_notifier(self, notifier, priority):
        count = self._conn_count
        item = (priority, count, ref(notifier, self._dead_notifier))
        insort(self._notifiers, item)
        self._conn_count = count + 1

    def remove_notifier(self, notifier):
        self._dead_notifier(ref(notifier))

    def notifiers(self):
        return [item[2]() for item in self._notifiers]
            

class Signal(object):

    def __init__(self):
        self._mgrs = WeakKeyDictionary()

    def connect(self, notifier, priority=16, context=_null_context):
        mgrs = self._mgrs

        if context not in mgrs:
            mgr = NotifierManager()
            mgrs[context] = mgr
        else:
            mgr = mgrs[context]

        mgr.add_notifier(notifier, priority)

    def disconnect(self, notifier, context=_null_context):
        mgrs = self._mgrs

        if context in mgrs:
            mgr = mgrs[context]
            mgr.remove_notifier(notifier)

    def emit(self, message, context=_null_context):
        mgrs = self._mgrs

        if context in mgrs:
            mgr = mgrs[context]
            notifiers = mgr.notifiers()
        
            if notifiers:
                message.initialize()
            
                if context is _null_context:
                
                    for notifier in notifiers:
                        try:
                            notifier(message)
                        except KillSignalException:
                            break
                        finally:
                            message.update()

                else:

                    for notifier in notifiers:
                        try:
                            notifier(context, message)
                        except KillSignalException:
                            break
                        finally:
                            message.update()
                
                message.finalize()

