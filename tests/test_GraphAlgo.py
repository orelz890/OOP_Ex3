import unittest

from src.Implementation.DiGraph import DiGraph
from src.Implementation.GraphAlgo import GraphAlgo


class test_GraphAlgo(unittest.TestCase):
    g: GraphAlgo = GraphAlgo()

    def setUp(self) -> None:
        self.g.load_from_json("../data/A0.json")
        pass

    def test_get_graph(self):
        pass

    def test_load_from_json(self):
        self.assertEqual(11, self.g.graph.node_size)
        self.assertEqual(22, self.g.graph.edge_size)

    def test_save_to_json(self):
        pass

    def test_shortest_path(self):
        pass

    def test_tsp(self):
        pass

    def test_center_point(self):
        pass

    def test_plot_graph(self):
        pass
