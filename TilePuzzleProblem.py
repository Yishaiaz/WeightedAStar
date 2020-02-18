import numpy as np
from random import randint, shuffle
import math
from functools import reduce
from aStar import Node, aStar

MOVES = ["UP", "RIGHT", "DOWN", "LEFT"]


class TrayTilePuzzle:

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
            self.shuffle_tiles()
            # np.random.shuffle(shuffled)
            # self.tiles = shuffled
        else:
            self.tiles = tiles

    def shuffle_tiles(self):
        number_of_moves = 100000
        random_moves = np.random.randint(0, 3, number_of_moves)
        last_move = None
        for move in random_moves:
            if last_move is not None and 2-last_move == move:
                continue
            move_sign = MOVES[move]
            tiles_after_move = move_tile(self.tiles, move_sign)
            if tiles_after_move is None:
                continue
            else:
                self.tiles = tiles_after_move
                last_move = move

    def __hash__(self):
        return hash(self.tiles.tostring())

    def __repr__(self):
        return "\n".join(["|{0}|".format(",".join(["{0},".format(word)for word in line])) for line in self.tiles])

    def __eq__(self, other):
        if type(other) == type(self):
            return np.array_equal(self.tiles, other.tiles)
        return False


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
        if blank_tile_y + 1 < len(tiles):
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x][blank_tile_y + 1]
            tiles[blank_tile_x][blank_tile_y + 1] = -1
            return tiles
    elif move == "DOWN":
        if blank_tile_x + 1 < len(tiles[0]):
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x + 1][blank_tile_y]
            tiles[blank_tile_x + 1][blank_tile_y] = -1
            return tiles
    elif move == "LEFT":
        if blank_tile_y - 1 >= 0:
            tiles[blank_tile_x][blank_tile_y] = tiles[blank_tile_x][blank_tile_y - 1]
            tiles[blank_tile_x][blank_tile_y - 1] = -1
            return tiles
    return None


def get_goal_tray(tray: TrayTilePuzzle):
    x = 0
    tiles_per_row = len(tray.tiles)
    tiles = np.zeros((tiles_per_row, tiles_per_row))
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
    path = []
    while(current_node!=None):
        path.append(current_node)
        current_node = current_node.parent
    path_cost = len(path)
    return path[::-1], path_cost, total_nodes_expanded, total_nodes_generated


class TilePuzzleNode(Node):
    def __init__(self, parent=None, position: TrayTilePuzzle =None):
        super(TilePuzzleNode, self).__init__(parent=parent, position=position)

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __hash__(self):
        return hash((self.position))

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
                    at_goal_location = np.where(goal_tiles==current_tiles[x][y])
                    at_goal_location_x = at_goal_location[0][0]
                    at_goal_location_y = at_goal_location[1][0]
                    x_dis = (at_goal_location_x - x)**2
                    y_dis = (at_goal_location_y - y)**2
                    dis = math.sqrt(x_dis+y_dis)
                    h+=dis
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
            if self.h != 0:
                child.h = weight * get_h(tray=tile_puzzle_for_child, end_node_=end_node, parent_h=self.h)
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


starting_tray = TrayTilePuzzle(None, 100)
starting_node = TilePuzzleNode(parent=None, position=starting_tray)
end_tray = get_goal_tray(starting_tray)
goal_node = TilePuzzleNode(parent=None, position=end_tray)
print(starting_node)
print("\n")
# starting_node.get_children(starting_tray, end_node, 1)
print(goal_node)
path, path_cost, total_nodes_expanded, total_nodes_generated = aStar(maze=starting_tray, start=starting_node, end=goal_node, weight=3, pure=False, sol_path_func=solution_path)
print(total_nodes_expanded)