class Stack:
    def __init__(self, values=None):
        self.items = []
        if values:
            for value in values:
                self.push(value)

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def to_list(self):
        return self.items.copy()
