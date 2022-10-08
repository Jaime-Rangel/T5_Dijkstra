
def bfs(queue,visited,graph):
    if queue:
        cur_node = queue.popleft()
        next_nodes = graph[cur_node]

        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return visited