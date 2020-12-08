def generate_graph(arr: [int]) -> []:
    graph = [0] * (len(arr) + 1)
    for pos, tile in enumerate(arr):
        graph[tile] = pos
    return graph


def viable_move(graph, tile):
    if 1 <= tile <= 15 and graph[16] - graph[tile] in [-1, 1, -4, 4]:
        return True
    return False


def verify(moves: int, solution: [int], start: [int], end: [int]) -> bool:
    if moves != len(solution):
        return False
    graph = generate_graph(start)
    for el in solution:
        if viable_move(graph, el):
            graph[el], graph[16] = \
                graph[16], graph[el]
        else:
            return False
    for i, el in enumerate(end):
        if graph[el] != i:
            return False
    return True
