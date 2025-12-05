from christofides_v1 import*
from heldkarp import*
from nn_2opt import*
import time

if __name__ == '__main__':

    numNodes = int(input("Enter how many nodes you want: "))
    print(f"Number of nodes set to: {numNodes}")

    g = randomWeightedComplete(numNodes)
    g.print_graph()


    fides_start_time = time.time()
    christofidesCost, christofidesTour = christofides(g)
    fides_end_time = time.time()

    fides_final_time = fides_end_time - fides_start_time

    karp_start_time = time.time()
    karp_cost, karp_path = held_karp(numNodes, g.adj_matrix)
    karp_end_time = time.time()








