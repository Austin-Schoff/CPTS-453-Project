from weightedGraph import *
import heapq
import math

def build_tree(T):
    """Builds a dictionary representing the tree from the list of parents."""
    n = len(T) - 1
    tree = {i: [] for i in range(1, n + 1)}  # Create an empty list for each node
    root = None

    # Construct the tree
    for child in range(1, n + 1):
        parent = T[child]
        if parent == -1:
            root = child  # Node with no parent is the root
        else:
            tree[parent].append(child)

    return tree, root

def print_tree(T):
    tree, root = build_tree(T)
    def print_tree(node, level=0):
        indent = "  " * level
        print(f"{indent} - Node {node}")
        for child in tree[node]:
            print_tree(child, level + 1)

    if root is not None:
        print_tree(root)
    else:
        print("No root found")

def get_neighbors(g, node):
    neighbors = []
    for i in range(1, g.num_nodes + 1):
        weight = g.adj_matrix[node][i]
        if weight != 0:
            neighbors.append((i, weight))
    return neighbors

def Prim(g):

    root = 1  # assign vertex 1 as the root
    Visited = [False] * (g.num_nodes + 1) # visited set
    T = [-1] * (g.num_nodes + 1) # tree
    pq = []  # Priority queue to store vertices that are being processed
    c = [math.inf] * (g.num_nodes + 1) # vertex cost
    c[root] = 0 # vertex cost of the root is 0
    heapq.heappush(pq, (0, root)) # insert the first item to priority queue

    # TODO: implement the while loop
    # See here https://docs.python.org/3/library/heapq.html for more information about heapq.
    while pq:
        _, u = heapq.heappop(pq)
        if Visited[u]:
            continue
        Visited[u] = True
        for v, weight in get_neighbors(g,u):
            if not Visited[v] and weight < c[v]:
                T[v] = u
                c[v] = weight
                heapq.heappush(pq, (c[v], v))
        
    return T

"""
# test
test_graph = WeightedGraph(5)
test_graph.add_edge(1,4, 2)
test_graph.add_edge(1,3, 4)
test_graph.add_edge(2,4, 6)
test_graph.add_edge(2,3, 1)
test_graph.add_edge(3,4, 3)
test_graph.add_edge(3,5, 10)
test_graph.add_edge(4,5, 5)
print("\nTest 1:")
print_tree(Prim(test_graph))

test_graph1 = WeightedGraph(3)
test_graph1.add_edge(1, 2, 10)
test_graph1.add_edge(2, 3, 1)
test_graph1.add_edge(1, 3, 2)
print("\nTest 2:")
print_tree(Prim(test_graph1))

test_graph2 = WeightedGraph(4)
test_graph2.add_edge(1, 2, 1)
test_graph2.add_edge(2, 3, 1)
test_graph2.add_edge(3, 4, 1)
test_graph2.add_edge(4, 1, 1)
test_graph2.add_edge(1, 3, 5)
test_graph2.add_edge(2, 4, 5)
print("\nTest 3:")
print_tree(Prim(test_graph2))

test_graph3 = WeightedGraph(4)
test_graph3.add_edge(1, 2, 3)
test_graph3.add_edge(1, 3, 2)
test_graph3.add_edge(1, 4, 5)
print("\nTest 4:")
print_tree(Prim(test_graph3))

test_graph4 = WeightedGraph(5)
test_graph4.add_edge(1, 2, 2)
test_graph4.add_edge(2, 3, 3)
test_graph4.add_edge(3, 4, 4)
test_graph4.add_edge(4, 5, 5)
print("\nTest 5:")
print_tree(Prim(test_graph4))
"""

