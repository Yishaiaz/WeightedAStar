import time

import numpy as np
from random import randint
import math
from aStar import Node, aStar
import copy

MOVES = ["UP", "RIGHT", "DOWN", "LEFT"]


class TrayTilePuzzle:

    def __init__(self, tiles: np.ndarray = None, num_of_rows: int = 3, num_of_cols: int = 4):
        """
        number of tiles must be a power of 2!
        empty tile is assigned the value -1
        :param tiles:
        :param number_of_tiles:
        """
        x = 0
        if tiles is None:
            self.tiles = np.zeros((num_of_rows, num_of_cols))
            for i in range(0, len(self.tiles)):
                tiles_len = len(self.tiles[0])
                for j in range(0, tiles_len):
                    if i == 0 and j == 0:
                        self.tiles[i][j] = -1
                        continue
                    self.tiles[i][j] = x
                    x += 1
            self.shuffle_tiles()
        else:
            self.tiles = tiles

    def shuffle_tiles(self):
        """
        function initTiles() {
    var i = tileCount * tileCount - 1;
    while (i > 0) {
      var j = Math.floor(Math.random() * i);
      var xi = i % tileCount;
      var yi = Math.floor(i / tileCount);
      var xj = j % tileCount;
      var yj = Math.floor(j / tileCount);
      swapTiles(xi, yi, xj, yj);
      --i;
    }
  }
        :return:
        """
        tiles = np.copy(self.tiles)
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                rand1 = randint(0, len(tiles)-1)
                rand2 = randint(0, len(tiles)-1)
                temp = tiles[i][j]
                tiles[i][j] = tiles[rand1][rand2]
                tiles[rand1][rand2] = temp
        self.tiles = np.copy(tiles)

    def __hash__(self):
        return hash(self.tiles.tostring())

    def __repr__(self):
        return "\n".join(["|{0}|".format(",".join(["{0},".format(word)for word in line])) for line in self.tiles])

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.tiles, other.tiles)
        return False

        # def check_if_contains(all_tiles, new_tiles):
        #     for old_tile in all_tiles:
        #         if np.array_equal(old_tile, new_tiles):
        #             return True
        #     return False
        #
        # max_number_of_no_move = 50
        # number_of_moves = 200000
        # random_moves = np.random.randint(0, 3, number_of_moves)
        #
        # previous_tiles = []
        # tiles_after_move = np.copy(self.tiles)
        # no_move_ctr = 0
        # total_ctr = 0
        #
        # move = random_moves[total_ctr]
        # while no_move_ctr < number_of_moves and total_ctr < number_of_moves*5:
        #     move_sign = MOVES[move]
        #     tiles_after_move = move_tile(self.tiles, move_sign)
        #     if check_if_contains(previous_tiles, tiles_after_move):
        #         move = random_moves[total_ctr % number_of_moves]
        #         no_move_ctr += 1
        #     else:
        #         no_move_ctr = 0
        #         move = random_moves[total_ctr]
        #         previous_tiles.append(tiles_after_move)
        #         self.tiles = tiles_after_move
        #     total_ctr += 1
        #
        # print("done shuffling")


def move_tile(tiles_puzzle: np.ndarray, move: str):
    tiles = np.copy(tiles_puzzle)
    blank_tile_location = np.where(tiles == -1)
    blank_tile_x = blank_tile_location[0][0]
    blank_tile_y = blank_tile_location[1][0]
    if move == "UP":
        if blank_tile_x - 1 >= 0:
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x - 1][blank_tile_y]
            tiles[blank_tile_x - 1][blank_tile_y] = -1
            return tiles
    elif move == "RIGHT":
        if blank_tile_y + 1 < len(tiles[0]):
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x][blank_tile_y + 1]
            tiles[blank_tile_x][blank_tile_y + 1] = -1
            return tiles
    elif move == "DOWN":
        if blank_tile_x + 1 < len(tiles):
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x + 1][blank_tile_y]
            tiles[blank_tile_x + 1][blank_tile_y] = -1
            return tiles
    elif move == "LEFT":
        if blank_tile_y - 1 >= 0:
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x][blank_tile_y - 1]
            tiles[blank_tile_x][blank_tile_y - 1] = -1
            return tiles
    return tiles


def get_goal_tray(tray: TrayTilePuzzle):
    x = 0
    tiles_per_row = len(tray.tiles)
    tiles_per_col = len(tray.tiles[0])
    tiles = np.zeros((tiles_per_row, tiles_per_col))
    for i in range(0, len(tiles)):
        tiles_len = len(tiles[0])
        for j in range(0, tiles_len):
            if i == 0 and j == 0:
                tiles[i][j] = -1
                continue
            tiles[i][j] = x
            x += 1
    return TrayTilePuzzle(tiles=tiles)


def solution_path(current_node, maze, total_nodes_expanded, total_nodes_generated):
    nodes_in_path = []
    current_node = copy.deepcopy(current_node)
    while current_node is not None:
        nodes_in_path.append(current_node)
        current_node = current_node.parent
    path_len = len(nodes_in_path)-1
    return nodes_in_path[::-1], path_len, total_nodes_expanded, total_nodes_generated


