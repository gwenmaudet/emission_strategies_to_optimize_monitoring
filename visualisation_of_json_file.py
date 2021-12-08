import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import numpy as np


import conf

"""

This file allows a visualization of the generated json file.
This file allows to fill a json file for the performance of a function for given parameters. We vary the parameters M and tau

"""



def plot_monitoring_function_of_diversity():
    diversities = []
    monitoring_times = []
    with open(conf.json_dir_for_db, 'r') as file:
        json_file = json.load(file)
        colors = cm.rainbow(np.linspace(0, 1, 12))
        i = 0
        for M in json_file:
            if int(M) < 100:
                diversities = []
                monitoring_times = []

                for tau in json_file[M]:
                    diversities.append(json_file[M][tau][1])
                    monitoring_times.append(json_file[M][tau][0])
                plt.scatter(diversities, monitoring_times, color=colors[i], label="M="+str(M))
                i += 1
    plt.title("performance of a function according to M ad tau")
    plt.xlabel("Diversity 'Q'")
    plt.ylabel("Time of monitoring 'D * tau'")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    plot_monitoring_function_of_diversity()