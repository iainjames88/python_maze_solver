import argparse
import collections
import sys

from colorama import init, Fore
import time
import os

CELL_KEYS = {
    -3: Fore.BLUE,  # visited
    -2: Fore.CYAN,  # queued
    -1: Fore.BLACK,  # wall
    0: Fore.WHITE,  # empty
    1: Fore.LIGHTGREEN_EX,  # current node
    2: Fore.LIGHTRED_EX,  # target node
    3: Fore.YELLOW,  # path node
}

DIRECTIONS = {(-1, 0), (0, 1), (1, 0), (0, -1)}


class Node:
    def __init__(self, row, cell, parent):
        self.row = row
        self.cell = cell
        self.parent = parent


def read_maze(file):
    start_node = None
    maze = []

    for i, line in enumerate(file):
        row = []
        for j, char in enumerate(line.split()):
            if char == "1":
                start_node = Node(i, j, None)
            row.append(int(char))
        maze.append(row)

    return start_node, maze


def print_maze(maze):
    os.system("clear")

    for row in maze:
        for cell in row:
            print(f"{CELL_KEYS[cell]} █", end="")
        print()
    print()


def get_neighbours(maze, current_node):
    neighbours = []

    for direction in DIRECTIONS:
        row = current_node.row + direction[0]
        cell = current_node.cell + direction[1]

        if (
            row < 0
            or row >= len(maze)
            or cell < 0
            or cell >= len(maze[current_node.row])
        ):
            continue

        if maze[row][cell] < 0:
            continue

        neighbours.append(Node(row, cell, current_node))

    return neighbours


def backtrack(maze, current_node):
    path = [current_node]

    while current_node.parent:
        maze[current_node.row][current_node.cell] = 3
        path.append(current_node.parent)
        current_node = current_node.parent

    maze[current_node.row][current_node.cell] = 3

    return path


if __name__ == "__main__":
    init()  # for colorama

    parser = argparse.ArgumentParser()
    parser.add_argument("maze_file", type=argparse.FileType("r"))
    parser.add_argument(
        "--speed", type=float, help="delay in seconds; defaults to 0.3", default=0.3
    )

    args = parser.parse_args()
    start_node, maze = read_maze(args.maze_file)

    q = collections.deque()

    q.append(start_node)

    while len(q) > 0:
        current_node = q.popleft()
        maze[current_node.row][current_node.cell] = 1
        print_maze(maze)

        for neighbour in get_neighbours(maze, current_node):
            if maze[neighbour.row][neighbour.cell] == 2:
                backtrack(maze, neighbour)
                print_maze(maze)
                sys.exit(0)
            else:
                q.append(neighbour)
                maze[neighbour.row][neighbour.cell] = -2
                print_maze(maze)

        maze[current_node.row][current_node.cell] = -3
        time.sleep(args.speed)
