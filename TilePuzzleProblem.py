import numpy as np
from random import randint, shuffle
import math
from functools import reduce
from aStar import Node, aStar


class Tray:

    def __init__(self, tiles: np.ndarray = None, number_of_tiles: int=16):
        """
        number of tiles must be a power of 2!
        empty tile is assigned the value -1
        :param tiles:
        :param number_of_tiles:
        """
        x = 0
        if tiles is None:
            tiles_per_row = int(math.sqrt(number_of_tiles))
            self.tiles = np.zeros((tiles_per_row, tiles_per_row))
            for i in range(0, len(self.tiles)):
                tiles_len = len(self.tiles[0])
                for j in range(0, tiles_len):
                    if i == 0 and j == 0:
                        self.tiles[i][j] = -1
                        continue
                    self.tiles[i][j] = x
                    x += 1
            np.random.shuffle(self.tiles)
        else:
            self.tiles = tiles

    def __hash__(self):
        return hash(tuple(self.tiles))

    def __repr__(self):
        return "\n".join(["|{0}|".format(",".join(["{0},".format(word)for word in line])) for line in self.tiles])

    def __eq__(self, other):
        return reduce(lambda x, y: x*y, [self.tiles[i] == other.pancakes[i] for i in range(len(self.tiles))])


def get_goal_tray(tray: Tray):
    pancakes = tray.tiles
    return Tray(tiles=np.sort(pancakes, kind='mergesort')[::-1])


def get_h(tray: Tray, end_node: Node):
    this_tray_pancakes = tray.tiles
    goal_tray_pancakes = end_node.position.pancakes
    h = 0
    for k, v in enumerate(goal_tray_pancakes):
        if v != this_tray_pancakes[k]:
            h += 1
    return h


def solution_path(current_node, maze, total_nodes_expanded, total_nodes_generated):
    path = []
    while(current_node!=None):
        path.append(current_node)
        current_node = current_node.parent
    path_cost = len(path)
    return path[::-1], path_cost, total_nodes_expanded, total_nodes_generated


class PancakeNode(Node):

    def __init__(self, parent=None, position:Tray =None):
        super(PancakeNode, self).__init__(parent=parent, position=position)

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __hash__(self):
        return hash((self.position))

    def __eq__(self, other):
        if type(other) == type(self):
            return reduce(lambda x, y: x*y, [self.position.pancakes[i]==other.position.pancakes[i] for i in range(len(self.position.pancakes))])
        return False

    def get_children(self, maze: Tray, end_node, weight, pure_h):
        children = []
        for i in range(len(self.position.pancakes)-1):
            new_pancake_order = np.copy(self.position.pancakes)
            new_pancake_order[i:] = new_pancake_order[i:][::-1]
            new_tray = Tray(tiles=new_pancake_order, number_of_tiles=0)
            child = PancakeNode(parent=self, position=new_tray)
            # todo change h and g and f
            child.g = self.g + 1
            child.h = weight * get_h(child.position, end_node)
            if not pure_h:
                child.f = child.g + child.h
            else:
                child.f = child.h
            children.append(child)
        return children

    def __repr__(self):
        return "".join(["{0}, ".format(x) for x in self.position.pancakes])



starting_tray = Tray(None, 16)
print(starting_tray)
# goal_tray = get_goal_tray(starting_tray)
# starting_node = PancakeNode(parent=None, position=starting_tray)
# goal_node = PancakeNode(parent=None, position=goal_tray)
# path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=starting_tray, start=starting_node, end=goal_node, weight=2, pure_h=False, sol_path_func=solution_path)
# print(total_nodes_expanded)