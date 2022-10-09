from heapq import *

def dijkstra(cost_visited ,goal, graph, visited):
    cur_cost, cur_node = heappop(queue)
    
    if cur_node == goal:
        queue = []
        return queue

    next_nodes = graph[cur_node]
    for next_node in next_nodes:
        neigh_cost, neigh_node = next_node
        new_cost = cost_visited[cur_node] + neigh_cost

        if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
            heappush(queue, (new_cost, neigh_node))
            cost_visited[neigh_node] = new_cost
            visited[neigh_node] = cur_node

    return queue,cur_node,cost_visited,visited