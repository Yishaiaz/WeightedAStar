import time
import aStar

def single_run(map, start, finish):
    # start with getting the pure heuristic solution

    pass

file1 = open("maps/arena.map", 'r')
maze = aStar.make_maze_from_file(file1)

print(maze)