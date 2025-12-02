import random
import math

class WeightedGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # Initialize a 2D matrix with None
        self.adj_matrix = [[None] * (num_nodes + 1) for _ in range(num_nodes + 1)]

        # Initialize a (x, y) coordinate for each vertex
        # This will be used to calcualte the distance
        self.coordinates = {}
        for node in range(1, num_nodes + 1):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            self.coordinates[node] = (x, y)

# ----------- Basic Operations --------------

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

# -------- Printing has a column and row headings --------------

    def print_graph(self):
        # Print the adjacency adj_matrix
        n = self.num_nodes

        # Header row: column vertex labels
        header = "    " + " ".join(f"{j:7}" for j in range(1, n + 1))
        print(header)

        # Each row: row label + matrix values
        for i in range(1, n + 1):
            row_vals = []
            for j in range(1, n + 1):
                val = self.adj_matrix[i][j]
                cell = "-" if val is None else val
                row_vals.append(f"{cell:>7}")

            print(f"{i:3} " + " ".join(row_vals))

    def edge_exists(self, node1, node2):
        if (self.adj_matrix[node1][node2] is not None and self.adj_matrix[node2][node1] is not None):
            return True
        return False

# ------------ Distance formula ------------------
    def distanceCal(self, u, v):
        x1, y1 = self.coordinates[u]
        x2, y2 = self.coordinates[v]

        distance = round(math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2)), 2)

        return distance

# ----------- Simulate "Travel time" from u to v ------
    def edgeTimeCost(self, u, v):
        """
        Components:
        - Base time: from distance give speed a unit of time say 10 units of time
        - Traffic penalty: picks a random number out of 0, 2, or 4 units of time
        - Light penalty: another random selection between 0 to 3 with each adding 1.5 units of time
        """
        distance = self.distanceCal(u,v)
        baseTime = distance / 10.0

        trafficLevel = random.choice([0,1,2])
        trafficPenalty = trafficLevel * 2.0

        numLights = random.randint(0,3)
        lightPenalty = numLights * 1.5

        return round(baseTime + trafficPenalty + lightPenalty, 2)
