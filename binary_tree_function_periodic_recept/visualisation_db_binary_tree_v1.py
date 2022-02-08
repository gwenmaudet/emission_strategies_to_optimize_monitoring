import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import numpy as np
import statistics
import logging
import os

import conf

logging.getLogger().setLevel(logging.INFO)

"""

This file allows a visualization of the generated json file.
This file allows to fill a json file for the performance of a function for given parameters. We vary the parameters M and tau


REMINDER :
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}

"""
def f(x,a,b):
    return a*x +b


def plot_monitoring_function_of_diversity( Ms, cst):
    f_M_tau_db_name = conf.json_dir_for_db_f_M_tau
    with open(f_M_tau_db_name, 'r') as file:
        json_file = json.load(file)
    colors = cm.rainbow(np.linspace(0, 1, len(Ms)))
    i = 0
    for intM in Ms:
            M = str(intM)
            diversities = []
            monitoring_times = []

            for tau in json_file[M]:
                diversities.append(json_file[M][tau][1])
                monitoring_times.append(json_file[M][tau][0])
            plt.scatter(diversities, monitoring_times, color=colors[i], label="M="+str(M),s=0.5)
            i += 1
    binary_tree_function_db_name = conf.json_dir_for_db_binary_tree_function_v1
    with open(binary_tree_function_db_name, 'r') as file:
        json_file = json.load(file)
    diversities = []
    monitoring_times = []
    for tau in json_file:
        diversities.append(json_file[tau][1])
        monitoring_times.append(json_file[tau][0])
    plt.scatter(diversities, monitoring_times, color='black', edgecolor='black', label="binary tree function", s=5)
    plt.title("performance of a function according to M and tau")
    plt.xlabel("Diversity penalty 'Q'")
    plt.ylabel("Monitoring time 'L*tau'")
    x = np.linspace(0.02, 1.2, 100)
    #plt.plot(x, f(x,cst, 0), label="affine function with b=0")
    #plt.plot(x, f(x,cst,-100000), label="affine function with b=-1e^5")
    #plt.plot(x, f(x,cst,100000), label="affine function with b=1e^5")

    plt.legend()
    #plt.yscale('log')
    plt.xscale('log')
    plt.savefig("plots/comparison_V1_f_M_tau.pdf", dpi=80, figsize=(8, 6))
    plt.show()



if __name__ == '__main__':
    Ms = [1,3,5,10,15,20,30,40,50,75,100,125,150,200]
    #taus = [0.2, 0.4, 0.8, 1.4, 2.2, 3.2]
    taus = [0.8,1.4,2.2,3.2,4.4,5.8,7.4]
    cst = 1000000
    plot_monitoring_function_of_diversity(Ms, cst)