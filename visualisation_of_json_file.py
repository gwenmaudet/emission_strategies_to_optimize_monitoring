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


def monitoring_and_diversity_according_to_M_for_a_fixed_taus(Ms, taus):
    with open(conf.json_dir_for_db, 'r') as file:
        json_file = json.load(file)
    M_values = {}
    monitoring_values = {}
    diversity_values = {}
    for inttau in taus:
        M_values[inttau] = []
        monitoring_values[inttau] = []
        diversity_values[inttau] = []
        strtau = str(inttau)
        for M in Ms:
            strM= str(M)
            if strM in json_file and strtau in json_file[strM].keys():
                M_values[inttau].append(int(M))
                monitoring_values[inttau].append(json_file[strM][strtau][0])
                diversity_values[inttau].append(json_file[strM][strtau][1])
    for inttau in taus:
        plt.plot(M_values[inttau],monitoring_values[inttau],label="monitoring time curve for parameter tau="+ str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding monitoring time")
    plt.title("monitoring time according to the choice of M for different values of tau")
    plt.legend()
    plt.show()
    for inttau in taus:
        plt.plot(M_values[inttau], diversity_values[inttau], label=" diverity curve for parameter tau=" + str(inttau))
    plt.xlabel("Values of M")
    plt.ylabel("corresponding diversity")
    plt.title("diversity according to the choice of M for different values of tau")
    plt.legend()
    plt.show()






if __name__ == '__main__':
    #plot_monitoring_function_of_diversity()
    Ms = [1,2,3,5,10,15,20,30,40,50,75,100,125,150,200]
    taus = [0.5,1.5,2.5,3.5,4.5]
    monitoring_and_diversity_according_to_M_for_a_fixed_taus(Ms, taus)