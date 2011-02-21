from collections import deque


class QueueDispatcher:

    def __init__(self):
        self.queue = deque() 
        self.working = False
    
    def dispatch(self, signal, message):

        self.queue.append((signal, message))
        
        if self.working:
            return 
        
        queue = self.queue
        self.working = True
                
        while queue:
            op_signal, op_message = queue.popleft()
            op_signal.emit(op_message)

        self.working = False

