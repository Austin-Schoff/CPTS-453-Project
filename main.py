from christofides_v1 import *
from heldkarp import *
from nn_2opt import *
import time

# ------------------------------------------------
# Pretty formatting functions
# ------------------------------------------------
def format_path(path):
    """Return raw path as: 1 → 2 → 3 → 4"""
    return " → ".join(str(x) for x in path)

def format_cycle(path):
    """Return Hamiltonian cycle as: 1 → 2 → 3 → ... → 1"""
    return " → ".join(str(x) for x in (path + [path[0]]))


if __name__ == '__main__':

    # -----------------------------
    # Ask for number of nodes
    # -----------------------------
    while True:
        numNodes = int(input("Enter number of nodes you want: "))
        print(f"Number of nodes set to: {numNodes}")

        # Warn about Held-Karp if needed
        if numNodes > 20:
            print("\n⚠️  WARNING: Held-Karp is exponential and will be VERY slow for > 20 nodes.")
            print("What would you like to do?")
            print("1) Run anyway")
            print("2) Run WITHOUT Held-Karp")
            print("3) Change number of nodes")

            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                runHeldKarp = True
                break
            elif choice == "2":
                runHeldKarp = False
                break
            elif choice == "3":
                continue
            else:
                print("Invalid choice. Try again.\n")
                continue
        else:
            runHeldKarp = True
            break

    # --------------------------------
    # Generate graph
    # --------------------------------
    g = randomWeightedComplete(numNodes)
    print("\nAdjacency Matrix:")
    g.print_graph()

    # --------------------------------
    # Run Christofides
    # --------------------------------
    cf_start = time.time()
    cf_path, cf_cost = christofides(g)
    cf_end = time.time()

    # --------------------------------
    # Run NN + 2-opt
    # --------------------------------
    nn_start = time.time()
    nn_path, nn_cost = nn_search(g, start_nodes=min(10, numNodes))

    # FIXED: Correct parameter order → (graph, tour)
    improved_tour = two_opt(g, nn_path)
    improved_cost = tour_cost(g, improved_tour)
    nn_end = time.time()

    # --------------------------------
    # Run Held-Karp (optional)
    # --------------------------------
    if runHeldKarp:
        hk_start = time.time()
        hk_cost, hk_path = held_karp(numNodes, g.adj_matrix)
        hk_end = time.time()
    else:
        hk_cost, hk_path = None, None

    # --------------------------------
    # Print Results
    # --------------------------------
print("\n================== RESULTS ==================\n")

# ---------- Christofides ----------
print("----- Christofides Algorithm -----")
print(f"Cost      : {cf_cost}")
print(f"Path      : {format_path(cf_path)}")
print(f"Runtime   : {cf_end - cf_start:.6f} seconds\n")

# ---------- Nearest Neighbor + 2-opt ----------
print("----- Nearest Neighbor + 2-opt -----")
print(f"NN Cost        : {nn_cost}")
print(f"2-opt Cost     : {improved_cost}")

nn_cycle = improved_tour + [improved_tour[0]]
print(f"Hamiltonian Cycle: {format_path(nn_cycle)}")
print(f"Runtime        : {nn_end - nn_start:.6f} seconds\n")

# ---------- Held-Karp ----------
print("----- Held-Karp Algorithm -----")
if hk_cost is None:
    print("Held-Karp skipped due to node limit.\n")
else:
    print(f"Cost      : {hk_cost}")
    print(f"Path      : {format_path(hk_path)}")
    print(f"Runtime   : {hk_end - hk_start:.6f} seconds\n")

print("============== END OF RESULTS ==============\n")


# ========================================================
#                 SUMMARY COMPARISON TABLE
# ========================================================
print("============== SUMMARY COMPARISON ==============")

# Determine optimal cost for % comparison
optimal_cost = hk_cost if hk_cost is not None else None

def pct_above_opt(cost):
    if optimal_cost is None:
        return "   N/A"
    return f"{((cost - optimal_cost) / optimal_cost) * 100:7.2f}%"

# Build rows
summary_rows = [
    ("Christofides", cf_cost, cf_end - cf_start, pct_above_opt(cf_cost)),
    ("NN + 2-opt", improved_cost, nn_end - nn_start, pct_above_opt(improved_cost)),
    ("Held-Karp" if hk_cost is not None else "Held-Karp (skipped)",
     hk_cost if hk_cost is not None else float('nan'),
     (hk_end - hk_start) if hk_cost is not None else 0,
     "   N/A" if hk_cost is None else pct_above_opt(hk_cost))
]

# Column headers
print(f"{'Algorithm':20} {'Cost':10} {'Runtime (s)':15} {'% Above Optimal':15}")
print("-" * 65)

# Print aligned rows
for name, cost, runtime, pct in summary_rows:
    cost_display = f"{cost:.4f}" if cost == cost else "   N/A"  # NaN-safe
    print(f"{name:20} {cost_display:10} {runtime:15.6f} {pct:15}")

print("\n===============================================\n")
