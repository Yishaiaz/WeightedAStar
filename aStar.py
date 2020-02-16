import math
from heapq import heappush, heappop
from pyvisgraph.shortest_path import priority_dict
import queue as Q


def euclidean_distance(start, end):
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __hash__(self):
        return hash(self.position)

    def get_children(self, end_node, weight: float, **kwargs): # todo: remove graph parameter & add the Weighted W
        children = []

        return children


def solution_path(current_node, maze): # todo: remove graph parameter
    path_cost = current_node.g
    path = []
    current = current_node
    # while current is not None:
    #     path.append((current.position[0], current.position[1]))
    #     if maze is not None:
    #         maze[current.position[1]][current.position[0]] = 2
    #         if current.parent is not None:
    #             # sub_path = graph[current.parent.position][current.position]['path'][1:-1][::-1]
    #             # for point in sub_path:
    #             #     path.append(point)
    #     current = current.parent
    # if maze is not None:
    #     for point in path:
    #         maze[point[1]][point[0]] = 2
    # print(path_cost)
    return path[::-1]  # Return reversed path
    # return path_cost


def aStar(maze, start, end):
    # Create start and end node
    # start_node = Node(None, start)
    # start_node.h = euclidean_distance(start, end)
    # start_node.f = start_node.g + start_node.h
    # end_node = Node(None, end)

    # Initialize both open and closed list
    open_list_queue = Q.PriorityQueue()
    open_list = dict()
    closed_list = []

    # Add the start node
    # heappush(open_list, start_node)
    open_list_queue.put(start)
    open_list[(start)] = start
    # Loop until you find the end
    while len(open_list.values()) > 0:
        # Get the current node
        current_node = open_list_queue.get()
        if current_node not in open_list:
            continue
        open_list.pop((current_node))
        # Pop current off open list, add to closed list
        closed_list.append(current_node)
        # Found the goal
        if current_node.position == end.position:
            return solution_path(current_node, maze)

        # Generate children
        children = current_node.get_children(end)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Child is already in the open list
            if child in open_list:
                dup_child = open_list[(child)]
                if child.g < dup_child.g:
                    open_list.pop((dup_child))
                    open_list_queue.put(child)
            # Add the child to the open list
            else:
                open_list_queue.put(child)
                open_list[(child)] = child


def make_maze_from_file(map_file):
    lines = []
    for line in map_file:
        lines.append(line)
    height = int(lines[1].split()[1])
    width = int(lines[2].split()[1])
    maze = [[0 for x in range(width)] for y in range(height)]
    for i in range(0, len(maze)):
        maze_row = lines[i+4]
        for j in range(0, len(maze[0])):
            cell = 1
            if maze_row[j] == ".":
                cell = 0
            maze[i][j] = cell
    # print_maze(maze)
    return maze