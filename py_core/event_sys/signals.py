from weakref import ref
from heapq import heappush, nsmallest


class KillSignalException(Exception):
    pass


class Signal(object):

    def __init__(self):
        self._heap = []
        self._conn_count = 0
        self._notifiers = []

    def _heap_changed(self):
        heap = self._heap
        self._notifiers = nsmallest(len(heap), heap)

    def connect(self, notifier, priority=16):
        count = self._conn_count
        heappush(self._heap, (priority, count, ref(notifier)))
        self._conn_count = count + 1
        
        self._heap_changed()

    def disconnect(self, notifier):
        remove_indices = []
        heap = self._heap

        wr_notifier = ref(notifier)

        for i, item in enumerate(heap):
            if item[2] is wr_notifier:
                remove_indices.append(i)
        
        for i in reversed(remove_indices):
            heap.pop(i)

        self._heap_changed()

    def emit(self, message):
        heap = self._heap
        heap_changed = False

        message.initialize()

        for item in self._notifiers:
            notifier = item[2]()
            if notifier is None:
                heap.remove(item)
                heap_changed = True
            else:
                try:
                    notifier(message)
                except KillSignalException:
                    break
                finally:
                    message.update()

        message.finalize()

        if heap_changed:
            self._heap_changed()

