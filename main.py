from christofides_v1 import*
from heldkarp import*
from nn_2opt import*
import time

if __name__ == '__main__':

    numNodes = int(input("Enter how many nodes you want: "))
    print(f"Number of nodes set to: {numNodes}")

    g = randomWeightedComplete(numNodes)
    print("Adjacency Matrix:")
    g.print_graph()



    fides_start_time = time.time()
    christofidesTour, christofidesCost = christofides(g)
    fides_end_time = time.time()

    fides_final_time = fides_end_time - fides_start_time

    karp_start_time = time.time()
    karp_cost, karp_path = held_karp(numNodes, g.adj_matrix)
    karp_end_time = time.time()

    karp_final_time = karp_end_time - karp_start_time

    print("\n------------- Christofides Results ----------")
    print(f"Timing Results in Seconds: {fides_final_time}")
    print(f"Path: {christofidesTour}")
    print(f"Cost: {christofidesCost}")
    print("------------- End of christofides Results ----\n")

    print("\n------------ Held-Karp Results ----------")
    print(f"Timing Results in Seconds: {karp_final_time}")
    print(f"Path: {karp_path}")
    print(f"Cost: {karp_cost}")
    print("------------- End of Held-Karp Results ----\n")









