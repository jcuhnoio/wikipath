"""
Declaration of the Graph Class
"""

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np


class Graph:
    def __init__(self, graph_dict: dict) -> None:
        """
        Initialize the Graph object

        Args:
            graph_dict: dictionary containing graph structure information; Example: {v1: {v2: 1, v3: 2}} would represent a graph where v1 has 2 connected vertices v2 & v3
                        with weight 1 & 2.

        """
        self.graph = graph_dict

    def add_edge(self, v1: str, v2: str, w: float) -> None:
        """
        Add an edge from v1 to v2 with weight w

        Args:
            v1: name of vertex 1
            v2: name of vertex 2
            w: weight of the edge
        """

        if v1 not in self.graph:
            self.graph[v1] = {}
        if v2 not in self.graph:
            self.graph[v2] = {}

        # Update or add the edges between v1 and v2
        self.graph[v1][v2] = w


    def visualize(self):
        G = nx.Graph()
        for vertex, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(vertex, neighbor, weight=weight)
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=10,
            font_weight="bold",
        )
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()

    def __iter__(self):
        """
        When called in for loop
        """
        return iter(self.graph.items())

    def __str__(self):
        """
        When called in print()
        """
        return str(self.graph)

    def __len__(self):
        """
        When called in len()
        """
        return len(self.graph)

