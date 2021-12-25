import unittest

from Implementation.DiGraph import DiGraph
from src.Implementation.GraphAlgo import GraphAlgo


class test_GraphAlgo(unittest.TestCase):
    g: GraphAlgo = GraphAlgo()

    def setUp(self) -> None:
        self.g = GraphAlgo()
        self.g.load_from_json("../data/A0.json")

    def test_get_graph(self):
        graph = self.g.get_graph()
        for node in graph.nodes_dict.values():
            self.assertEqual(self.g.graph.nodes_dict.get(str(node.key)).location, node.location)
            for edge in graph.out_edges.get(str(node.key)).values():
                self.assertEqual(self.g.graph.out_edges.get(str(node.key)).get(str(edge.dest)).weight, edge.weight)

    def test_load_from_json(self):
        self.assertTrue(self.g.load_from_json("../data/A0.json"))
        self.assertEqual(11, self.g.graph.node_size)
        self.assertEqual(22, self.g.graph.edge_size)
        self.assertEqual(1.4622464066335845, self.g.graph.out_edges.get(str(5)).get(str(4)).weight)
        self.assertEqual(1.6449953452844968, self.g.graph.out_edges.get(str(8)).get(str(7)).weight)
        self.assertEqual(1.1761238717867548, self.g.graph.out_edges.get(str(10)).get(str(0)).weight)
        self.assertEqual('35.197528356739305,32.1053088,0.0', self.g.graph.nodes_dict.get(str(3)).location)
        self.assertEqual('35.20746249717514,32.10254648739496,0.0', self.g.graph.nodes_dict.get(str(7)).location)
        self.assertEqual('35.19597880064568,32.10154696638656,0.0', self.g.graph.nodes_dict.get(str(9)).location)

    def test_save_to_json(self):
        try:
            self.assertTrue(self.g.save_to_json("my_save_test"))
        except Exception as exp:
            print(Exception, exp)

    def test_dijkstra(self):
        pass

    def test_set_all_w(self):
        self.g.set_all_tags(1.2, 890)
        for node in self.g.graph.nodes_dict.values():
            self.assertEqual(1.2, node.w)
            self.assertEqual(890, node.tag)

    def test_shortest_path(self):
        self.g.load_from_json("../data/A0.json")
        self.assertEqual((1.4004465106761335,
                          [self.g.graph.nodes_dict.get(str(0)),
                           self.g.graph.nodes_dict.get(str(1))]), self.g.shortest_path(0, 1))
        self.assertEqual((6.670946327534079,
                          [self.g.graph.nodes_dict.get(str(0)),
                           self.g.graph.nodes_dict.get(str(10)),
                           self.g.graph.nodes_dict.get(str(9)),
                           self.g.graph.nodes_dict.get(str(8)),
                           self.g.graph.nodes_dict.get(str(7)),
                           self.g.graph.nodes_dict.get(str(6))]), self.g.shortest_path(0, 6))
        self.g.load_from_json("../data/A2.json")
        self.assertEqual((4.959012170482032,
                          [self.g.graph.nodes_dict.get(str(0)),
                           self.g.graph.nodes_dict.get(str(1)),
                           self.g.graph.nodes_dict.get(str(2)),
                           self.g.graph.nodes_dict.get(str(6))]), self.g.shortest_path(0, 6))

    def test_tsp(self):
        pass

    def test_center_point(self):
        pass

    def test_plot_graph(self):
        pass
