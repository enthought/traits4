from collections import deque
from weakref import WeakKeyDictionary
    

class BaseDispatcher(object):

    def __init__(self):
        self._notifiers = WeakKeyDictionary()

    def __call__(self, trait, obj, name, old, new):
        raise NotImplementedError
    
    def add_notifier(self, trait, obj, notifier):
        all_notifiers = self._notifiers
        if trait not in all_notifiers:
            all_notifiers[trait] = WeakKeyDictionary()
        inner = all_notifiers[trait]
        if obj not in inner:
            inner[obj] = set()
        inner[obj].add(notifier)

    def remove_notifier(self, trait, obj, notifier):
        all_notifiers = self._notifiers
        if trait in all_notifiers:
            inner = all_notifiers[trait]
            if obj in inner:
                notifiers = inner[obj]
                if notifier in notifiers:
                    notifiers.remove(notifier)
                if not notifiers:
                    del inner[obj]
            if not inner:
                del all_notifiers[trait]

    def notifiers(self, trait, obj):
        all_notifiers = self._notifiers
        if trait in all_notifiers:
            inner = all_notifiers[trait]
            if obj in inner:
                notifiers = inner[obj]
                return list(notifiers)
        return []
       

class ImmediateDispatcher(BaseDispatcher):

    def __call__(self, trait, obj, name, old, new):
        if old == new:
            return

        for notifier in self.notifiers(trait, obj):
            if not notifier(obj=obj, name=name, old=old, new=new):
                self.remove_notifier(trait, obj, notifier)


class QueueDispatcher(BaseDispatcher):
    """ This is a dispatcher which instead of notifying immediately,
    calls notifiers with changes in the order in which they occur.
    
    This is essentially 'breadth-first' dispatching.
    
    Some consequences of this:
      - each trait's set of notifiers runs to completion before any other trait
        is run
      - there is no guarantee that new is equal to the current value of the
        trait (something else may have changed the value before the current
        listener gets to run)
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.queue = deque()
        self.working = False

    def __call__(self, trait, obj, name, old, new):
        if old == new:
            return

        # add our stuff to the end of the queue
        self.queue.append((trait, obj, name, old, new))
        
        # if we're not the first caller, return immediately
        if self.working:
            return
       
        self.working = True

        # now process the queue until done
        while self.queue:
            trait, obj, name, old, new = self.queue.popleft()
            for notifier in self.notifiers(trait, obj):
                if not notifier(obj=obj, name=name, old=old, new=new):
                    self.remove_notifier(trait, obj, notifier)
                           
        self.working = False


class CollapsingQueueDispatcher(BaseDispatcher):
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
            for notifier in self.notifiers(trait, obj):
                if not notifier(obj=obj, name=name, old=old, new=new):
                    self.remove_notifier(trait, obj, notifier)

        self.working = False


class StackDispatcher(BaseDispatcher):
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
            self.insert_at = len(self.stack)
            for notifier in self.notifiers(trait, obj):
                if not notifier(obj=obj, name=name, old=old, new=new):
                    self.remove_notifier(trait, obj, notifier)
                            
        self.working = False
        self.insert_at = len(self.stack)


#------------------------------------------------------------------------------
# instances used by the traits framework
#------------------------------------------------------------------------------

_immediate_dispatcher = ImmediateDispatcher()
_queue_dispatcher = QueueDispatcher()
_collapsing_queue_dispatcher = CollapsingQueueDispatcher()
_stack_dispatcher = StackDispatcher()
