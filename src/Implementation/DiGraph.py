from Implementation.Node import Node
from Implementation.Edge import Edge
from api.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    nodes_dict = {}
    into_edges = {}
    out_edges = {}
    node_size = 0
    edge_size = 0
    MC = 0

    def __init__(self):
        self.nodes_dict = {}
        self.into_edges = {}
        self.out_edges = {}
        self.node_size = 0
        self.edge_size = 0
        self.MC = 0

    def v_size(self) -> int:
        return self.node_size

    def e_size(self) -> int:
        return self.edge_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.nodes_dict

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        ans = {}
        node = self.nodes_dict.get(str(id1))
        if node is not None:
            for key in self.into_edges.get(str(id1)):
                node_edges = self.into_edges.get(str(key))
                if ans.get(str(key)) is None:
                    ans[str(key)] = {}
                for key2 in node_edges:
                    edge = self.into_edges.get(str(key)).get(str(key2))
                    ans[str(key)] = (edge.src, edge.weight)
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        ans = {}
        node = self.nodes_dict.get(str(id1))
        if node is not None:
            for key in self.out_edges.get(str(id1)):
                node_edges = self.out_edges.get(str(key))
                if ans.get(str(key)) is None:
                    ans[str(key)] = {}
                for key2 in node_edges:
                    edge = self.out_edges.get(str(key)).get(str(key2))
                    ans[str(key)] = (edge.src, edge.weight)
        return ans

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        src = self.nodes_dict.get(str(id1))
        dest = self.nodes_dict.get(str(id2))
        if src is None or dest is None:
            return False
        new_edge = Edge(id1, id2, weight)
        edges_into = self.into_edges.get(str(id2))
        edges_out = self.out_edges.get(str(id1))
        if edges_out is not None and edges_into is not None:
            if edges_out.get(str(id2)) is not None:
                return False
        else:
            if edges_into is None:
                self.into_edges[str(id2)] = {}
            if edges_out is None:
                self.out_edges[str(id1)] = {}
        self.into_edges[str(id2)][str(id1)] = new_edge
        self.out_edges[str(id1)][str(id2)] = new_edge
        self.nodes_dict.get(str(id1)).weight += 1
        self.edge_size += 1
        src.weight += 1
        self.MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node = self.nodes_dict.get(str(node_id))
        if node is not None:
            return False
        self.nodes_dict[str(node_id)] = Node(node_id, pos)
        self.node_size += 1
        self.MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        node = self.nodes_dict.get(str(node_id))
        if node is None:
            return False
        s = str(node_id)
        self.nodes_dict.pop(s)
        self.node_size -= 1

        edge1 = self.out_edges.get(s)
        if edge1 is not None:
            e = self.out_edges.pop(s)
            self.edge_size -= len(e)
        edge2 = self.into_edges.get(s)
        if edge2 is not None:
            e = self.into_edges.pop(s)
            self.edge_size -= len(e)
        for key in self.out_edges:
            self.remove_edge(key, node_id)

        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        s1 = str(node_id1)
        s2 = str(node_id2)
        node1 = self.nodes_dict.get(s1)
        node2 = self.nodes_dict.get(s2)
        edge = self.out_edges.get(s1).get(s2)
        if node1 is None or node2 is None or edge is None:
            return False
        self.out_edges[s1].pop(s2)
        self.into_edges[s2].pop(s1)
        self.edge_size -= 1
        node1.weight -= 1
        self.MC += 1
        return True


if __name__ == '__main__':
    g = DiGraph()
    n1 = Node(0, (0, 0, 0))
    n2 = Node(1, (1, 1, 1))
    n3 = Node(2, (2, 2, 2))
    e1 = Edge(0, 1, 1.5)
    e2 = Edge(0, 2, 2.0)
    e3 = Edge(1, 0, 3.5)
    g.add_node(n1.key, n1.location)
    g.add_node(n2.key, n2.location)
    g.add_node(n3.key, n3.location)
    print(3, g.node_size)
    g.add_edge(n1.key, n2.key, 21.3)
    g.add_edge(n2.key, n1.key, 14.7)
    g.add_edge(n2.key, n3.key, 12.5)
    g.add_edge(n3.key, n1.key, 12.5)
    print(4, g.edge_size)
    g.remove_node(n1.key)
    print(2, g.node_size)
    print(1, g.edge_size)
    edge_left = g.out_edges.get(str(n2.key)).get(str(n3.key))
    print(n2.key, edge_left.src)
    print(n3.key, edge_left.dest)
    print(edge_left.weight)
