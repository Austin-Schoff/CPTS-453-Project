from prims import Prim
from randomGraph import randomWeightedComplete
import math
import time

def get_mst_adj_list(T,n):
    """
    Convert the parent array T (from Prim) into an adjacency list 
    for the MST. Vertices are 1..n
    """

    # Create a dictonary for the adj list
    adj_list = {i: [] for i in range(1, n + 1)}

    for vertex in range(1, n + 1):
        parent = T[vertex]
        if parent != -1:
            adj_list[parent].append(vertex)
            adj_list[vertex].append(parent)

    return adj_list

def odd_degree_vertices(T, n):
    """
    Return the list of vertices in the MST that have odd degree 
    """
    adj_list = get_mst_adj_list(T, n)
    odd_degree_list = []

    for vertex in range(1, n + 1):
        if len(adj_list[vertex]) % 2 == 1:
            odd_degree_list.append(vertex)

    return odd_degree_list

def greedy_matching(graph, odd_degree_vertices):
    """
    Compute a greedy minimum-weight perfect matching on the odd-degree vertices. Returns a list of edges (u,v)
    """

    # vertices we still need to match 
    unmatched = set(odd_degree_vertices)

    matching = []

    # There should always be an even number of odd vertices in a graph
    assert len(unmatched) % 2 == 0, "The number of odd-degree vertices has to be even"

    while unmatched:
        v = unmatched.pop()     # Take one odd vertex from the list
        best_u = None           # Best matching vertex
        best_weight = math.inf

        # Find the nearest neighbor among the remaing unmatched odd vertices
        for u in unmatched:
            weight = graph.adj_matrix[v][u]
            if weight < best_weight:
                best_weight = weight
                best_u = u


        # Pair v with its nearest neighbor
        unmatched.remove(best_u)
        matching.append((v, best_u))

    return matching

def build_multigraph(T, matching, n):
    """
    Build the multigraph used in Christofides:
    Start with the MST (given by the partent array T) and 
    add the matching edges

    Returns an adjacency list: dict {vertex: [neighbors...]}.
    Multiple entries in the list represent multi-edges.
    """

    # start with the MST adjacency list
    adj_list = get_mst_adj_list(T, n)

    # Add each matching edge as another undirected edge
    for u, v in matching:
        adj_list[u].append(v)
        adj_list[v].append(u)

    return adj_list

def dfs_count(v, adj, visited):
    # DFS to count reachable vertices from visted
    visited.add(v)
    for neighbors in adj[v]:
        if neighbors not in visited:
            dfs_count(neighbors, adj, visited)

def is_bridge(u, v, adj):
    """
    Return True if edge (u, v) is a brige in the current graph.
    adj is a dict: vertex -> list of neighbors (multi-edges allowed).
    """

    # if (u, v) is the only edge out of u, we can't avoid it 
    if len(adj[u]) == 1:
        return False

    # Count reachable vertices from u BEFORE removing edge
    vistited_before = set()
    dfs_count(u, adj, vistited_before)
    count_before = len(vistited_before)

    # --- Remove ONE copy of edge (u, v)
    adj[u].remove(v)
    adj[v].remove(u)

    # Count reachable verticies from u after removing edge
    visited_after = set()
    dfs_count(u, adj, visited_after)
    count_after = len(visited_after)

    # Restore the edge
    adj[u].append(v)
    adj[v].append(u)

    return count_after < count_before

def fleury(multigraph):
    """
    Compute an Eulerian tour using Fleury's algorithm.

    multigraph: dict {vertex: [neighbors...]} (multi-edges allowed)
    Assumes:
      - every vertex with nonzero degree has even degree
      - the graph is connected on those vertices
    Returns:
      list of vertices in tour order, e.g. [1, 2, 3, 1, 4, 5, 1]
    """
    start = 1

    # Work on a copy so we don't destroy the original
    adj = {v: multigraph[v][:] for v in multigraph}

    # Total number of undirected edges (each counted twice in adjacency)
    total_edges = sum(len(adj[v]) for v in adj) // 2 
    used_edges = 0

    current = start
    tour = [current]

    while used_edges < total_edges:
        neighbors = adj[current]
        if not neighbors:
            # Shouldn't happen in a correct Eulerian graph
            break

        # Try to pick a neighbor that is not a is_bridge
        next_vertex = None
        for neighbor in neighbors:
            if not is_bridge(current, neighbor, adj):
                next_vertex = neighbor
                break

        # If all neighbors lead to bridges, we have to use one
        if next_vertex is None:
            next_vertex = neighbors[0]

        # Use edge (curr, next_vertex): remove one copy each side
        adj[current].remove(next_vertex)
        adj[next_vertex].remove(current)
        used_edges += 1

        current = next_vertex
        tour.append(current)

    return tour

def shortcut_tour(graph, euler_tour):
    """
    Given an Eulerian tour (list of vertices, with repeats),
    build a TSP tour by skipping already-visited vertices
    and compute its total cost using the original graph weights.

    Returns: (tsp_tour, total_cost)
    """

    if not euler_tour:
        return [], 0.0

    visited = set()
    tsp_tour = []

    start = euler_tour[0]

    for v in euler_tour:
        if v not in visited:
            tsp_tour.append(v)
            visited.add(v)

    # Make it a cycle: return to start if not already There
    if tsp_tour[-1] != start:
        tsp_tour.append(start)

    # compute total cost along the tsp tour
    total_cost = 0.0
    for i in range(len(tsp_tour) - 1):
        u = tsp_tour[i]
        v = tsp_tour[i + 1]
        weight = graph.adj_matrix[u][v]
        total_cost += weight

    total_cost = round(total_cost, 2)

    return tsp_tour, total_cost




def christofides(graph):

    # Number of nodes in the graph
    n = graph.num_nodes

    # Step 1: MST
    mst = Prim(graph)

    # Step 2: find odd-degree vertices in the MST
    odd_degrees = odd_degree_vertices(mst, n)

    # Step 3: find a minimum-weight perfect matching in the subgraph
    matching = greedy_matching(graph, odd_degrees)
 
    #step 4: Build multigraph = MST + matching edges
    multigraph = build_multigraph(mst, matching, n)

    # Step 5: Eulerian tour using Fleury
    euler = fleury(multigraph)

    # Step 6: shortcut Euler tour to TSP tour
    tsp_tour, tsp_cost = shortcut_tour(graph, euler)


    return tsp_tour, tsp_cost


if __name__ == "__main__":

    g = randomWeightedComplete(10)
    
    start = time.time()
    tour, cost = christofides(g)
    end = time.time()

    print(f"Christofides runtime: {end - start}, seconds")
    

