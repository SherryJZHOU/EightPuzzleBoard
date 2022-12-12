import heapq
import itertools

class PriorityQueue:
    """Basic priority queue class. 
    """

    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        if task in self.entry_finder:
            self.remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, task):
        """Mark an existing task as REMOVED.  Raise KeyError if not found."""
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def get(self, task):
        return self.entry_finder[task][0]

    def pop(self):
        """Remove and return the lowest priority task. Raise KeyError if empty."""
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def empty(self):
        return len(self.entry_finder) == 0

    def __contains__(self, key):
        return key in self.entry_finder

    def __len__(self):
        return len(self.entry_finder)
