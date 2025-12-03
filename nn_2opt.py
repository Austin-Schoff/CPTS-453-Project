import argparse
import random
import time
import math

from randomGraph import randomWeightedComplete as generate_graph
# If you want pure random weights instead:
# from randomCompleteWeightedGraph import randomWeightedComplete as generate_graph


# ---------------------------
# Helpers over your graph API
# ---------------------------
def nodes_list(graph):
    return list(range(1, graph.num_nodes + 1))

def w(graph, u, v):
    return graph.adj_matrix[u][v]

def tour_cost(graph, tour):
    total = 0.0
    n = len(tour)
    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]
        total += w(graph, a, b)
    return total

def assert_symmetric_complete(graph):
    n = graph.num_nodes
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                continue
            wij = graph.adj_matrix[i][j]
            wji = graph.adj_matrix[j][i]
            assert wij != 0 and wji != 0, f"Missing edge between {i} and {j}"
            assert abs(wij - wji) < 1e-9, f"Asymmetry detected on ({i},{j}): {wij} vs {wji}"


# ---------------------------
# Nearest Neighbor
# ---------------------------
def nearest_neighbor(graph, start=1):
    n = graph.num_nodes
    unvisited = set(range(1, n + 1))
    tour = [start]
    unvisited.remove(start)

    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda u: w(graph, last, u))
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour


# ---------------------------
# 2-opt
# ---------------------------
def two_opt(graph, tour):
    n = len(tour)
    improved = True

    def gain(i, k):
        a, b = tour[i - 1], tour[i]
        c, d = tour[k - 1], tour[k % n]
        old_cost = w(graph, a, b) + w(graph, c, d)
        new_cost = w(graph, a, c) + w(graph, b, d)
        return old_cost - new_cost  # positive = improvement

    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                if k == i + 1:
                    continue
                g = gain(i, k)
                if g > 1e-12:
                    tour[i:k] = reversed(tour[i:k])
                    improved = True
    return tour


# ---------------------------
# Multi-start NN
# ---------------------------
def nn_multistart(graph, starts=None):
    if starts is None:
        starts = nodes_list(graph)

    best_tour = None
    best_cost = math.inf

    for s in starts:
        t = nearest_neighbor(graph, start=s)
        c = tour_cost(graph, t)
        if c < best_cost:
            best_cost = c
            best_tour = t
    return best_tour, best_cost


# ---------------------------
# Pretty print Hamiltonian cycle
# ---------------------------
def print_cycle(tour):
    cycle = tour + [tour[0]]  # return to start
    return " → ".join(str(x) for x in cycle)


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Run NN + 2-opt on a weighted complete graph.")
    parser.add_argument("-n", "--nodes", type=int, default=60)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--starts", type=int, default=10)
    args = parser.parse_args()

    random.seed(args.seed)

    # Generate graph
    g = generate_graph(args.nodes)
    assert_symmetric_complete(g)

    all_nodes = nodes_list(g)
    if args.starts <= 0 or args.starts >= len(all_nodes):
        start_nodes = all_nodes
    else:
        start_nodes = random.sample(all_nodes, k=args.starts)

    # Nearest Neighbor
    t0 = time.time()
    nn_tour, nn_cost_open = nn_multistart(g, start_nodes)
    nn_cost = tour_cost(g, nn_tour)
    t1 = time.time()

    # 2-opt
    improved_tour = two_opt(g, nn_tour[:])
    improved_cost = tour_cost(g, improved_tour)
    t2 = time.time()

    # OUTPUT
    print(f"\n=== TSP via Nearest Neighbor + 2-opt ===")
    print(f"Nodes              : {args.nodes}")
    print(f"Start nodes tried  : {len(start_nodes)}")

    print(f"\n--- Nearest Neighbor ---")
    print(f"Cost: {nn_cost:.4f}")
    print(f"Hamiltonian cycle:\n{print_cycle(nn_tour)}")
    print(f"Runtime: {(t1 - t0):.4f}s")

    print(f"\n--- After 2-opt Improvement ---")
    print(f"Cost: {improved_cost:.4f}")
    print(f"Hamiltonian cycle:\n{print_cycle(improved_tour)}")
    print(f"Runtime: {(t2 - t1):.4f}s")
    print(f"Improvement: {nn_cost - improved_cost:.4f}\n")


if __name__ == "__main__":
    main()
