import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import numpy as np


import conf

"""

This file allows a visualization of the generated json file.
This file allows to fill a json file for the performance of a function for given parameters. We vary the parameters M and tau


REMINDER :
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}

"""



def plot_monitoring_function_of_diversity(json_name):
    diversities = []
    monitoring_times = []
    with open(json_name, 'r') as file:
        json_file = json.load(file)
    colors = cm.rainbow(np.linspace(0, 1, len(json_file.keys())))
    i = 0
    for M in json_file:

            diversities = []
            monitoring_times = []

            for tau in json_file[M]:
                diversities.append(json_file[M][tau][1])
                monitoring_times.append(json_file[M][tau][0])
            plt.scatter(diversities, monitoring_times, color=colors[i], label="M="+str(M),s=5)
            i += 1
    plt.title("performance of a function according to M and tau")
    plt.xlabel("Diversity penalty")
    plt.ylabel("Time of monitoring")
    plt.legend()
    #plt.yscale('log')
    #plt.xscale('log')
    plt.show()


def monitoring_and_diversity_according_to_M_for_a_fixed_taus(taus):
    with open(conf.json_dir_for_db, 'r') as file:
        json_file = json.load(file)
    print(json_file['1'].keys())
    M_values = {}
    monitoring_values = {}
    diversity_values = {}
    for inttau in taus:
        M_values[inttau] = []
        monitoring_values[inttau] = []
        diversity_values[inttau] = []
        strtau = str(round(float(inttau),3))
        for strM in json_file.keys():
            if strtau in json_file[strM].keys():
                M_values[inttau].append(int(strM))
                monitoring_values[inttau].append(json_file[strM][strtau][0])
                diversity_values[inttau].append(json_file[strM][strtau][1])
    for inttau in taus:
        plt.plot(M_values[inttau], monitoring_values[inttau],label="monitoring time curve for parameter tau="+ str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding monitoring time")
    plt.title("monitoring time according to the choice of M for different values of tau")
    plt.legend()
    plt.show()
    for inttau in taus:
        plt.plot(M_values[inttau], diversity_values[inttau], label=" diverity penalty curve for parameter tau=" + str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding diversity")
    plt.title("diversity penalty according to the choice of M for different values of tau")
    plt.legend()
    plt.show()


def weighted_sum_according_to_tau_for_different_values_of_M(Ms, cst):
    with open(conf.json_dir_for_db, 'r') as file:
        json_file = json.load(file)
    colors = cm.rainbow(np.linspace(0, 1, len(Ms)))
    j = 0
    for M in Ms:
        if str(M) in json_file.keys():
            taus = [float(elt) for elt in json_file[str(M)].keys()]
            sums = [json_file[str(M)][tau][0] - cst * json_file[str(M)][tau][1] for tau in json_file[str(M)].keys()]
            results = []
            for i in range(len(json_file[str(M)].keys())):
                results.append([taus[i],sums[i]])
            results.sort()

            taus = [results[i][0] for i in range(len(results))]
            sums = [results[i][1] for i in range(len(results))]
            plt.plot(taus,sums, label="M = " + str(M), color=colors[j])
            j += 1
    plt.xlabel("Values of tau")
    plt.ylabel("Weigthed sum of the metrics")
    plt.title("Representation of the objectif weigthed sum according to tau, for différent values of M")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    cplot_monitoring_function_of_diversity(conf.json_dir_for_db)
    Ms = [5,10,15,20,30,40,50,75,100,125,150,200]
    taus = [0.2, 0.4, 0.8, 1.4, 2.2, 3.2]
    cst = 300000
    #monitoring_and_diversity_according_to_M_for_a_fixed_taus(taus)
    #weighted_sum_according_to_tau_for_different_values_of_M(Ms, cst)