class TilePuzzleNode(Node):
    def __init__(self, parent=None, position: TrayTilePuzzle = None):
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

    def get_children(self, maze: TrayTilePuzzle, end_node, weight, pure_h=False):
        def get_h(tray: TrayTilePuzzle, end_node_: Node, parent_h: float = 0.0):
            h = 0
            current_tiles = tray.tiles
            goal_tiles = end_node_.position.tiles
            for x in range(len(current_tiles)):
                for y in range(len(current_tiles[x])):
                    if current_tiles[x][y] == -1:
                        continue
                    at_goal_location = np.where(goal_tiles == current_tiles[x][y])
                    at_goal_location_x = at_goal_location[0][0]
                    at_goal_location_y = at_goal_location[1][0]
                    x_dis = (at_goal_location_x - x)**2
                    y_dis = (at_goal_location_y - y)**2
                    dis = math.sqrt(x_dis+y_dis)
                    # simpler heuristic, count the number of tiles that are not in place.
                    # dis = 1 if goal_tiles[x][y] != current_tiles[x][y] else 0
                    h += dis
            return h

        children = []
        for move in MOVES:
            child_tiles = move_tile(self.position.tiles, move)
            if child_tiles is None:
                continue
            tile_puzzle_for_child = TrayTilePuzzle(tiles=child_tiles)
            child = TilePuzzleNode(parent=self, position=tile_puzzle_for_child)
            if child == self:
                continue
            child.g = self.g + 1
            child.h = weight * get_h(tray=tile_puzzle_for_child, end_node_=end_node)
            if not pure_h:
                child.f = child.g + child.h
            else:
                child.f = child.h / weight
            children.append(child)
        return children

    def __repr__(self):
        return "\n".join(["|{0}|".format(",".join(["{0},".format(word)
                                                   for word in line])) for line in self.position.tiles])


def read_korf_data(korf_data_path:str):
    maps_by_index = dict()
    file = open(korf_data_path, 'r')
    line = file.readline()
    while line != "" and line is not None:
        if line not in ["\n", "\t", " "]:
            map_index, map_flat = tuple(line.split(','))
            map_flat = np.array([int(x)-1 for x in map_flat.split(' ')])
            map = np.reshape(map_flat, (4, 4))
            maps_by_index[map_index] = map
        line = file.readline()
    return maps_by_index


# reading korf puzzles
# korf_data = read_korf_data("korf_data/korf100.txt")
# array = np.array(
#     [[0.0, 6.0, 1.0, 3.0, 9.0, -1.0],
#      [5.0, 12.0, 8.0, 2.0, 15.0, 4.0],
#      [11.0, 18.0, 7.0, 14.0, 21.0, 10.0],
#      [17.0, 19.0, 13.0, 20.0, 27.0, 16.0],
#      [23.0, 24.0, 25.0, 26.0, 28.0, 22.0],
#      [29.0, 30.0, 31.0, 32.0, 33.0, 34.0]])
# for key in korf_data.keys():
#     array = korf_data[key]
#     starting_tray = TrayTilePuzzle(array, 0)
#     starting_node = TilePuzzleNode(parent=None, position=starting_tray)
#     end_tray = get_goal_tray(starting_tray)
#     goal_node = TilePuzzleNode(parent=None, position=end_tray)
#     print(starting_node)
#     print("\n")
#
#     w = 2
#
#     while w < 10:
#         now = time.time()
#         path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=starting_tray, start=starting_node,
#                                                                              end=goal_node, weight=w, pure=False,
#                                                                              sol_path_func=solution_path)
#         print("w: {0} expanded: {1}, path cost: {2}, nodes generated: {4}, time: {3}".format(w,
#                                                                        total_nodes_expanded,
#                                                                        path_cost,
#                                                                        time.time() - now,
#                                                                         total_nodes_generated))
#         w += 1
array = np.array(
    [
        [6, 5, 4, 3],
        [2, 1, 0, -1],
        [7, 8, 9, 10]
    ]
)
# array = np.array(
#     [
#         [10, 9, 8, 7],
#         [6, 5, 4, 3],
#         [2, 1, 0, -1]
#     ]
# )
# array = np.array(
#     [
#         [2, 1, 0, -1],
#         [6, 5, 4, 3],
#         [10, 9, 8, 7]
#     ]
# )
# starting_tray = TrayTilePuzzle(array, 0)

starting_tray = TrayTilePuzzle(num_of_cols=4)
starting_node = TilePuzzleNode(parent=None, position=starting_tray)
end_tray = get_goal_tray(starting_tray)
goal_node = TilePuzzleNode(parent=None, position=end_tray)
print(starting_node)
print("\n")

w = 1

while w < 10:
    now = time.time()
    path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=starting_tray, start=starting_node,
                                                                         end=goal_node, weight=w, pure=False,
                                                                         sol_path_func=solution_path)
    print("w: {0} expanded: {1}, path cost: {2}, nodes generated: {4}, time: {3}".format(w,
                                                                   total_nodes_expanded,
                                                                   path_cost,
                                                                   time.time() - now,
                                                                    total_nodes_generated))
    w += 1
