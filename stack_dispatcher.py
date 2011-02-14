from weakref import ref, WeakKeyDictionary
from notifiers import Dispatcher
from collections import deque


class StackDispatcher(Dispatcher):
    """ This is a dispatcher which waits for each handler to finish before
    invoking the next.  The call order remains the same as it would under
    traits 3.
    
    This is essentially 'depth-first' calling.
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.stack = []
        self.insert_at = len(self.stack)
        self.working = False
    
    def __call__(self, trait, obj, name, old, new):
        if old == new:
            return
        
        self.stack.insert(self.insert_at, (trait, obj, name, old, new))

        if self.working:
            self.insert_at -= 1
            return 

        self.working = True

        while self.stack:
            trait, obj, name, old, new = self.stack.pop()
            all_notifiers = self.notifiers
            if trait in all_notifiers:
                inner = all_notifiers[trait]
                if obj in inner:
                    notifiers = inner[obj]
                    dead_notifiers = []
                    self.insert_at = len(self.stack)
                    for notifier in notifiers:
                        if not notifier(obj=obj, name=name, old=old, new=new):
                            dead_notifiers.append(notifier)
                    if dead_notifiers:
                        for notifier in dead_notifiers:
                            notifiers.remove(notifier)
                        if not notifiers:
                            del inner[obj]
                            if not inner:
                                del all_notifiers[trait]
        
        self.working = False
        self.insert_at = len(self.stack)

_stack_dispatcher = StackDispatcher()
