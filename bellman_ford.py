import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from scraper import get_links_weight_1

EPSILON = 10**-8


class BellmanFord(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)
        self.path = None

    def get_dists(self, start: str) -> dict:
        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0

        for _ in range(len(self.graph) - 1):
            updated = False
            for u in self.graph:
                for v, weight in self.graph[u].items():
                    if (
                        distances[u] != float("inf")
                        and distances[u] + weight < distances[v]
                    ):
                        distances[v] = distances[u] + weight
                        updated = True
            if not updated:
                break

        for u in self.graph:
            for v, weight in self.graph[u].items():
                if (
                    distances[u] != float("inf")
                    and distances[u] + weight < distances[v]
                ):
                    print("Graph contains a negative weight cycle.")
                    return None

        return distances

    def get_shortest_path(self, start: str, goal: str):
        distances = self.get_dists(start)
        if distances is None:
            return None

        if distances[goal] == float("inf"):
            print(f"No path from {start} to {goal}.")
            return None

        path = []
        current = goal
        while current is not None:
            path.append(current)

            found = False
            for neighbor, weight in self.graph[current].items():
                if abs(distances[current] - weight - distances[neighbor]) < EPSILON:
                    current = neighbor
                    found = True
                    break
            if not found:
                break

        path.reverse()
        return path if path[0] == start else None

    def visualize(self):
        if self.path:
            G = nx.Graph()

            for vertex, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    G.add_edge(vertex, neighbor, weight=weight)

            pos = nx.spring_layout(G)
            node_colors = ['lightblue' if node not in self.path else 'lightgreen' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size = 10, font_weight = 'bold')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.show()
        else:
            raise TypeError("No path has been found")

if __name__ == "__main__":
    # testing 
    test_graph = Graph({})
    get_links_weight_1(test_graph, "Alnico")
    bellman_ford = BellmanFord(test_graph.graph)

    print("Demo Graph:", bellman_ford.graph)

    result = bellman_ford.get_shortest_path(start="Alnico", goal="Magnetic field")
    if result is not None:
        print("Shortest Path:", (result))
    else:
        print("No path.")
