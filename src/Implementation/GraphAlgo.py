import json
import math
import random
import queue
from typing import List
from api.GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from api.GraphInterface import GraphInterface


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

    # def dijkstra(self, src: int):
    #     node_q = queue.PriorityQueue()
    #     for node in self.graph.nodes_dict.values():
    #         if node.key == src:
    #             node.w = 0.0
    #         else:
    #             node.w = float("inf")
    #         node_q.put(node)
    #     while node_q.not_empty:
    #         node = node_q.get()
    #


    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """

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
    g.load_from_json("../../data/A0.json")
    g.save_to_json("firstTryToSave.json")