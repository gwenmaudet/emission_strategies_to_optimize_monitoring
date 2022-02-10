import matplotlib.pyplot as plt
import latex
import math

"""plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica"
})"""
# plt.rcParams['text.usetex'] = True


import matplotlib.cm as cm
import json
import numpy as np
import statistics
import logging

import conf

logging.getLogger().setLevel(logging.INFO)

"""

This file allows a visualization of the generated json file.
This file allows to fill a json file for the performance of a function for given parameters. We vary the parameters M and tau


REMINDER :
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}

"""


def f(x, a, b):
    return a * x + b

def plot_monitoring_function_of_diversity(json_name, Ms, min_tau):
    with open(json_name, 'r') as file:
        json_file = json.load(file)
    colors = cm.rainbow(np.linspace(0, 1, len(Ms)))
    i = 0
    #forms = ['o' ,'s', '+','x', '*', 'D','d','H', 'h' ,'.' ,'>' ,'<' ,'v' ,'^','|' ,'_' ]
    forms = ['o', 's', 'X',  'D', '>', '|', '_']
    for intM in Ms:
        M = str(intM)
        diversities = []
        monitoring_times = []

        for tau in json_file[M]:
            if float(tau)>= min_tau:
                diversities.append(1/json_file[M][tau][1])
                monitoring_times.append(json_file[M][tau][0])
        marker = forms.pop()
        plt.scatter(diversities, monitoring_times, color=colors[i], label="M=" + str(M), s=20, marker=marker,alpha=0.3)
        i += 1
    #plt.title("Performance of a function according to M and tau\n with some affine function plots")
    plt.xlabel("Diversity 'D'")
    plt.ylabel("Monitoring time 'L*tau'")
    #plt.ylim(ymin=-10000, ymax=2600000)
    plt.legend(loc='upper right', ncol=2)
    plt.savefig("plots/performance_and_pareto.pdf", dpi=80, figsize=(8, 6))

    plt.show()



def monitoring_and_diversity_according_to_M_for_a_fixed_taus(taus):
    with open(conf.json_dir_for_db_f_M_tau, 'r') as file:
        json_file = json.load(file)
    M_values = {}
    monitoring_values = {}
    diversity_values = {}
    nb_of_changes = {}
    for inttau in taus:
        M_values[inttau] = []
        monitoring_values[inttau] = []
        diversity_values[inttau] = []
        nb_of_changes[inttau] = []
        strtau = str(round(float(inttau), 3))
        for strM in json_file.keys():
            if strtau in json_file[strM].keys():
                M_values[inttau].append(int(strM))
                monitoring_values[inttau].append(json_file[strM][strtau][0])
                diversity_values[inttau].append(json_file[strM][strtau][1])
                nb_of_changes[inttau].append(json_file[strM][strtau][2])
    linestyles = ['-', '--', ':']
    lineindex = 0
    for inttau in taus:

        logging.info("The max monitoring values for tau=" + str(inttau) + " is " + str(max(monitoring_values[inttau]))
                     + " and the min is " + str(min(monitoring_values[inttau]))
                     + " for a realative difference of " + str(
            (max(monitoring_values[inttau]) - min(monitoring_values[inttau]))
            / statistics.mean([max(monitoring_values[inttau]), min(monitoring_values[inttau])]) * 100))
        results = list(zip(M_values[inttau], monitoring_values[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [results[i][1]/inttau for i in range(len(results))],
                 label="tau=" + str(inttau), linestyle=linestyles[lineindex])
        lineindex += 1
    plt.xlabel("Values of M")
    plt.ylabel("Sample span 'L'")
    plt.legend()
    plt.savefig("plots/monitoring_according_to_M.pdf", dpi=80, figsize=(8, 6))
    plt.show()

    lineindex = 0
    for inttau in taus:
        results = list(zip(M_values[inttau], diversity_values[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [1/results[i][1] for i in range(len(results))],
                 label="tau=" + str(inttau), linestyle=linestyles[lineindex])
        lineindex += 1
    plt.xlabel("Values of M")
    plt.ylabel("Diversity 'D'")
    plt.legend()
    plt.savefig("plots/diversity_according_to_M.pdf", dpi=80, figsize=(8, 6))
    plt.show()

    lineindex = 0
    for inttau in taus:
        results = list(zip(M_values[inttau], nb_of_changes[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [results[i][1] for i in range(len(results))],
                 label="tau=" + str(inttau), linestyle=linestyles[lineindex])
        lineindex += 1
    plt.xlabel("Values of M")
    plt.ylabel("Number of emissions in downlink")
    plt.legend()
    plt.savefig("plots/downlink_according_to_M.pdf", dpi=80, figsize=(8, 6))
    plt.show()


if __name__ == '__main__':
    #Ms = [1,2,  3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 125, 150, 200]
    Ms = [5,10,30,50,100,150,200]
    Ms.reverse()
    min_tau = 0.5
    #taus = [0.8, 1.4, 2.2, 3.2, 4.4, 5.8, 7.4]
    taus = [0.8, 3.2, 7.4]
    cst = 3000000
    monitoring_and_diversity_according_to_M_for_a_fixed_taus(taus)
    plot_monitoring_function_of_diversity(conf.json_dir_for_db_f_M_tau, Ms, min_tau)

