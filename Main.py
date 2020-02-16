import time
import aStar
from aStar import Node

lines_for_csv="domain, run_id, start position," \
              " end position, weight, solution size, number of generated nodes," \
              "number of expanded nodes  \n "
sample_maze = [
        [0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]

def single_run(domain, map, start, end, weight, data):
    sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, weight)
    data[weight] = {}
    data[weight]["path_len"] = len(sol_path)
    data[weight]["num_of_gen_nodes"] = num_of_gen_nodes
    data[weight]["num_of_expan_nodes"] = num_of_expan_nodes
    data[weight]["domain"] = domain


    # csv_line="{0},{1},{2},{3},{4},{5},{6},{7}\n".format(domain,
    #                                           run_id,
    #                                           start.position,
    #                                           end.position,
    #                                           weight,
    #                                           len(sol_path),
    #                                           num_of_gen_nodes,
    #                                           num_of_expan_nodes)
    # return csv_line
    return

def run_pure_huristic(domain, map, start, end, data):
    sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, 1, True)
    data["pure"] = {}
    data["pure"]["path_len"] = len(sol_path)
    data["pure"]["num_of_gen_nodes"] = num_of_gen_nodes
    data["pure"]["num_of_expan_nodes"] = num_of_expan_nodes
    data["pure"]["domain"] = domain

    return


def multiRun():
    global lines_for_csv
    run_ctr=0
    domains = dict()
    domains['mazes'] = [sample_maze]
    for k,v in enumerate(domains.keys()):
        for graph in domains[v]:
            # graph = domains[k]
            data = {}
            start = Node(None, position=(0, 0))
            end = Node(None, position=(4, 2))
            W = 1
            run_pure_huristic('maze', graph, start, end, data)
            print(data["pure"])
            while True:
                single_run('maze', graph, start, end, W, data)
                if data[W] == data["pure"]:
                    break
                W += 1
            print(data)

# file1 = open("maps/arena.map", 'r')
# maze = aStar.make_maze_from_file(file1)

# sol_path, path_cost = aStar.aStar(maze, start, end, 1)
# print(sol_path)
multiRun()
