"""
Declaration of the Graph Class
"""

class Graph():
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
        Add an edge between v1 and v2 with weight w

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
        self.graph[v2][v1] = w


    def edge_weight(self, v1, v2):
        """
        Given two vertices, return the edge weight

        Args:
            v1: name of vertex 1
            v2: name of vertex 2
        
        Returns: 
            weight of the edge v1 <-> v2
        """
        try:
            edges = self.graph[v1]
            try:
                return edges[v2]
            except:
                raise KeyError(f"Vertex {v2} not found")
        except:
            raise KeyError(f"Vertex {v1} not found")
        
    def __str__(self):
        """
        When called in print()
        """
        return str(self.graph)
        
            
if __name__ == "__main__":
    # For testing
    graph_dict = {"Node1": {}}
    my_graph = Graph(graph_dict=graph_dict)
    my_graph.add_edge("Node2", "Node1", 10)
    print(my_graph)