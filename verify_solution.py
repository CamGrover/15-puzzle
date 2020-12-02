class Node:
    def __init__(self, position):
        self.position = position

    def set_position(self, position):
        if 0 <= position <= 15:
            self.position = position

    def top(self):
        if self.position >= 4:
            return self.position - 4
        return None

    def bottom(self):
        if self.position <= 11:
            return self.position + 4

    def left(self):
        if self.position % 4 >= 1:
            return self.position - 1
        return None

    def right(self):
        if self.position % 4 <= 2:
            return self.position + 1


def generate_graph(arr: [int]) -> []:
    graph = [0] * (len(arr) + 1)
    for i, el in enumerate(arr):
        graph[el] = i
    return graph


def viable_move(graph, tile):
    diff = graph[16] - graph[tile]
    if diff in [-1, 1, -4, 4]:
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
    for i, el in enumerate(end):
        if graph[el] != i:
            return False
    return True


def main():
    m = 106
    s = [7, 15, 6, 2, 1, 9, 11, 4, 5, 13, 12, 3, 14, 10, 8, 16]
    g = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    solution = [8, 10, 13, 9, 15, 7, 1, 15, 11, 6, 2, 4, 6, 12, 3, 6, 12, 3,
                9, 11, 7, 2, 3, 7, 15, 5, 11, 15, 7, 12, 6, 9, 12, 6, 9, 8,
                10, 13, 15, 7, 6, 12, 7, 15, 13, 10, 8, 7, 12, 9, 7, 8, 10,
                12, 9, 7, 8, 10, 12, 13, 15, 11, 14, 15, 13, 9, 11, 13, 9,
                11, 11, 9, 15, 14, 13, 15, 9, 11, 15, 9, 14, 13, 9, 15, 10,
                12, 11, 14, 15, 10, 14, 11, 12, 14, 11, 15, 10, 11, 14, 12,
                15, 14, 11, 10, 14, 15]

    print(verify(m, solution, s, g))


if __name__ == "__main__":
    main()
