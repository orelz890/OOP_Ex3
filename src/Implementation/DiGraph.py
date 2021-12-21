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
        for edge in self.into_edges[str(id1)].values:
            ans[str(edge.dest)] = (edge.src, edge.weight)
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        ans = {}
        for edge in self.out_edges[str(id1)].values:
            ans[str(edge.src)] = (edge.dest, edge.weight)
        return ans

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        src = self.nodes_dict[str(id1)]
        dest = self.nodes_dict[str(id2)]
        if src is None or dest is None:
            return False
        new_edge = Edge(id1, id2, weight)
        if self.into_edges[str(id2)][str(id1)] is not None and self.out_edges[str(id1)][str(id2)] is not None:
            self.into_edges[str(id2)][str(id1)] = new_edge
            self.out_edges[str(id1)][str(id2)] = new_edge
            self.nodes_dict[str(src)].weight += 1
            self.edge_size += 1
            self.MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node = self.nodes_dict[str(node_id)]
        if node is not None:
            return False
        self.nodes_dict[str(node_id)] = Node(node_id, pos)
        self.node_size += 1
        self.MC += 1
        raise True

    def remove_node(self, node_id: int) -> bool:
        node = self.nodes_dict[str(node_id)]
        if node is None:
            return False
        s = str(node_id)
        self.into_edges.pop(s)
        self.out_edges.pop(s)
        self.nodes_dict.pop(s)
        self.node_size -= 1
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        s1 = str(node_id1)
        s2 = str(node_id2)
        node1 = self.nodes_dict[s1]
        node2 = self.nodes_dict[s2]
        edge = self.out_edges[s1][s2]
        if node1 is None or node2 is None or edge is None:
            return False
        self.out_edges[s1].pop(s2)
        self.into_edges[s2].pop(s1)
        self.edge_size -= 1
        self.MC += 1
        return True
