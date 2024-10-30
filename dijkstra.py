import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from scraper import get_links_and_weights
from heapq import heapify, heappop, heappush
from collections import defaultdict


class Dijkstra(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.path = None

    def find_shortest_path(self, start: str, goal: str) -> list:
        """
        Compute the shortest path from the start node to the goal node using Dijkstra's algorithm.
        
        Args:
            start: The starting vertex (source)
            goal: The target vertex (goal)

        Returns:
            path: List of vertices that make up the shortest path, or a dictionary with distances if no path is found.
        """

        visited = set()  # Keep track of visited nodes
        distances = defaultdict(lambda: float("inf"), {key: float("inf") for key in self.graph})
        distances[start] = 0  # Start node has distance 0

        # Priority queue to store (distance, vertex), initially with just the start vertex
        pq = [(0, start)]
        heapify(pq)

        # Track the path: which node we came from to get to each node
        came_from = {start: None}

        while pq:
            cur_dist, cur_node = heappop(pq)
            print(cur_node)

            # If the goal is reached, generate and return the path
            if cur_node.lower() == goal.lower():
                return self.generate_path(came_from, cur_node)

            if cur_node in visited:
                continue

            visited.add(cur_node)
            get_links_and_weights(self, cur_node)

            # Process all neighbors of the current node
            for neighbor, weight in self.graph[cur_node].items():
                if neighbor not in visited:
                    # Calculate the tentative distance to this neighbor
                    tent_dist = cur_dist + weight

                    # If the calculated distance is less than the known distance, update it
                    if tent_dist < distances[neighbor]:
                        came_from[neighbor] = cur_node # type: ignore
                        distances[neighbor] = tent_dist
                        heappush(pq, (tent_dist, neighbor))
        return []

    def generate_path(self, came_from: dict, curr_node: str):
        """
        Generate the path from start to goal after running Dijkstra's algorithm.

        Args:
            came_from: A dictionary mapping each node to the node it was reached from.
            curr_node: The current node (goal) to backtrack from.

        Returns:
            A list of nodes representing the shortest path from start to goal.
        """
        path = [curr_node]
        while came_from[curr_node]:
            curr_node = came_from[curr_node]
            path.append(curr_node)

        path.reverse()  # Reverse the path to get it from start to goal
        self.path = path
        return path

    def visualize(self, start=None, goal=None):
        """
        Visualize the graph and the shortest path using NetworkX and Matplotlib.
        
        Args:
            start: The start node to highlight.
            goal: The goal node to highlight.
        """
        if self.path:
            G = nx.Graph()
            for vertex, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    G.add_edge(vertex, neighbor, weight=weight)

            pos = nx.spring_layout(G)
            node_colors = [
                "lightblue" if node not in self.path else "lightgreen"
                for node in G.nodes()
            ]

            # Highlight the start and goal nodes if they are provided
            if start and goal:
                node_colors = [
                    "yellow" if node == start else ("red" if node == goal else color)
                    for node, color in zip(G.nodes(), node_colors)
                ]

            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color=node_colors,
                node_size=500,
                font_size=10,
                font_weight="bold",
            )
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.show()
        else:
            raise TypeError("No path has been calculated")


if __name__ == "__main__":
    # Test the Dijkstra class on a Wikipedia game example
    dijk = Dijkstra({})
    result = dijk.find_shortest_path(start="Alnico", goal="magnetic field")
    print(result)
