from graph import Graph

EPSILON = 10 ** -8

class BellmanFord(Graph):
    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)

    def get_dists(self, start: str) -> dict:
        """
        Compute the shortest distance from the starting vertex to every other vertex.
        Stops early if no updates are made in an iteration, indicating all shortest paths are found.
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        for i in range(len(self.graph) - 1):
            updated = False

            for u in self.graph:
                for v, weight in self.graph[u].items():
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        updated = True

            if not updated:
                break

        for u in self.graph:
            for v, weight in self.graph[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    print("Graph contains a negative weight cycle.")
                    return None

        return distances

    def get_shortest_path(self, start: str, goal: str):
        """
        Given a starting vertex and end goal vertex, shortest path between the two vertices.
        """
        distances = self.get_dists(start)
        if distances is None:
            return None

        path = [goal]
        cur = goal

        while cur != start:
            found = False
            for neighbor, weight in self.graph[cur].items():
                if abs((distances[cur] - weight) - distances[neighbor]) < EPSILON:
                    cur = neighbor
                    path.append(cur)
                    found = True
                    break
            if not found:
                return None

        return path[::-1]


if __name__ == "__main__":
    test_graph = {
        "A": {"B": 3, "C": 3},
        "B": {"A": 3, "D": 3.5, "E": 2.8},
        "C": {"A": 3, "E": 2.8, "F": 3.5},
        "D": {"B": 3.5, "E": 3.1, "G": 10},
        "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
        "F": {"G": 2.5, "C": 3.5},
        "G": {"F": 2.5, "E": 7, "D": 10},
    }

    bf = BellmanFord(test_graph)
    distances = bf.get_dists("A")
    print("Shortest distances from A:", distances)

    path = bf.get_shortest_path("A", "C")
    print("Shortest path from A to C:", path)
