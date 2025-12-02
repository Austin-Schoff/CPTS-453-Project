import random

class WeightedGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # Initialize a 2D matrix with zeros
        self.adj_matrix = [[None] * (num_nodes + 1) for _ in range(num_nodes + 1)]

    def add_edge(self, node1, node2, w):
        # Add an undirected edge between node1 and node2
        self.adj_matrix[node1][node2] = w
        self.adj_matrix[node2][node1] = w
        

    def remove_edge(self, node1, node2):
        # Remove the edge between node1 and node2
        self.adj_matrix[node1][node2] = None
        self.adj_matrix[node2][node1] = None

    def num_edges(self):
        num_edges = 0
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes + 1):
                if self.adj_matrix[i][j] != None:
                    num_edges += 1
        return num_edges

    def print_graph(self):
        # Print the adjacency adj_matrix
        n = self.num_nodes

        # Header row: column vertex labels
        header = "    " + " ".join(f"{j:3}" for j in range(1, n + 1))
        print(header)

        # Each row: row label + matrix values
        for i in range(1, n + 1):
            row_vals = []
            for j in range(1, n + 1):
                val = self.adj_matrix[i][j]
                cell = "-" if val is None else val
                row_vals.append(f"{cell:>3}")

            print(f"{i:3} " + " ".join(row_vals))

    def edge_exists(self, node1, node2):
        if (self.adj_matrix[node1][node2] != None and self.adj_matrix[node2][node1] != None):
            return True
        return False


def randomWeightedComplete(num_nodes):
   
    randomGraph = WeightedGraph(num_nodes)

    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            if i == j:
                continue
            if randomGraph.edge_exists(i, j):
                continue

            weight = random.randint(1, 10)
            randomGraph.add_edge(i, j, weight)

    return randomGraph




