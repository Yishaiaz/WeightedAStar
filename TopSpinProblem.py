import numpy as np
import time
import math
from aStar import Node, aStar
import copy


class TrayTopSpin:
    def __init__(self, scrambled_array: np.array = None, array_size: int = 10, k_param: int = 3):
        if scrambled_array is None:
            sorted_array = np.linspace(0, array_size - 1, array_size)
            np.random.shuffle(sorted_array)
            self.array = sorted_array
            self.k_param = k_param
        else:
            self.array = scrambled_array
            self.k_param = k_param
            
    def __hash__(self):
        return hash( self.array.tostring() )

    def __repr__(self):
        return ", ".join(['{0}'.format(x) for x in self.array])

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.array, other.array)
        return False
    

class TopSpinNode(Node):
    def __init__(self, parent=None, position: TrayTopSpin = None):
        super(TopSpinNode, self).__init__(parent=parent, position=position)

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __hash__(self):
        return hash( (self.position) )

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.position.array, other.position.array)
        return False

    def __repr__(self):
        return str(self.position)

    def flip(self,idx, K, board):
        temp = copy.deepcopy(board)
        last_idx = idx + K - 1
        for i in range(idx, idx + K):
            temp[i % len(board)] = board[last_idx % len(board)]
            last_idx = last_idx - 1
        return temp

    def get_children(self, maze: TrayTopSpin, end_node, weight, pure_h=False):
        k_param = self.position.k_param
        board = self.position.array
        children = []
        for i in range(0, len(board)):
            child = self.flip(i, k_param, board)
            child = TopSpinNode(parent=self, position=TrayTopSpin(scrambled_array=child, k_param=k_param))
            child.g = self.g + 1
            child.h = self.get_h(child.position)
            child.f = child.g + weight*child.h

            children.append(child)
        return children

    def get_h(self, tray: TrayTopSpin, end_node_: Node = None, parent_h: float = 0.0):
        this_tray_ring = tray.array
        h = 0
        for k in range(len(this_tray_ring) - 1):
            # if int(this_tray_ring[k])!=k:
                # h+=1
            if this_tray_ring[k] > this_tray_ring[k+1]:
                h +=1
            # current_num_location = np.where(this_tray_ring == k)[0]
            # consecutive_num_location = np.where(this_tray_ring == k + 1)[0]
            # h += abs(consecutive_num_location - current_num_location) / self.position.k_param
        return h / self.position.k_param

    # def get_children(self, maze: TrayTopSpin, end_node, weight, pure_h=False):

def solution_path(current_node, maze, total_nodes_expanded, total_nodes_generated):
    nodes_in_path = []
    current_node = copy.deepcopy(current_node)
    while current_node is not None:
        nodes_in_path.append(current_node)
        current_node = current_node.parent
    path_len = len(nodes_in_path)-1
    return nodes_in_path[::-1], path_len, total_nodes_expanded, total_nodes_generated

# w=1
# array_size = 7
# k_param = 3
# # array = np.array([4, 5, 1, 0, 3, 6, 2], dtype=float)
# start_tray = TrayTopSpin(array_size=array_size, k_param=k_param)
# #
# # start_tray = TrayTopSpin(scrambled_array=array, k_param=2)
# print(start_tray)
# while w < 10:
#     now = time.time()
#     start_node = TopSpinNode(position=start_tray)
#     end_goal = TopSpinNode(position=TrayTopSpin(scrambled_array=np.linspace(0, array_size - 1, array_size), k_param=k_param))
#     try:
#         path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=start_tray, start=start_node, end=end_goal, weight=w, pure=False, sol_path_func=solution_path)
#     except Exception as e:
#         start_tray = TrayTopSpin(array_size=array_size, k_param=3)
#         print(start_tray)
#         start_node = TopSpinNode(position=start_tray)
#         end_goal = TopSpinNode(
#         position=TrayTopSpin(scrambled_array=np.linspace(0, array_size - 1, array_size), k_param=k_param))
#         w = 0
#         continue
#
#     print("w: {0} expanded: {1}, path cost: {2}, nodes generated: {4}, time: {3}".format(w,
#                                                                        total_nodes_expanded,
#                                                                        path_cost                                                        time.time() - now,
#                                                                         total_nodes_generated))
#     w += 1
#
