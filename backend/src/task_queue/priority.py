
class PriorityQueue:
    def __init__(self):
        self.items = []
    def push(self, item, priority):
        self.items.append((priority, item))
