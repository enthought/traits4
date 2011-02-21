from weakref import ref
from heapq import heappush, nsmallest


class KillSignalException(Exception):
    pass


class Signal(object):

    def __init__(self):
        self.heap = []
        self.conn_count = 0

    def connect(self, notifier, priority=16):
        count = self.conn_count
        heappush(self.heap, (priority, count, ref(notifier)))
        self.conn_count = count + 1

    def disconnect(self, notifier):
        remove_indices = []
        heap = self.heap

        wr_notifier = ref(notifier)

        for i, item in enumerate(heap):
            if item[2] is wr_notifier:
                remove_indices.append(i)
        
        for i in reversed(remove_indices):
            heap.pop(i)

    def emit(self, message):
        heap = self.heap

        notifiers = nsmallest(len(heap), heap)

        message.initialize()

        for item in notifiers:
            notifier = item[2]()
            if notifier is None:
                heap.remove(item)
            else:
                try:
                    notifier(message)
                except KillSignalException:
                    break
                finally:
                    message.update()

        message.finalize()

