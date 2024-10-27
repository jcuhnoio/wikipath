from graph import Graph
from heapq import heapify, heappop, heappush
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

class AStar(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)

        self.graph = graph_dict
        self.vertex_heuristics = np.zeros((len(self.graph), 2))

    def find_path(self, start: str, end: str) -> list:
        """
        From a given start node and end node, finds the optimal path
        between the two nodes based on a heuristic function.

        Args:
            start (string): Name of start node
            end (string): Name of end node
        
        Returns:
            path (list): List of nodes to traverse to generate the path.
        """
        
        # Start with our initially discovered node
        open = [start]
        came_from = {key: [] for key in self.graph} 

        # Set the g score of the start node to 0, initialize rest of scores to infinity
        g_score = {key: float('inf') for key in self.graph} 
        g_score[start] = 0

        f_score = {key: float('inf') for key in self.graph} 
        f_score[start] = self.find_heuristic(start, end)


        pq = [(f_score[start], start)]
        heapify(pq)

        while pq:

            _, curr_node = heappop(pq)
            if curr_node == end:
                return self.generate_path(came_from, curr_node)

            for neighbor, weight in self.graph[curr_node].items():
                tentative_g_score = g_score[curr_node] + weight
                if tentative_g_score < g_score[neighbor]:
                    # the path to this neighbor is better than previous
                    came_from.update({neighbor : curr_node})
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.find_heuristic(curr_node, neighbor)
                    heappush(pq, (tentative_g_score, neighbor))
        
    
    def generate_path(self, came_from: dict, curr_node: str) -> list:

        path = [curr_node]

        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()

        return path
        
    def find_heuristic(self, start, end):

        start_deg = len(self.graph[start])
        end_deg = len(self.graph[end])
        h = ((1/start_deg) + (1/end_deg))

        return h
    
    def visualize(self, path=None):
        G = nx.Graph()

        for vertex, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(vertex, neighbor, weight=weight)

        pos = nx.spring_layout(G)
        node_colors = ['lightblue' if node not in path else 'lightgreen' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size = 10, font_weight = 'bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.show()



if __name__ == "__main__":
    test_graph = {
    "A": {"B": 3, "C": 3},
    "B": {"A": 3, "D": 3.5, "E": 2.8, "H": 4},
    "C": {"A": 3, "E": 2.8, "F": 3.5, "I": 5},
    "D": {"B": 3.5, "E": 3.1, "G": 10, "J": 6},
    "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7, "H": 2.5, "I": 4.2},
    "F": {"G": 2.5, "C": 3.5, "K": 4.3},
    "G": {"F": 2.5, "E": 7, "D": 10, "L": 6},
    "H": {"B": 4, "E": 2.5, "I": 3.3, "M": 5.2},
    "I": {"C": 5, "E": 4.2, "H": 3.3, "N": 4.6},
    "J": {"D": 6, "K": 2.7, "L": 3.9},
    "K": {"F": 4.3, "J": 2.7, "L": 2.1},
    "L": {"G": 6, "J": 3.9, "K": 2.1, "N": 5.7},
    "M": {"H": 5.2, "N": 3.8},
    "N": {"I": 4.6, "L": 5.7, "M": 3.8}
}

    test = AStar(test_graph)
    path = test.find_path("A", "J")
    print(path)
    test.visualize(path)