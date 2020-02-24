import time
import aStar
from aStar import Node
import os
import random
import csv
from tkinter import *
import GUI
from PancakeProblem import Tray, get_goal_tray, PancakeNode, solution_path
import TilePuzzleProblem as tp
import numpy as np
import TopSpinProblem as top
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


def run_weighted_AStar(domain, map, start, end, weight, map_name, point_iteration, pure=False, sol_func= aStar.solution_path):
    try:
        sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, weight,pure=pure, sol_path_func=sol_func)


        listing = list()
        listing.append(domain)
        listing.append(map_name)
        listing.append(point_iteration)
        listing.append(start)
        listing.append(end)
        listing.append(weight)
        listing.append(path_cost)
        listing.append(num_of_gen_nodes)
        listing.append(num_of_expan_nodes)

    except:
        print("Fail!")
        return None

    return listing



def iteritive_W_AStar(domain, start,end,graph,point_iteration, map_name,solution_path=aStar.solution_path):
    # pure_huristic = run_weighted_AStar(domain, graph, start, end, 1, map_name, point_iteration, True, sol_func=solution_path)
    # print("map: " + str(map_name) + ", mutation num: " + str(point_iteration))
    pure_huristic = run_weighted_AStar(domain, graph, start, end, 100, map_name, point_iteration, False, sol_func=solution_path)

    if not pure_huristic:
        print("no solution")
        return

    print("pure huristic length = " + str(pure_huristic[len(pure_huristic)-3]) +", expanded: " + str(pure_huristic[len(pure_huristic) - 1]) )
    for W in np.arange(1,2.01,0.05):
    # for W in range(1,21):
        ans = run_weighted_AStar(domain, graph, start, end, W, map_name, point_iteration, sol_func=solution_path)
        if ans == None:
            return
        print("W: " + str(W) + ", solution length: " + str(ans[len(ans) - 3]) +", expanded: " + str(ans[len(ans) - 1]))


        all_data.append(ans)

        # if isSameResult(ans,pure_huristic):
        #     return;
    return

def isSameResult(first,second):
    if first[len(first)-1] == second[len(second)-1] and first[len(first)-3] == second[len(second)-3]:
        return True
    # print(str(first[len(first)-1]) + " != " + str(second[len(second)-1]) + ", or " + str(first[len(first)-3]) + " != " + str(second[len(second)-3] ))
    return False

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
        iteritive_W_AStar("maze",start, end, graph, i, file_name)


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
    print("created file CSV file")

def reset_all_data():
    all_data.clear()
    all_data.append(
        ["domain", "map_name", "random_point_iteration", "start_position", "end_position", "wight", "solution_size",
         "num_of_gen_nodes", "num_of_expanded_nodes"])
def test_gui(file_name,directory):
    reset_all_data()
    map_file = open(directory + "/" + file_name, "r")
    graph = aStar.make_maze_from_file(map_file)
    start = Node(None, position=(177, 42))
    end = Node(None, position=(64, 98))

    # row = 42, col = 177
    # ","
    # row = 98, col = 64
    # "
    # start, end = get_random_points(graph)

    print(graph[start.position[1]][start.position[0]])
    print(graph[end.position[1]][end.position[0]])
    W = 1
    print("running ASTAR")
    sol_path, path_cost, num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(graph, start, end, W)
    print("solution length: " + str(path_cost))
    paintPath(start,end,graph,sol_path)

    root = Tk()
    my_gui = GUI.CellGrid(root, len(graph), len(graph[0]), 7, graph)
    root.mainloop()

def paintPath(start,end,graph,sol_path):
    graph[start.position[1]][start.position[0]] = 2
    graph[end.position[1]][end.position[0]] = 3
    for node in sol_path:
        graph[node[1]][node[0]] = 6

def run_all_pancakes():

    for pancake_map in range(10,15):
        reset_all_data()
        if os.path.isfile('data_'+"pancake_size_"+str(pancake_map)+'.csv'):
            continue


        for mutation in range(1, 31):
            print("RUNNING: map: {}, mutation: {}".format(pancake_map, mutation))
            starting_tray = Tray(None, pancake_map)
            goal_tray = get_goal_tray(starting_tray)
            starting_node = PancakeNode(parent=None, position=starting_tray)
            goal_node = PancakeNode(parent=None, position=goal_tray)

            iteritive_W_AStar("Pancake",starting_node, goal_node, starting_tray, mutation, pancake_map, solution_path)
        create_csv(all_data, "pancake_size_"+str(pancake_map))

        # print("path cost: {0}, total expanded: {1}, total generated: {2}".format(path_cost, total_nodes_expanded, total_nodes_generated))

def turn_to_str(tray: tp.TrayTilePuzzle):
    np_array = np.copy(tray.tiles)
    convert_to_str = lambda x: str(int(x+1)) if x>=0 else '_'
    rows = []
    for row in np_array:
        col = []
        for val in row:
            str_rep = convert_to_str(val)
            col.append(str_rep)
        rows.append(col)
    return rows

def run_all_TilePuzzles():

    for tile_map in [49]:
        reset_all_data()
        # if os.path.isfile('data_'+"tilePuzzle_size_"+str(tile_map)+'.csv'):
        #     continue


        for mutation in range(3,10):
            starting_tray = tp.TrayTilePuzzle(None, tile_map)
            end_tray = tp.get_goal_tray(starting_tray)
            starting_node = tp.TilePuzzleNode(parent=None, position=starting_tray)
            goal_node = tp.TilePuzzleNode(parent=None, position=end_tray)
            iteritive_W_AStar("tilePuzzle",starting_node, goal_node, starting_tray, mutation, tile_map, solution_path=tp.solution_path)
        # create_csv(all_data, "tilePuzzle_size_"+str(tile_map))

def run_all_topspin():
    # k_param = 3
    for k_param in range(3,5):
        for tile_map in [9]:
            reset_all_data()
            # if os.path.isfile('data_'+"tilePuzzle_size_"+str(tile_map)+'.csv'):
            #     continue
            mutation = 1
            error=0
            while mutation < 30:
            # for mutation in range(1,31):
                try:
                    start_tray = top.TrayTopSpin(array_size=tile_map, k_param=k_param)
                    end_goal = top.TopSpinNode(position=top.TrayTopSpin(scrambled_array=np.linspace(0, tile_map - 1, tile_map), k_param=k_param))
                    start_node = top.TopSpinNode(position=start_tray)
                    print("RUNNING: map: {}, K: {}, mutation: {}".format(tile_map, k_param, mutation))
                    iteritive_W_AStar("topSpin", start_node, end_goal, start_tray, mutation, tile_map,solution_path=top.solution_path)
                    mutation += 1

                except:
                    error+=1
                    print("map: {}, K: {}, error: {}, mutation: {}".format(tile_map,k_param,error,mutation))
                    continue
            create_csv(all_data, "topSpin_K_"+str(k_param)+"_size"+str(tile_map))

map_directory = "/Users/yanivleedon/Desktop/university/adir/WeightedAStar/maps"
# run_all_maps(map_directory)
# run_single_map("den011d.map",map_directory)
# test_gui("den011d.map",map_directory)
# run_all_maps(map_directory)
run_all_pancakes()
# run_all_TilePuzzles()
# run_all_topspin()
