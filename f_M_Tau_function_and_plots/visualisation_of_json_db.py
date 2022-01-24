import matplotlib.pyplot as plt
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
def f(x,a,b):
    return a*x +b


def plot_monitoring_function_of_diversity(json_name, Ms, cst):
    total_diversities = []
    monitoring_times = []
    with open(json_name, 'r') as file:
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
    plt.title("performance of a function according to M and tau")
    plt.xlabel("Diversity penalty 'Q'")
    plt.ylabel("Monitoring time 'L*tau'")
    x = np.linspace(0.02, 1.2, 100)
    plt.plot(x, f(x,cst, 0), label="affine function with b=0")
    plt.plot(x, f(x,cst,-100000), label="affine function with b=-1e^5")
    plt.plot(x, f(x,cst,100000), label="affine function with b=1e^5")

    plt.legend()
    #plt.yscale('log')
    plt.xscale('log')
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
        strtau = str(round(float(inttau),3))
        for strM in json_file.keys():
            if strtau in json_file[strM].keys():
                M_values[inttau].append(int(strM))
                monitoring_values[inttau].append(json_file[strM][strtau][0])
                diversity_values[inttau].append(json_file[strM][strtau][1])
                nb_of_changes[inttau].append(json_file[strM][strtau][2])
    for inttau in taus:
        logging.info("The max monitoring values for tau=" + str(inttau) + " is "+ str(max(monitoring_values[inttau]))
              + " and the min is " + str(min(monitoring_values[inttau]))
              +" for a realative difference of " + str((max(monitoring_values[inttau]) -  min(monitoring_values[inttau]))
                                      /statistics.mean([max(monitoring_values[inttau]), min(monitoring_values[inttau])])*100))
        results = list(zip(M_values[inttau], monitoring_values[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [results[i][1] for i in range(len(results))],label="monitoring time curve for parameter tau="+ str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding monitoring time 'L*tau'")
    plt.title("monitoring time according to the choice of M for different values of tau")
    #plt.yscale('log')
    plt.legend()
    plt.show()
    for inttau in taus:
        results = list(zip(M_values[inttau], diversity_values[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [results[i][1] for i in range(len(results))], label=" diverity penalty curve for parameter tau=" + str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding diversity penalty 'Q'")
    plt.title("diversity penalty according to the choice of M for different values of tau")
    plt.xscale('log')
    plt.legend()
    plt.show()

    for inttau in taus:
        results = list(zip(M_values[inttau], nb_of_changes[inttau]))
        results.sort()
        plt.plot([results[i][0] for i in range(len(results))], [results[i][1] for i in range(len(results))], label=" nb of usage of downlink transmission for parameter tau=" + str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding nb of emissions in downlink")
    plt.title("nb of emissions in downlink according to the choice of M for different values of tau")
    plt.yscale('log')
    plt.legend()
    plt.show()



def weighted_sum_according_to_tau_for_different_values_of_M(Ms, cst):
    with open(conf.json_dir_for_db_f_M_tau, 'r') as file:
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
            maxi = max(sums)
            tau_max = taus[sums.index(maxi)]
            logging.info("for M=" + str(M) + " the max of the weighted sum is obtained for tau="+str(tau_max)
                         + " with total monitoring equal to " + str(json_file[str(M)][str(tau_max)][0])
                         + " and diversity penalty equal to " + str(json_file[str(M)][str(tau_max)][1])
                         + " with a total sum of " + str(maxi))
            plt.scatter(taus,sums, label="M = " + str(M), color=colors[j],s=2)
            j += 1
    plt.xlabel("Values of tau")
    plt.ylabel("Weigthed sum 'S'")
    plt.title("Representation of the objectif weigthed sum according to tau, for différent values of M")
    plt.xlim(0.5,12)
    plt.legend()
    plt.show()



if __name__ == '__main__':
    Ms = [1,3,5,10,15,20,30,40,50,75,100,125,150,200]
    #taus = [0.2, 0.4, 0.8, 1.4, 2.2, 3.2]
    taus = [0.8,1.4,2.2,3.2,4.4,5.8,7.4]
    cst = 1000000
    monitoring_and_diversity_according_to_M_for_a_fixed_taus(taus)
    plot_monitoring_function_of_diversity(conf.json_dir_for_db_f_M_tau, Ms, cst)

    weighted_sum_according_to_tau_for_different_values_of_M(Ms, cst)