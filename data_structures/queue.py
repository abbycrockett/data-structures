class Queue:
    def __init__(self, values=None):
        self.items = []
        if values:
            for value in values:
                self.enqueue(value)

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if self.items:
            return self.items.pop(0)
        return None

    def to_list(self):
        return self.items.copy()
