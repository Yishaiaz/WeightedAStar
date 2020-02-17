import math
import time
from heapq import heappush, heappop
import queue as Q
import copy


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

    def get_children(self, maze, end_node, weight, pure_h=False):
        # print("pure: 3 " + str(pure_h))
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (self.position[0] + new_position[0], self.position[1] + new_position[1])

            # Make sure within range
            if node_position[1] > (len(maze) - 1) or node_position[1] < 0 or node_position[0] > (len(maze[len(maze) - 1]) - 1) or node_position[0] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[1]][node_position[0]] != 0:
                continue

            # Create new node
            new_node = Node(self, node_position)
            if new_position in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_node.g = self.g + math.sqrt(2)
            else:
                new_node.g = self.g + 1
            euclidean_distance = math.sqrt((new_node.position[0] - end_node.position[0]) ** 2 + (new_node.position[1] - end_node.position[1]) ** 2)


            # calculate f with regards to pure search
            if not pure_h:
                new_node.h = weight * euclidean_distance
                new_node.f = new_node.g + new_node.h
            else:
                new_node.h = euclidean_distance
                new_node.f = new_node.h
            # Append
            children.append(new_node)
        return children

    def __repr__(self):
        return "row={},col={}".format(self.position[1],self.position[0])

    def solution_path(current_node, maze, total_nodes_expanded, total_nodes_generated):
        maze = copy.deepcopy(maze)

        path_cost = current_node.g
        path = []
        current = current_node
        while current is not None:
            path.append((current.position[0], current.position[1]))
            if maze is not None:
                maze[current.position[1]][current.position[0]] = 2
            current = current.parent
        if maze is not None:
            for point in path:
                maze[point[1]][point[0]] = 2
        return path[::-1], path_cost, total_nodes_expanded, total_nodes_generated # Return reversed path


def solution_path(current_node, maze, total_nodes_expanded, total_nodes_generated):
    maze = copy.deepcopy(maze)

    path_cost = current_node.g
    path = []
    current = current_node
    while current is not None:
        path.append((current.position[0], current.position[1]))
        if maze is not None:
            maze[current.position[1]][current.position[0]] = 2
        current = current.parent
    if maze is not None:
        for point in path:
            maze[point[1]][point[0]] = 2
    return path[::-1], path_cost, total_nodes_expanded, total_nodes_generated # Return reversed path


def aStar(maze, start, end, weight, sol_path_func=solution_path, pure=False):
    total_nodes_expanded = 0
    total_nodes_generated = 0

    # Create start and end node
    # start_node = Node(None, start)
    # start_node.h = euclidean_distance(start, end)
    # start_node.f = start_node.g + start_node.h
    # end_node = Node(None, end)

    # Initialize both open and closed list
    open_list_queue = Q.PriorityQueue()
    open_list = dict()
    closed_list = dict()

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
        closed_list[(current_node)] = current_node
        # Found the goal
        if current_node.position == end.position:
            return sol_path_func(current_node, maze ,total_nodes_expanded,total_nodes_generated)
        # Generate children
        total_nodes_expanded = total_nodes_expanded + 1
        children = current_node.get_children(maze=maze, weight=weight, end_node=end, pure_h=pure)
        # Loop through children
        for child in children:
            # Child is on the closed list
            if (child) in closed_list:
                continue

            # Child is already in the open list
            if child in open_list:
                dup_child = open_list[(child)]
                if child.g < dup_child.g:
                    open_list.pop((dup_child))
                    open_list_queue.put(child)
                    total_nodes_generated = total_nodes_generated + 1
            # Add the child to the open list
            else:
                open_list_queue.put(child)
                open_list[(child)] = child
                total_nodes_generated = total_nodes_generated + 1


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