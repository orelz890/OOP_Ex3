class Node:
    def __init__(self, key: int, pos: tuple = None):
        self.key = key
        self.location = pos
        self.weight = 0
        self.tag = 0
        self.w = 0

    def __str__(self):
        return f"({self.key}, {self.location})"

    def __repr__(self):
        return f"({self.key}, {self.location})"