TEST_GRAPH = {
                "Node0": {"Node9": 7.7, "Node47": 7.7, "Node4": 7.1, "Node19": 6.0, "Node35": 1.8},
                "Node1": {"Node17": 9.2, "Node9": 7.9, "Node32": 6.9},
                "Node2": {"Node33": 1.6, "Node14": 9.7, "Node41": 8.4, "Node46": 6.0, "Node24": 3.6, "Node26": 6.4, "Node48": 5.2},
                "Node3": {"Node25": 2.2, "Node18": 6.7, "Node49": 9.9, "Node13": 4.2, "Node20": 8.2, "Node36": 3.4, "Node39": 2.1, "Node43": 3.9},
                "Node4": {"Node41": 1.2, "Node22": 1.2, "Node0": 7.1, "Node44": 2.3},
                "Node5": {"Node27": 7.2, "Node8": 1.7, "Node32": 2.1, "Node9": 8.6, "Node10": 6.5, "Node29": 7.2, "Node33": 10.0},
                "Node6": {"Node46": 7.9, "Node8": 3.5, "Node24": 2.6, "Node27": 7.4, "Node31": 7.9, "Node48": 5.9},
                "Node7": {"Node38": 8.6, "Node21": 6.2, "Node28": 3.9, "Node34": 4.5, "Node41": 9.1, "Node45": 5.3, "Node49": 7.2},
                "Node8": {"Node5": 1.7, "Node6": 3.5, "Node23": 6.4, "Node43": 10.0, "Node21": 6.0, "Node14": 6.3, "Node18": 6.0, "Node31": 5.4, "Node32": 5.4, "Node40": 6.7, "Node45": 6.5},
                "Node9": {"Node0": 7.7, "Node5": 8.6, "Node1": 7.9, "Node35": 6.4, "Node12": 8.1, "Node13": 6.3, "Node16": 5.2, "Node41": 5.1},
                "Node10": {"Node12": 7.9, "Node47": 6.6, "Node5": 6.5, "Node21": 6.4, "Node48": 5.0},
                "Node11": {"Node39": 2.3, "Node40": 9.4, "Node17": 7.7, "Node20": 8.1, "Node24": 9.5, "Node25": 4.2, "Node33": 4.7},
                "Node12": {"Node10": 7.9, "Node24": 9.5, "Node9": 8.1, "Node30": 1.4, "Node28": 9.7, "Node40": 7.2},
                "Node13": {"Node27": 8.7, "Node3": 4.2, "Node9": 6.3, "Node15": 5.0, "Node39": 3.1},
                "Node14": {"Node2": 9.7, "Node41": 4.6, "Node39": 6.6, "Node23": 5.1, "Node8": 6.3},
                "Node15": {"Node46": 3.8, "Node13": 5.0, "Node44": 1.4, "Node42": 9.5, "Node26": 7.7},
                "Node16": {"Node9": 5.2, "Node23": 4.4, "Node29": 9.1, "Node39": 3.2},
                "Node17": {"Node1": 9.2, "Node35": 2.5, "Node11": 7.7, "Node34": 6.2},
                "Node18": {"Node3": 6.7, "Node8": 6.0, "Node23": 3.0, "Node35": 1.1, "Node28": 7.6, "Node38": 9.1, "Node44": 8.6},
                "Node19": {"Node37": 5.0, "Node0": 6.0, "Node27": 7.7, "Node28": 3.5, "Node29": 7.3, "Node42": 6.4},
                "Node20": {"Node11": 8.1, "Node34": 6.7, "Node3": 8.2, "Node35": 3.0},
                "Node21": {"Node7": 6.2, "Node10": 6.4, "Node8": 6.0, "Node46": 7.9},
                "Node22": {"Node4": 1.2},
                "Node23": {"Node8": 6.4, "Node14": 5.1, "Node16": 4.4, "Node18": 3.0},
                "Node24": {"Node2": 3.6, "Node11": 9.5, "Node12": 9.5, "Node6": 2.6},
                "Node25": {"Node3": 2.2, "Node11": 4.2, "Node47": 5.9},
                "Node26": {"Node46": 9.5, "Node15": 7.7},
                "Node27": {"Node5": 7.2, "Node6": 7.4, "Node19": 7.7, "Node47": 1.2},
                "Node28": {"Node7": 3.9, "Node18": 7.6, "Node12": 9.7},
                "Node29": {"Node5": 7.2, "Node19": 7.3, "Node16": 9.1},
                "Node30": {"Node12": 1.4, "Node48": 8.9, "Node44": 7.4},
                "Node31": {"Node6": 7.9, "Node8": 5.4},
                "Node32": {"Node1": 6.9, "Node5": 2.1, "Node8": 5.4, "Node45": 3.6},
                "Node33": {"Node2": 1.6, "Node5": 10.0, "Node11": 4.7},
                "Node34": {"Node7": 4.5, "Node20": 6.7, "Node17": 6.2},
                "Node35": {"Node1": 2.5, "Node3": 1.8, "Node20": 3.0, "Node18": 1.1, "Node9": 6.4},
                "Node36": {"Node3": 3.4, "Node49": 3.1},
                "Node37": {"Node19": 5.0, "Node44": 2.7, "Node48": 3.1, "Node46": 5.9},
                "Node38": {"Node7": 8.6, "Node18": 9.1, "Node47": 3.8},
                "Node39": {"Node3": 2.1, "Node18": 6.6, "Node13": 3.1, "Node14": 6.6, "Node16": 3.2},
                "Node40": {"Node11": 9.4, "Node10": 7.2, "Node8": 6.7, "Node45": 6.1},
                "Node41": {"Node2": 8.4, "Node4": 1.2, "Node7": 9.1, "Node14": 4.6, "Node9": 5.1},
                "Node42": {"Node15": 9.5, "Node19": 6.4},
                "Node43": {"Node3": 3.9, "Node8": 10.0},
                "Node44": {"Node4": 2.3, "Node15": 1.4, "Node18": 8.6, "Node30": 7.4},
                "Node45": {"Node7": 5.3, "Node8": 6.5, "Node32": 3.6, "Node40": 6.1},
                "Node46": {"Node2": 6.0, "Node6": 7.9, "Node15": 9.5, "Node10": 5.0, "Node37": 5.9, "Node21": 7.9},
                "Node47": {"Node0": 7.7, "Node10": 6.6, "Node38": 3.8, "Node25": 5.9, "Node27": 1.2},
                "Node48": {"Node2": 5.2, "Node6": 5.9, "Node30": 8.9, "Node10": 5.0},
                "Node49": {"Node3": 9.9, "Node7": 7.2, "Node36": 3.1}
            }


if __name__ == "__main__":
    # For testing
    graph_dict = {"Node1": {}}
    my_graph = Graph(graph_dict=graph_dict)
    my_graph.add_edge("Node2", "Node1", 10)
    my_graph.visualize()
