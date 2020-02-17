import time
import aStar
from aStar import Node
import os

lines_for_csv="domain, run_id, start position," \
              " end position, weight, solution size, number of generated nodes," \
              "number of expanded nodes  \n "
sample_maze = [
        [0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]

def run_weighted_AStar(domain, map, start, end, weight, data):
    sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, weight)
    data[weight] = {}
    data[weight]["path_len"] = len(sol_path)
    data[weight]["num_of_gen_nodes"] = num_of_gen_nodes
    data[weight]["num_of_expan_nodes"] = num_of_expan_nodes
    data[weight]["domain"] = domain
    return

def run_pure_huristic(domain, map, start, end):
    sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, 1, True)
    tmp_dic = {}
    tmp_dic["path_len"] = len(sol_path)
    tmp_dic["num_of_gen_nodes"] = num_of_gen_nodes
    tmp_dic["num_of_expan_nodes"] = num_of_expan_nodes
    tmp_dic["domain"] = domain
    return tmp_dic


def iteritive_W_AStar(start,end,graph):
    data = {}
    W = 1
    prue_search = run_pure_huristic('maze', graph, start, end)
    while True:
        run_weighted_AStar('maze', graph, start, end, W, data)
        if data[W] == prue_search:
            break
        W += 1
    print("max W = " + str(W))
    print(data)
    return data


def run_on_map(map_file):

    graph = aStar.make_maze_from_file(map_file)
    map_results = {}
    ############ temp #############
    # graph = sample_maze
    start = Node(None, position=(0, 0))
    end = Node(None, position=(4, 2))
    #############################
    # start, end = get_random_points(graph)
    map_results[start,end] = iteritive_W_AStar(start,end,graph)
    print(map_results)

def get_random_points(graph):
    pass

def run_all_maps(directory):
    data = {}
    for map in os.listdir(directory):
        print(map)
        map_file = open(directory+"/"+map, "r")
        data[map] = run_on_map(map_file)

    print(data)


map_directory = "/Users/yanivleedon/Desktop/university/adir/WeightedAStar/maps"
run_all_maps(map_directory)