import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def extract_and_plot_avgs_by_w(data: pd.DataFrame, plot_name_to_save: str = "test.png"):
    # get raw data by W
    by_w = dict()
    for w in data['wight'].unique():
        by_w[w] = data.loc[data['wight'] == w]

    # create the averages in a dictionary per w
    averages_by_w = dict()
    for w_in_by_w in by_w.keys():
        full_data_by_w = by_w[w_in_by_w]
        averages_by_w[w_in_by_w] = dict({
            "Avg_Expanded": np.average(full_data_by_w['num_of_expanded_nodes'].values),
            "Avg_Generated": np.average(full_data_by_w['num_of_gen_nodes'].values),
            "Avg_Solution_Size": np.average(full_data_by_w['solution_size'].values),
        })
    # create the vectors for the plot
    expanded_avg_vector = []
    generated_avg_vector = []
    sol_size_avg_vector = []
    for w in averages_by_w.keys():
        expanded_avg_vector.append(averages_by_w[w]["Avg_Expanded"])
        generated_avg_vector.append(averages_by_w[w]["Avg_Generated"])
        sol_size_avg_vector.append(averages_by_w[w]["Avg_Solution_Size"])

    expanded_avg_vector = np.array(expanded_avg_vector)
    generated_avg_vector = np.array(generated_avg_vector)
    sol_size_avg_vector = np.array(sol_size_avg_vector)
    w = np.array(list(averages_by_w.keys()))
    fig, axis = plt.subplots(3, 1)
    axis[0].plot(w, expanded_avg_vector)
    axis[1].plot(w, generated_avg_vector)
    axis[2].plot(w, sol_size_avg_vector)
    axis[0].set_title("Expanded Avg")
    axis[1].set_title("Generated Avg")
    axis[2].set_title("Solution Size Avg")
    axis[0].set_xlabel("W", fontsize=7)
    axis[1].set_xlabel("W", fontsize=7)
    axis[2].set_xlabel("W", fontsize=7)
    plt.tight_layout()
    plt.show()
    fig.savefig("{0} avgs data.png".format(plot_name_to_save), dpi=300)

def extract_w_per_domain(domain_map_list:list = []):

    mutation_number = 0
    avg_expnaded_sum = 0
    for map_data in domain_map_list:
        for random_point_iter in map_data['random_point_iteration'].unique():
            c_star = 1
            random_point_data = map_data.loc[map_data['random_point_iteration'] == random_point_iter]
            list_of_sol_per_c_start = []
            for w_idx in random_point_data['wight'].unique():
                if w_idx == 1:
                    c_star = random_point_data[random_point_data['wight'] == w_idx]["solution_size"].values[0]
                else:
                    solution_normailized = random_point_data[random_point_data['wight'] == w_idx]["solution_size"].values[0]/c_star
                    list_of_sol_per_c_start.append(solution_normailized)

            random_point_data['sol / c*'] = list_of_sol_per_c_start




# MAZE
first_data = pd.read_csv("map_data/data_brc000d.map.csv")
# extract_and_plot_avgs_by_w(first_data, "first map")
second_data = pd.read_csv("map_data/data_brc501d.map.csv")
# extract_and_plot_avgs_by_w(second_data, "second map")
third_data = pd.read_csv("map_data/data_brc505d.map.csv")
# extract_and_plot_avgs_by_w(third_data, "third map")
fourth_data = pd.read_csv("map_data/data_den011d.map.csv")
# extract_and_plot_avgs_by_w(fourth_data, "fourth map")
a = [first_data, second_data, third_data, fourth_data]
extract_w_per_domain(a)


# PANCAKE
# num = 7
# seven_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(seven_size_pancake_data, "pancake size {0} ".format(num))
# num = 8
# eight_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(eight_size_pancake_data, "pancake size {0} ".format(num))
# num = 9
# nine_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(nine_size_pancake_data, "pancake size {0} ".format(num))
# num = 10
# ten_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(ten_size_pancake_data, "pancake size {0} ".format(num))
# num = 11
# eleven_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(eleven_size_pancake_data, "pancake size {0} ".format(num))
# num = 12
# twelve_size_pancake_data = pd.read_csv("pancake_data/data_pancake_size_{0}.csv".format(num))
# extract_and_plot_avgs_by_w(twelve_size_pancake_data, "pancake size {0} ".format(num))


