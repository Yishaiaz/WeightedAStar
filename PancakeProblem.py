import numpy as np
from random import randint
from functools import reduce
from aStar import Node, aStar


class Tray:
    max_size_of_pancake = 20
    min_size_of_pancake = 1

    def __init__(self, pancakes: np.ndarray = None, number_of_pancakes: int=3):
        if pancakes is None:
            self.pancakes = np.zeros((number_of_pancakes))
            for i in range(len(self.pancakes)):
                self.pancakes[i] = randint(self.min_size_of_pancake, self.max_size_of_pancake)
        else:
            self.pancakes = pancakes

    def __hash__(self):
        return hash(tuple(self.pancakes))

    def __eq__(self, other):
        return reduce(lambda x, y: x*y, [self.pancakes[i] == other.pancakes[i] for i in range(len(self.pancakes))])

def get_goal_tray(tray: Tray):
    pancakes = tray.pancakes
    return Tray(pancakes=np.sort(pancakes, kind='mergesort')[::-1])


def get_h(tray: Tray, end_node: Node):
    this_tray_pancakes = tray.pancakes
    goal_tray_pancakes = end_node.position.pancakes
    h = 0
    for k, v in enumerate(goal_tray_pancakes):
        if v != this_tray_pancakes[k]:
            h += 1
    return h


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
        return reduce(lambda x, y: x*y, [self.position.pancakes[i]==other.position.pancakes[i] for i in range(len(self.position.pancakes))])

    def get_children(self, maze: Tray, end_node, weight, pure_h):
        children = []
        for i in range(len(maze.pancakes)-1):
            new_pancake_order = np.copy(maze.pancakes)
            new_pancake_order[i:] = maze.pancakes[i:][::-1]
            new_tray = Tray(pancakes=new_pancake_order, number_of_pancakes=0)
            child = PancakeNode(parent=self, position=new_tray)
            # todo change h and g and f
            child.g = self.g + 1
            child.h = weight * get_h(child.position, end_node)
            child.f += child.g + child.h
            children.append(child)
        return children

    def __repr__(self):
        return "".join(["{0}, ".format(x) for x in self.position.pancakes])



starting_tray = Tray(None, 3)
goal_tray = get_goal_tray(starting_tray)
starting_node = PancakeNode(parent=None, position=starting_tray)
goal_node = PancakeNode(parent=None, position=goal_tray)
sol_path = aStar(maze=starting_tray, start=starting_node, end=goal_node, weight=1, pure_h=False)