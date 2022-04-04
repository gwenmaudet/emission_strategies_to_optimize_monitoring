import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import numpy as np
import statistics
import math
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


def write_latex_sensor_variation_proba():
    open("latex_files/sensor_variation_proba.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)

    #theoritical results
    theoritical_result = []
    nb_max_of_iteration = 300
    for tau in taus:
        pi = 0
        pdt = 1
        pdts = []
        for i in range(1, nb_max_of_iteration):
            pdt = pdt * (conf.lambda_ / (i * conf.mu + conf.gamma / float(tau)))
            pdts.append(pdt)
            pi += pdt
        pi = 1/(1 + pi)
        average_num = 0
        for i in range (1,nb_max_of_iteration):
            average_num += pi * pdts[i-1] * i
        theoritical_result.append(average_num)
    with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]) + ')')
        fout.write("};\n")

    #exponential results
    with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        list = json_file[strtau]["battery_exponential"]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(confidence_interval) + ')')
    # dicrete consumption
    with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
        fout.write("};\n\\addplot+[smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        list = json_file[strtau]["discrete_consumption"]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, ' + str(confidence_interval) + ')')
    with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
        fout.write("};")




if __name__ == '__main__':
    """Ms = [3, 5, 10, 15, 20, 30, 50, 100,150, 200]
    #taus = [0.2, 0.4, 0.8, 1.4, 2.2, 3.2]
    taus = [0.8,1.4,2.2,3.2,4.4,5.8,7.4]
    cst = 1000000
    plot_monitoring_function_of_diversity(Ms, cst)"""
    write_latex_sensor_variation_proba()