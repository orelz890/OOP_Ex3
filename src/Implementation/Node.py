import random


class Node:
    def __init__(self, key: int, pos: tuple = None):
        if pos is None:
            pos = (random.uniform(35.19, 35.22), random.uniform(32.05, 32.22), 0.0)
        self.key = key
        self.location = pos
        self.weight = 0
        self.tag = 0
        self.w = 0
        self.info = "White"

    def __str__(self):
        return f"({self.key}, {self.location})"

    def __repr__(self):
        return f"({self.key}, {self.location})"

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __ne__(self, other):
        return self.weight != other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight <= other.weight

    def pos_to_string(self):
        string = "{},{},{}".format(self.location[0], self.location[1], self.location[2])
        return string
