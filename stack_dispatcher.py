from weakref import ref, WeakKeyDictionary
from notifiers import Dispatcher

class StackDispatcher(Dispatcher):
    """ This is a dispatcher which waits for each handler to finish before
    invoking the next.  The call order remains the same as it would under
    traits 3.
    
    This is essentially 'depth-first' calling.
    """

    def __init__(self):
        import collections
        self.notifiers = WeakKeyDictionary()
        self.queue = []
        self.working = False
        self.insert_at = 0

    def __call__(self, trait, obj, name, old, new):
        if old == new:
            return
        # add our stuff to the front of the queue
        self.queue.insert(self.insert_at, (trait, obj, name, old, new))
        
        # if we're not the first caller, return immediately
        if self.working:
            self.insert_at += 1
            return
        
        # now process the queue until done
        while self.queue:
            self.working = True
            trait, obj, name, old, new = self.queue.pop(0)
            all_notifiers = self.notifiers
            if trait in all_notifiers:
                inner = all_notifiers[trait]
                if obj in inner:
                    notifiers = inner[obj]
                    dead_notifiers = []
                    self.insert_at = 0
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
        self.insert_at = 0

_stack_dispatcher = StackDispatcher()