import json
import random
import queue
from typing import List

from Implementation.Edge import Edge
from Implementation.Node import Node
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

    def is_connected(self) -> bool:
        if len(self.graph.nodes_dict) == 0 or len(self.graph.nodes_dict) == 1:
            return True
        # some_node = random.choice(list(self.graph.nodes_dict.keys()))
        some_node = 1
        if not self.is_node_connected(self.graph, some_node):
            return False
        reversed_graph = DiGraph()
        reversed_graph.nodes_dict = self.graph.nodes_dict
        for node_key in self.graph.nodes_dict.keys():
            for edge in self.graph.out_edges.get(str(node_key)).values():
                reversed_graph.add_edge(edge.dest, edge.src, edge.weight)
        return self.is_node_connected(reversed_graph, some_node)

    def is_node_connected(self, DWG: DiGraph, key: int) -> bool:
        flag = DWG.dijkstra(key)
        # If one of the nodes tag still holds -1 as his father it means there is no path to it from the src node.
        for node in DWG.nodes_dict.values():
            if node.tag == no_path:
                return False
        return True

    def shortest_path_dist(self, src: int, dst: int) -> float:
        flag = self.graph.dijkstra(src)
        src_node = self.graph.nodes_dict.get(str(src))
        dst_node = self.graph.nodes_dict.get(str(dst))
        if src_node is None or dst_node is None or flag == no_path or dst_node.tag == -1:
            return float('inf')
        if src == dst:
            return 0
        return dst_node.w

    """
        The Idea for this function is also based on the Dijkstra's algorithm.
        Mission -> Return the list of nodes which represent the shortest path from a given src node to the given dest
                    And the path cost(weight).
        Implementation:
        Step 1: Do dijkstra on the src node.
        Step 2: Check if the returned value shows a valid path(using flag).
        Step 3: Go to the dest node tag and start gathering fathers(tag value stores this node father id) to a list.
        Step 4: The list we made is reversed. therefore, reverse it.
        Last, return the list and the dest node w (after the dijkstra its stores the shortest dist from src to it)
        
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        flag = self.graph.dijkstra(id1)
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

    """
        https://www.sanfoundry.com/java-program-implement-traveling-salesman-problem-using-nearest-neighbour-algorithm/
        The Idea for this function is a Greedy algorithm.
        Mission ->  Given a city nodes the function Returns a list of nodes represents the shortest path throw all.
        Implementation -> Same idea as before:
        Step 1: Chose the first node. Add is to the ans array.
        Step 2: Find the closest node in the given city to this node(lets call it CN).
        Step 3: Get the path between them, and add it to the ans array.
        Step 4: Remove the current node from cities and add CN
        Step 5: Loop till there are no more nodes in cities.
        Last, return the ans list.
    """

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if len(node_lst) == 0:
            return [], 0
        if len(node_lst) == 1:
            return [self.graph.nodes_dict.get(str(node_lst[0]))], 0
        current_node = self.graph.nodes_dict.get(str(node_lst[0]))
        node_lst.remove(node_lst[0])
        ans = [current_node]
        total_dist = 0
        while node_lst:
            src = float('-inf')
            dst = float('-inf')
            shortest_dist = float('inf')
            i = 0
            for node_key in node_lst:
                dist = self.shortest_path_dist(current_node.key, node_key)
                if dist < shortest_dist:
                    src = i
                    dst = node_key
                    shortest_dist = dist
                i += 1
            # Now we know who are the current src and dst that has the shortest path between them
            shortest_path = self.shortest_path(current_node.key, dst)[1]
            shortest_path.remove(shortest_path[0])
            # Filling the ans with the list of nodes we got from the shortestPath function.
            ans.extend(shortest_path)
            current_node = self.graph.nodes_dict.get(str(node_lst[src]))
            node_lst.remove(node_lst[src])
            total_dist += shortest_dist
        return ans, total_dist

    """
        Mission -> Find the NodeData which minimizes the max distance to all the other nodes.
        Implementation:
        Step 1: Check if the graph is connected. If not return null.
        Step 2: ForEach node in the graph call dijkstra, And find the max weight value.
        Step 3: If this value is lower than the last canter update, update the center to this value.
        Last, return the center.
    """

    def centerPoint(self) -> (int, float):
        if not self.is_connected():
            return None , float('inf')
        center = None
        best_dist = float('inf')
        for node in self.graph.nodes_dict.values():
            self.graph.dijkstra(node.key)
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
    # g.load_from_json("../../data/NotConnectedG.json")
    g.load_from_json("../../data/G3.json")
    # print(g.shortest_path(0, 6))
    # print(g.centerPoint())
    # print(g.TSP([0, 20, 5, 28, 4]))
    # print(g.is_connected())
    print(g.centerPoint())