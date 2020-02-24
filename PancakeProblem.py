import numpy as np
from random import randint
from functools import reduce
from aStar import Node, aStar


class Tray:

    def __init__(self, pancakes: np.ndarray = None, number_of_pancakes: int=3):
        if pancakes is None:
            self.pancakes = np.zeros((number_of_pancakes))
            for i in range(len(self.pancakes)):
                self.pancakes[i] = i
            temp = np.copy(self.pancakes)
            np.random.shuffle(temp)
            self.pancakes = temp
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
    # goal_tray_pancakes = end_node.position.pancakes
    h = 0
    for k in range(len(tray.pancakes) - 1):
        # if int(this_tray_ring[k])!=k:
        # h+=1
        if this_tray_pancakes[k] -1 != this_tray_pancakes[k + 1] and  this_tray_pancakes[k] + 1 != this_tray_pancakes[k + 1]:
            h += 1
    if this_tray_pancakes[len(this_tray_pancakes)-1] != len(this_tray_pancakes)-1:
        h+=1

    # for k, v in enumerate(goal_tray_pancakes):
    #     if v != this_tray_pancakes[k]:
    #         h += 1
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

    def get_children(self, maze: Tray, end_node, weight, pure_h=False):
        children = []
        for i in range(len(self.position.pancakes)-1):
            new_pancake_order = np.copy(self.position.pancakes)
            new_pancake_order[i:] = new_pancake_order[i:][::-1]
            new_tray = Tray(pancakes=new_pancake_order, number_of_pancakes=0)
            child = PancakeNode(parent=self, position=new_tray)
            child.g = self.g + 1
            child.h = weight * get_h(child.position, end_node)
            # print("hello")
            if not pure_h:
                child.f = child.g + child.h
            else:
                child.f = child.h
            children.append(child)
        return children

    def __repr__(self):
        return "".join(["{0}, ".format(x) for x in self.position.pancakes])



# starting_tray = Tray(None, 8)
# goal_tray = get_goal_tray(starting_tray)
# starting_node = PancakeNode(parent=None, position=starting_tray)
# goal_node = PancakeNode(parent=None, position=goal_tray)
# path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=starting_tray, start=starting_node, end=goal_node, weight=5, pure=False, sol_path_func=solution_path)
# print("path cost: {0}, total expanded: {1}, total generated: {2}".format(path_cost, total_nodes_expanded, total_nodes_generated))