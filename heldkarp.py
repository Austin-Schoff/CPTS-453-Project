from itertools import combinations
import time

def hk_solve(dist):
    n = len(dist)
    # Number of subsets: 2^n
    N = 1 << n
    INF = float('inf')

    # dp[mask][j] = minimum cost to reach subset 'mask' and end at node j
    dp = [[INF] * n for _ in range(N)]
    # parent[mask][j] = previous node before j in optimal path for (mask, j)
    parent = [[None] * n for _ in range(N)]

    # Base case: start at node 0, mask = 1<<0
    dp[1][0] = 0

    # Iterate over all subsets that include node 0
    for mask in range(1, N):
        if not (mask & 1):
            continue  # we always require the tour to start at node 0
        for j in range(1, n):
            if not (mask & (1 << j)):
                continue  # j not in subset
            prev_mask = mask ^ (1 << j)
            # Try all possibilities of coming to j from some k in prev_mask
            for k in range(n):
                if prev_mask & (1 << k):
                    cost = dp[prev_mask][k] + dist[k][j]
                    if cost < dp[mask][j]:
                        dp[mask][j] = cost
                        parent[mask][j] = k

    # Close the tour: return to node 0
    full_mask = (1 << n) - 1
    min_cost = INF
    last = None
    for j in range(1, n):
        cost = dp[full_mask][j] + dist[j][0]
        if cost < min_cost:
            min_cost = cost
            last = j

    # Reconstruct path
    path = []
    mask = full_mask
    curr = last
    while curr is not None:
        path.append(curr)
        prev = parent[mask][curr]
        mask ^= (1 << curr)
        curr = prev
    path.reverse()
    path.append(0)
    path.reverse()

    return min_cost, path

def held_karp(n, dist):
    temp = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            temp[i][j] = dist[i+1][j+1]
    #start = time.time()
    min_cost, zero_based_path = hk_solve(temp)
    #end = time.time()
    path = [x+1 for x in zero_based_path]
    #print("shortest path: " +str(path))
    #print("weight: " +str(zero_based_path[0]))
    #print("execution time: " +str(end - start))

    return min_cost, path


