from weakref import ref, WeakKeyDictionary
from collections import deque

from notifiers import Dispatcher


class CollapsingQueueDispatcher(Dispatcher):
    """ This is a dispatcher which instead of notifying immediately,
    calls notifiers with changes in the order in which they occur.
    In addition, if the same trait is changed twice, it combines the changes
    into one event, forgetting the intermediate value.
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.queue = deque()
        self.values = {}
        self.working = False

    def __call__(self, trait, obj, name, old, new):
        if old == new:
            return
        
        # has this been messed with before?
        if (trait, obj, name) in self.values:
            old, new1 = self.values[(trait, obj, name)]
            self.queue.remove((trait, obj, name, old, new1))

        # add our stuff to the end of the queue and our values dict
        self.queue.append((trait, obj, name, old, new))
        self.values[(trait, obj, name)] = (old, new)
        
        if self.working:
            return
        
        self.working = True

        # now process the queue until done
        while self.queue:
            trait, obj, name, old, new = self.queue.popleft()
            del self.values[(trait, obj, name)]
            all_notifiers = self.notifiers
            if trait in all_notifiers:
                inner = all_notifiers[trait]
                if obj in inner:
                    notifiers = inner[obj]
                    dead_notifiers = []
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

_collapsing_queue_dispatcher = CollapsingQueueDispatcher()
