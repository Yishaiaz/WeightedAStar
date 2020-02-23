import numpy as np
import time
import math
from aStar import Node, aStar


class TrayTopSpin:
    def __init__(self, scrambled_array: np.array = None, array_size: int = 10, k_param: int = 3):
        if scrambled_array:
            sorted_array = np.linspace(0, array_size, 1)
            np.random.shuffle(sorted_array)
            self.array = sorted_array
            self.k_param = k_param
        else:
            self.array = scrambled_array
            self.k_param = k_param
            
    def __hash__(self):
        return hash(self.array.tostring())

    def __repr__(self):
        return "\n".join(["|{0}|".format(",".join(["{0},".format(word)for word in line])) for line in self.tiles])

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.array, other.tiles)
        return False
    

class TilePuzzleNode(Node):
    def __init__(self, parent=None, position: TrayTopSpin = None):
        super(TilePuzzleNode, self).__init__(parent=parent, position=position)

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __hash__(self):
        return hash( (self.position) )

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.position.tiles, other.position.tiles)
        return False

    def get_children(self, maze: TrayTopSpin, end_node, weight, pure_h=False):
        def get_h(tray: TrayTopSpin, end_node_: Node, parent_h: float = 0.0):
            this_tray_ring = tray.array
            h = 0
            for k in range(len(this_tray_ring) - 1):
                current_num = this_tray_ring[k]
                consecutive_num = this_tray_ring[k+1]
                consecutive_num_location = np.where(this_tray_ring == consecutive_num)[0]
                h += abs(consecutive_num_location - k)
            return h

