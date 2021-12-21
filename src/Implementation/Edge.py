class Edge:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __str__(self):
        return f"({self.src}, {self.dest}, {self.weight})"

    def __repr__(self):
        return f"({self.src}, {self.dest}, {self.weight})"

