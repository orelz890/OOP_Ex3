import json
import random
import queue
from typing import List
from api.GraphAlgoInterface import GraphAlgoInterface
from src.Implementation.DiGraph import DiGraph
from api.GraphInterface import GraphInterface

valid_path = 1
zero_dist = 0
no_path = -1


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            data = open(file_name, 'r')
            with data as f:
                file = json.load(f)
                nodes = file['Nodes']
                edges = file['Edges']
            for node in nodes:
                id = node['id']
                pos = node['pos']
                if pos is None:
                    x = random.uniform(35.18763666989508, 35.212217299435025)
                    y = random.uniform(32.09925715462185, 32.109397749579834)
                    pos = (x, y, 0.0)
                self.graph.add_node(id, pos)
            for edge in edges:
                self.graph.add_edge(edge['src'], edge['dest'], edge['w'])
        except Exception:
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        data = {"Nodes": [], "Edges": []}
        for node in self.graph.nodes_dict.values():
            data["Nodes"].append({"id": node.key, "pos": node.location})
        for src in self.graph.out_edges.keys():
            for dst in self.graph.out_edges.get(str(src)).keys():
                weight = self.graph.out_edges.get(str(src)).get(str(dst)).weight
                data["Edges"].append({"src": src, "dest": dst, "w": weight})
        try:
            with open(file_name, 'w') as file:
                json.dump(data, indent=2, fp=file)
        except Exception:
            return False
        return True

    def dijkstra(self, src: int) -> int:
        if self.graph.nodes_dict.get(str(src)) is None:
            return no_path

        src_node = self.graph.nodes_dict.get(str(src))
        self.set_all_tags(float('inf'), -1)
        node_q = queue.PriorityQueue()
        node_q.put(src_node)
        src_node.w = 0

        while not node_q.empty():
            node = node_q.get()
            for neighbour_edge in self.graph.out_edges.get(str(node.key)).values():
                neighbour_node = self.graph.nodes_dict.get(str(neighbour_edge.dest))
                neighbours_new_weight = neighbour_edge.weight + node.w
                if neighbour_node.w > neighbours_new_weight:
                    neighbour_node.tag = node.key
                    neighbour_node.w = neighbours_new_weight
                    node_q.put(neighbour_node)
        return valid_path

    def set_all_tags(self, w_val: float, tag_val: int):
        for node in self.graph.nodes_dict.values():
            node.w = w_val
            node.tag = tag_val

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        flag = self.dijkstra(id1)
        src_node = self.graph.nodes_dict.get(str(id1))
        dst_node = self.graph.nodes_dict.get(str(id2))
        if src_node is None or dst_node is None or flag == no_path or dst_node.tag == -1:
            return float('inf'), []
        if id1 == id2:
            return 0, [src_node]
        # If we got to the next line it means we have a valid path between id1 to id2
        # The dijkstra works from src to dest and stores in each node in his way a reference to his father(flag val)
        # Therefore, lets gather the information to a valid answer:
        stack = [dst_node]
        current_tag = dst_node.tag
        while current_tag != id1:
            current_node = self.graph.nodes_dict.get(str(current_tag))
            current_tag = current_node.tag
            stack.append(current_node)
        stack.append(src_node)
        # Now, we have a reversed version of the answer. Because we gathered fathers from dest till we saw the src.
        ans_list = []
        while stack:
            ans_list.append(stack.pop())
        return dst_node.w, ans_list

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        #     isConnected?
        center = None
        best_dist = float('inf')
        for node in self.graph.nodes_dict.values():
            self.dijkstra(node.key)
            temp = float('-inf')
            for node2 in self.graph.nodes_dict.values():
                if node2.w > temp:
                    temp = node2.w
            if temp < best_dist:
                best_dist = temp
                center = node.key
        return center, best_dist

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json("../../data/G3.json")
    # print(g.shortest_path(0, 6))
    print(g.centerPoint())
