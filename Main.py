import time
import aStar
from aStar import Node


def single_run(map, start, finish):
    # start with getting the pure heuristic solution

    pass

# file1 = open("maps/arena.map", 'r')
# maze = aStar.make_maze_from_file(file1)
maze = [
    [0,1,1,1,1],
    [0,1,0,0,0],
    [0,0,0,1,0],
]
start = Node(None, position=(0, 0))
end = Node(None, position=(4, 2))
sol_path, path_cost = aStar.aStar(maze, start, end, 1)
print(sol_path)