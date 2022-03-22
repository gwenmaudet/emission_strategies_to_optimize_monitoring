import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import numpy as np
import statistics
import logging
import os
import math

import conf

logging.getLogger().setLevel(logging.INFO)

"""

This file allows a visualization of the generated json file.
This file allows to fill a json file for the performance of a function for given parameters. We vary the parameters M and tau


REMINDER :
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}

"""

def write_latex_nb_of_sensors():
    open("latex_files/binary_nb_of_sensors.tex", "w").close()

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
            pdt = pdt * (conf.lambda_activation/(i*conf.lambda_shut_down + conf.lambda_battery/float(tau)))
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
        list = json_file[strtau]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(confidence_interval) + ')')
    with open('latex_files/sensor_variation_proba.tex', 'a') as fout:
        fout.write("};")


def write_latex_nb_of_emissions():
    open("latex_files/binary_nb_of_emissions.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_emissions, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        list = json_file[strtau]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/binary_nb_of_emissions.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(confidence_interval) + ')')
    with open('latex_files/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("};")

def write_latex_nb_of_perturbations():
    open("latex_files/binary_nb_of_perturbations.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_perturbations, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        list = json_file[strtau]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/binary_nb_of_perturbations.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(confidence_interval) + ')')
    with open('latex_files/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("};")


def write_latex_diversity_and_std():
    open("latex_files/binary_diversity_and_std.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_perturbations, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        list = json_file[strtau]
        stdev = statistics.stdev(list)
        confidence_interval = stdev * 2.262 / math.sqrt(len(list))
        mean = statistics.mean(list)
        with open('latex_files/binary_diversity_and_std.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(confidence_interval) + ')')
    with open('latex_files/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("};")



if __name__ == '__main__':
    write_latex_nb_of_sensors()