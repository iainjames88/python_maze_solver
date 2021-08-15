import collections

maze = [
    [1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, -1, -1, -1, 0, 0, -1, 0, -1],
    [-1, 0, -1, 0, 0, 0, 0, -1, 0, -1],
    [-1, 0, -1, 0, 0, -1, 0, -1, 0, -1],
    [-1, -1, -1, -1, 2, -1, -1, -1, -1, -1]
]

CELL_KEYS = {
    -2: 'x',
    -1: "#",
    0: ".",
    1: "S",
    2: "E",
    3: "o",
    9: "Y"
}

DIRECTIONS = {
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
}


class Node:
    def __init__(self, row, cell, parent):
        self.row = row
        self.cell = cell
        self.parent = parent


def print_maze(maze):
    for row in maze:
        for cell in row:
            print(CELL_KEYS[cell], end="")
        print()
    print()


def get_neighbours(maze, current_node):
    neighbours = []

    for direction in DIRECTIONS:
        row = current_node.row + direction[0]
        cell = current_node.cell + direction[1]

        if row < 0 or row >= len(maze) or cell < 0 or cell >= len(maze[current_node.row]):
            continue

        if maze[row][cell] < 0:
            continue

        neighbours.append(Node(row, cell, current_node))

    return neighbours


def backtrack(maze, current_node):
    path = [current_node]

    while current_node.parent:
        maze[current_node.row][current_node.cell] = 9
        path.append(current_node.parent)
        current_node = current_node.parent

    maze[current_node.row][current_node.cell] = 9

    return path


if __name__ == "__main__":
    q = collections.deque()
    visited = []

    current_node = start_node = Node(0, 0, None)
    q.append(current_node)

    print_maze(maze)

    while len(q) > 0:
        current_node = q.popleft()
        maze[current_node.row][current_node.cell] = 3
        print_maze(maze)

        for neighbour in get_neighbours(maze, current_node):
            if maze[neighbour.row][neighbour.cell] == 2:
                backtrack(maze, neighbour)
                print_maze(maze)
                import sys;

                sys.exit(0)
            else:
                q.append(neighbour)
        maze[current_node.row][current_node.cell] = -2
        visited.append(current_node)
