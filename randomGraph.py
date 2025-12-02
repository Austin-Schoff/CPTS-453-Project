# Must include the weightedGraph file
from weightedGraph import WeightedGraph

def randomWeightedComplete(numNodes):
    """
    Generates a random weighted complete graph with vertices labeled 1 to numNodes

    - Uses the time-cost model defined in the weightedGraph class (edge_time_cost(***))

    """
    graph = WeightedGraph(numNodes)

    for index in range(1, numNodes + 1):
        for inner_index in range(index + 1, numNodes + 1):
            weight = graph.edgeTimeCost(index,inner_index)
            graph.add_edge(index, inner_index, weight)

    return graph
"""
Small test cases
g = randomWeightedComplete(5)
g.print_graph()
print("Edges:", g.num_edges())
"""

