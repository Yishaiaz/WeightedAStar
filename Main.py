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

def single_run(run_id, domain, map, start, end, weight):
    (sol_path, path_cost), num_of_expan_nodes, num_of_gen_nodes = aStar.aStar(map, start, end, weight)
    csv_line="{0},{1},{2},{3},{4},{5},{6},{7}\n".format(domain,
                                              run_id,
                                              start.position,
                                              end.position,
                                              weight,
                                              len(sol_path),
                                              num_of_gen_nodes,
                                              num_of_expan_nodes)
    return csv_line


def multiRun():
    global lines_for_csv
    run_ctr=0
    domains = dict()
    domains['mazes'] = [sample_maze]
    for k in enumerate(domains.keys()):
        for graph in domains[k]:
            # graph = domains[k]
            start = Node(None, position=(0, 0))
            end = Node(None, position=(4, 2))
            lines_for_csv += single_run(run_ctr,'maze', graph, start, end, 1)
            run_ctr += 1

# file1 = open("maps/arena.map", 'r')
# maze = aStar.make_maze_from_file(file1)

# sol_path, path_cost = aStar.aStar(maze, start, end, 1)
# print(sol_path)
multiRun()
print(lines_for_csv)