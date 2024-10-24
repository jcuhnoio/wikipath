"""
Implementation of Dijkstra's Algorithm

1. Initialize the graph with the source node to take the value of 0 and all other nodes infinity. Start with the source as the “current node”.

2. Visit all neighboring nodes of the current node and update their values to the cumulative sum of weights (distances) from the source.
   If a neighbor’s current value is smaller than the cumulative sum, it stays the same. Mark the “current node” as finished.

3. Mark the unfinished minimum-value node as the “current node”.

4. Repeat steps 2 and 3 until all nodes are finished.
"""

from graph import Graph
from heapq import heapify, heappop, heappush

EPSILON = 10 ** -8

class Dijkstra(Graph):

    def __init__(self, graph_dict: dict) -> None:
        super().__init__(graph_dict)

    def get_dists(self, start: str) -> dict:
        """
        Given a starting vertex, compute the shortest distance from starting vertex to every other vertex

        Args:
            start: vertex to start from; this is a key for the graph dictionary

        Returns:
            distances: dictionary containing shortest distance form starting vertex for every other vertex
        """
        if start not in self.graph:
            raise KeyError(f"vertex {start} not found.")

        else:
            # Store vertices we already visited
            visited = set()

            # Initialize all distances between `start` to other nodes to infinity, start node will get 0
            distances = {key: float('inf') for key in self.graph} 
            distances[start] = 0

            # Priotiry queue of vertices we need to visit, elements are in (distance, vertex) form
            pq = [(0, start)]
            heapify(pq)


            # When pq is empty, that means we visited every vertex 
            while pq:
                cur_dist, cur_node = heappop(pq)

                if cur_node in visited:
                    continue
                    
                else:
                    visited.add(cur_node)

                    # Iterate through current vertex neighbots
                    for neighbor, weight in self.graph[cur_node].items():
                        if neighbor not in visited:
                            # If current distance value is larger than the cumulative sum, it updates
                            tent_dist = cur_dist + weight
                            if tent_dist < distances[neighbor]: 
                                distances[neighbor] = tent_dist
                                heappush(pq, (tent_dist, neighbor))

            return distances
    
    def get_shortest_path(self, start: str, goal: str):
        """
        Given a starting vertex and a goal vertex, compute the shortest distance between the two vertices

        Args:
            start: vertex to start from; this is a key for the graph dictionary
            goal: vertex to end at; this is a key for this graph dictionary

        Returns:
            path: list of vertices that make up the shortest path
        """

        if goal not in self.graph:
            raise Exception(f"vertex {goal} not found.")

        else:
            distances = self.get_dists(start = start)
            path = [goal]
            cur = goal

            while cur != start:
                for neighbor, weight in self.graph[cur].items():
                    diff = (distances[cur] - weight) - distances[neighbor]
                    if abs(diff) < EPSILON: # Using epsilon comparison to prevent floating point error
                        cur = neighbor
                        path.append(cur)

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

    dijk = Dijkstra(test_graph)
    result = dijk.get_shortest_path(start="B", goal="A")
    print(result)
