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
            "avg_Solution_per_c_star": np.average(full_data_by_w['sol / c*'].values),
            "avg_expanded_per_expanded_star": np.average(full_data_by_w['expanded_star'].values)
        })
    # create the vectors for the plot
    expanded_avg_vector = []
    generated_avg_vector = []
    sol_size_avg_vector = []
    sol_size_per_c_star_avg_vector = []
    expanded_per_expanded_star_avg_vector = []
    for w in averages_by_w.keys():
        expanded_avg_vector.append(averages_by_w[w]["Avg_Expanded"])
        generated_avg_vector.append(averages_by_w[w]["Avg_Generated"])
        sol_size_avg_vector.append(averages_by_w[w]["Avg_Solution_Size"])
        sol_size_per_c_star_avg_vector.append(averages_by_w[w]["avg_Solution_per_c_star"])
        expanded_per_expanded_star_avg_vector.append(averages_by_w[w]["avg_expanded_per_expanded_star"])

    expanded_avg_vector = np.array(expanded_avg_vector)
    generated_avg_vector = np.array(generated_avg_vector)
    sol_size_avg_vector = np.array(sol_size_avg_vector)
    sol_size_per_c_star_avg_vector = np.array(sol_size_per_c_star_avg_vector)
    expanded_per_expanded_star_avg_vector = np.array(expanded_per_expanded_star_avg_vector)

    w = np.array(list(averages_by_w.keys()))
    fig, axis = plt.subplots(5, 1)
    axis[0].plot(w, expanded_avg_vector)
    axis[1].plot(w, generated_avg_vector)
    axis[2].plot(w, sol_size_avg_vector)
    axis[3].plot(w, sol_size_per_c_star_avg_vector)
    axis[4].plot(w, expanded_per_expanded_star_avg_vector)
    axis[0].set_title("Expanded Avg")
    axis[1].set_title("Generated Avg")
    axis[2].set_title("Solution Size Avg")
    axis[3].set_title("Solution Cost / C* Cost")
    axis[4].set_title("Expanded / Expanded Star")
    axis[0].set_xlabel("W", fontsize=7)
    axis[1].set_xlabel("W", fontsize=7)
    axis[2].set_xlabel("W", fontsize=7)
    axis[3].set_xlabel("W", fontsize=7)
    axis[4].set_xlabel("W", fontsize=7)
    axis[0].tick_params(axis='both', which='major', labelsize=5)
    axis[0].tick_params(axis='both', which='minor', labelsize=5)
    axis[1].tick_params(axis='both', which='major', labelsize=5)
    axis[1].tick_params(axis='both', which='minor', labelsize=5)
    axis[2].tick_params(axis='both', which='major', labelsize=5)
    axis[2].tick_params(axis='both', which='minor', labelsize=5)
    axis[3].tick_params(axis='both', which='major', labelsize=5)
    axis[3].tick_params(axis='both', which='minor', labelsize=5)
    axis[4].tick_params(axis='both', which='major', labelsize=5)
    axis[4].tick_params(axis='both', which='minor', labelsize=5)
    plt.tight_layout()
    plt.show()
    fig.savefig("{0} avgs data.png".format(plot_name_to_save), dpi=300)


def extract_w_behavior_per_domain(domain_map_list:list = [], problem_analyzed_dir: str = "Maps"):
    for map_data in domain_map_list:
        total_map_sol_per_expanded_star = []
        total_map_sol_per_c_star = []
        sol_per_c_star_data_frame_for_map = pd.DataFrame(columns=['sol / c*'], index=map_data.index)
        sol_per_expanded_star_data_frame_for_map = pd.DataFrame(columns=['expanded_star'], index=map_data.index)
        for random_point_iter in map_data['random_point_iteration'].unique():
            c_star = 1
            expanded_star = 1
            random_point_data = map_data.loc[map_data['random_point_iteration'] == random_point_iter]
            list_of_sol_per_c_star = []
            list_of_expanded_per_expanded_star = []
            for w_idx in random_point_data['wight'].unique():
                if w_idx == 1:
                    # idx = random_point_data[random_point_data['wight'] == w_idx]
                    c_star = random_point_data[random_point_data['wight'] == w_idx]["solution_size"].values[0]
                    expanded_star = random_point_data[random_point_data['wight'] == w_idx]["num_of_expanded_nodes"].values[0]
                    list_of_sol_per_c_star.append(1)
                    list_of_expanded_per_expanded_star.append(1)

                else:
                    solution_normailized = random_point_data[random_point_data['wight'] == w_idx]["solution_size"].values[0]/c_star
                    expanded_normalized = random_point_data[random_point_data['wight'] == w_idx]["num_of_expanded_nodes"].values[0]/expanded_star
                    list_of_sol_per_c_star.append(solution_normailized)
                    list_of_expanded_per_expanded_star.append(expanded_normalized)

            total_map_sol_per_expanded_star = total_map_sol_per_expanded_star + list_of_expanded_per_expanded_star
            total_map_sol_per_c_star = total_map_sol_per_c_star + list_of_sol_per_c_star

        sol_per_expanded_star_data_frame_for_map['expanded_star'] = total_map_sol_per_expanded_star
        sol_per_c_star_data_frame_for_map['sol / c*'] = total_map_sol_per_c_star
        map_data = pd.concat([map_data, sol_per_c_star_data_frame_for_map, sol_per_expanded_star_data_frame_for_map], axis=1)
        # map_data['sol / c*'] = pd.Series(total_map_sol_per_c_star)
        # map_data['expanded_star'] = pd.Series(total_map_sol_per_expanded_star)
        name_of_file = map_data['map_name'].values[0]
        if type(name_of_file) == type(tuple()):
            name_of_file = name_of_file[0]
        map_data.to_csv("Analyzed/{1}/{0}.csv".format(name_of_file, problem_analyzed_dir))
        print()





# MAZE
# first_data = pd.read_csv("Analyzed/Maps/brc000d.map.csv")
# extract_and_plot_avgs_by_w(first_data, "first map")
# second_data = pd.read_csv("Analyzed/Maps/brc501d.map.csv")
# extract_and_plot_avgs_by_w(second_data, "second map")
# third_data = pd.read_csv("Analyzed/Maps/brc505d.map.csv")
# extract_and_plot_avgs_by_w(third_data, "third map")
# fourth_data = pd.read_csv("Analyzed/Maps/den011d.map.csv")
# extract_and_plot_avgs_by_w(fourth_data, "fourth map")
# a = [first_data, second_data, third_data, fourth_data]
# extract_w_behavior_per_domain(a, 'Maps')


# PANCAKE
num = 7
seven_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(seven_size_pancake_data, "pancake size {0} ".format(num))
num = 8
eight_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(eight_size_pancake_data, "pancake size {0} ".format(num))
num = 9
nine_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(nine_size_pancake_data, "pancake size {0} ".format(num))
num = 10
ten_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(ten_size_pancake_data, "pancake size {0} ".format(num))
num = 11
eleven_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(eleven_size_pancake_data, "pancake size {0} ".format(num))
num = 12
twelve_size_pancake_data = pd.read_csv("Analyzed/pancake_problem/{0}.csv".format(num))
extract_and_plot_avgs_by_w(twelve_size_pancake_data, "pancake size {0} ".format(num))
# a = [seven_size_pancake_data, eight_size_pancake_data, nine_size_pancake_data, ten_size_pancake_data, eleven_size_pancake_data, twelve_size_pancake_data]
# extract_w_behavior_per_domain(a, 'pancake_problem')


