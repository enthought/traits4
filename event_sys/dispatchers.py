from collections import deque


class Dispatcher(object):

    def dispatch(self, signal, message):
        signal.emit(message)


class QueueDispatcher(Dispatcher):

    def __init__(self):
        self.queue = deque() 
        self.working = False
    
    def dispatch(self, signal, message):
        queue = self.queue
        queue.append((signal, message))
        
        if self.working:
            return 
        
        self.working = True
                
        while queue:
            op_signal, op_message = queue.popleft()
            op_signal.emit(op_message)

        self.working = False


class StackDispatcher(Dispatcher):

    def __init__(self):
        self.stack = []
        self.working = False

    def dispatch(self, signal, message):
        stack = self.stack
        stack.append((signal, message))

        if self.working:
            return 

        self.working = True

        while stack:
            op_signal, op_message = stack.pop()
            op_signal.emit(op_message)

        self.working = False


