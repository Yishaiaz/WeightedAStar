import time
import aStar
from aStar import Node
import os
import random
import csv
# lines_for_csv="domain, run_id, start position," \
#               " end position, weight, solution size, number of generated nodes," \
#               "number of expanded nodes  \n "

all_data = list()

# sample_maze = [
#         [0, 1, 1, 1, 1],
#         [0, 1, 0, 0, 0],
#         [0, 0, 0, 1, 0],
#     ]

def get_random_points(graph):
    start_row = -1
    start_col = -1
    while not validPoint(start_row,start_col,graph):
        start_row = random.randint(0,len(graph))
        start_col = random.randint(0, len(graph[0]))
    end_row =-1
    end_col = -1
    while not validPoint(end_row, end_col, graph) or (start_row == end_row and start_col == end_col) or (abs(start_row - end_row) < len(graph)/3 and abs(start_col - end_col) < len(graph[0])/3) :
        end_row = random.randint(0, len(graph))
        end_col = random.randint(0, len(graph[0]))

    # note that the x,y is flipped
    print("found valid start and end points")
    return Node(None, position=(start_col, start_row)), Node(None, position=(end_col, end_row))


def validPoint(x,y,graph):
    if x < 0 or x >= len(graph) or y < 0 or y >= len(graph[0]) or graph[x][y] != 0:
        return False
    return True


def run_weighted_AStar(domain, map, start, end, weight, map_name, point_iteration,):
    try:
        sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, weight)


        listing = list()
        listing.append(domain)
        listing.append(map_name)
        listing.append(point_iteration)
        listing.append(start)
        listing.append(end)
        listing.append(weight)
        listing.append(len(sol_path))
        listing.append(num_of_gen_nodes)
        listing.append(num_of_expan_nodes)

    except:
        print("Fail!")
        return None

    # data[weight] = {}
    # data[weight]["path_len"] = len(sol_path)
    # data[weight]["start"] = start
    # data[weight]["end"] = end
    # data[weight]["num_of_gen_nodes"] = num_of_gen_nodes
    # data[weight]["num_of_expan_nodes"] = num_of_expan_nodes
    # data[weight]["domain"] = domain
    # data[weight]["map_name"] = map_name
    # data[weight]["point_iteration"] = point_iteration
    return listing



def iteritive_W_AStar(start,end,graph,point_iteration, map_name):
    for W in range(1,101):
        ans = run_weighted_AStar('maze', graph, start, end, W, map_name, point_iteration)
        if ans == None:
            all_data.append(["FAIL"])
            continue
        all_data.append(ans)
    return


def run_on_map(map_file,file_name):

    graph = aStar.make_maze_from_file(map_file)
    ############ temp #############
    # graph = sample_maze
    # start = Node(None, position=(2, 1))
    # end = Node(None, position=(3, 0))
    #############################
    for i in range(1,30):
        start, end = get_random_points(graph)
        print(str(i) + "#, map: " + file_name)
        print(start, end)
        iteritive_W_AStar(start, end, graph, i, file_name)


def run_all_maps(directory):
    for map in os.listdir(directory):
        if map == "arena2.map" or  os.path.isfile('data_'+map+'.csv'):
            continue
        reset_all_data()
        print("running map " + map)
        map_file = open(directory+"/"+map, "r")
        run_on_map(map_file, map)
        create_csv(all_data,map)


def run_single_map(file,directory):
    reset_all_data()
    map_file = open(directory + "/" + file, "r")
    run_on_map(map_file,file)
    create_csv(all_data,file)

def create_csv(data, file):

    with open('data_'+file+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for listing in data:
            writer.writerow(listing)

def reset_all_data():
    all_data.clear()
    all_data.append(
        ["domain", "map_name", "random_point_iteration", "start_position", "end_position", "wight", "solution_size",
         "num_of_gen_nodes", "num_of_expanded_nodes"])

map_directory = "/Users/yanivleedon/Desktop/university/adir/WeightedAStar/maps"
# run_all_maps(map_directory)
# run_single_map("arena.map",map_directory)
run_all_maps(map_directory)