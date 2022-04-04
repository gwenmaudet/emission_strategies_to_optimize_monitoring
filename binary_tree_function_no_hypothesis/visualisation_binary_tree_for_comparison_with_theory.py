import json
import statistics
import logging
import math

import conf

logging.getLogger().setLevel(logging.INFO)


def computes_pis(taus):
    pis = {}
    for tau in taus:
        pis[tau] = []
        pi = 0
        pdt = 1
        pdts = []
        nb_max_of_sensors = 300
        for i in range(1, nb_max_of_sensors):
            pdt = pdt * (conf.lambda_ / (i * conf.mu + conf.gamma / float(tau)))
            pdts.append(pdt)
            pi += pdt
        pi = 1 / (1 + pi)
        pis[tau] = [pi]
        for i in range(1, nb_max_of_sensors):
            pis[tau].append(pi * pdts[i - 1])
    return pis

def write_latex_nb_of_sensors(pis):
    open("latex_files_for_comparison_with_theory/binary_nb_of_sensors.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    # theoritical results
    theoritical_result = []
    for tau in taus:
        average_num = 0
        i =0
        for pi in pis[tau]:
            average_num += pi * i
            i += 1
        theoritical_result.append(average_num)
    with open('latex_files_for_comparison_with_theory/binary_nb_of_sensors.tex', 'a') as fout:
        fout.write("\\addplot[] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]) + ')')
        fout.write("};\n")
    # exponential results
    with open('latex_files_for_comparison_with_theory/binary_nb_of_sensors.tex', 'a') as fout:
        fout.write("\\addplot+[blue,mark=*, only marks,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_theory/binary_nb_of_sensors.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') ')
    with open('latex_files_for_comparison_with_theory/binary_nb_of_sensors.tex', 'a') as fout:
        fout.write("};")


def write_latex_nb_of_emissions():
    open("latex_files_for_comparison_with_theory/binary_nb_of_emissions.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_emissions, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files_for_comparison_with_theory/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("\\addplot+[blue,mark=*, only marks,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_theory/binary_nb_of_emissions.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ')')
    with open('latex_files_for_comparison_with_theory/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("};")


def write_latex_nb_of_perturbations(pis):
    open("latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_perturbations, 'r') as file:
        json_file = json.load(file)
    with open(conf.json_dir_binary_nb_of_change_ids, 'r') as file:
        json_file2 = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    # theoritical results
    theoritical_result = []
    """for tau in taus:
        average_num_low_bound = 2*conf.lambda_
        average_num_high_bound = 2*conf.lambda_
        i = 1
        for pi in pis[tau]:
            average_num_low_bound += (i *conf.mu + conf.gamma/tau)* pi
            average_num_high_bound += 2*(i *conf.mu + conf.gamma/tau)* pi
            i += 1
        theoritical_result.append({"lower_bound":average_num_low_bound,"higher_bound":average_num_high_bound})
    total_time = conf.stopping_time - conf.beggining_time
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot[] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]["lower_bound"]) + ')')
        fout.write("};\n")
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot[] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]["higher_bound"]) + ')')
        fout.write("};\n")"""
    n_1s = [0]
    n_2s = [0]
    ks = [0]
    nb_max_of_sensors = 300
    for i in range(1, nb_max_of_sensors + 1):
        k = math.pow(2,int(math.log(i,2)))
        n_2 = 2 * k - i
        n_1 = i - n_2
        n_2s.append(n_2)
        n_1s.append(n_1)
        ks.append(k)
    for tau in taus:
        nb_of_changes = 2 * conf.lambda_
        i = 0

        for pi in pis[tau]:
            if i != 0:
                nb_of_changes += ((conf.gamma/tau * (2 * n_2s[i])/(2*n_2s[i] +n_2s[i]) + n_2s[i] * conf.mu) * 2 + (conf.gamma/tau *(n_1s[i])/(2*n_2s[i] +n_1s[i]) + n_1s[i] * conf.mu)) * pi
            i += 1
        theoritical_result.append(nb_of_changes)
    total_time = conf.stopping_time - conf.beggining_time
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot[] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]) + ')')
        fout.write("};\n")

    #experiment results
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot+[blue,mark=*, only marks,] plot coordinates{")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean/total_time) + ')')
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("};\n")

    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot+[blue,mark=*, only marks,] plot coordinates{")
    for tau in taus:
        strtau = str(tau)
        mean = json_file2[strtau]
        with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean/total_time) + ')')
    with open('latex_files_for_comparison_with_theory/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("};")


def write_latex_diversity_and_std(pis):
    open("latex_files_for_comparison_with_theory/binary_diversity_and_std.tex", "w").close()

    with open(conf.json_dir_binary_diversity_and_std, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    # theoritical results
    theoritical_result = []
    n_1s = [0]
    n_2s = [0]
    ks = [0]
    nb_max_of_sensors = 300
    for i in range (1,nb_max_of_sensors+1):
        k=1
        while k<=i:
            k = k*2
        k = k/2
        ks.append(k)
        n_2 = 2*k - i
        n_1 = i - n_2
        n_2s.append(n_2)
        n_1s.append(n_1)
    for tau in taus:
        average_num = 0
        i = 0
        for pi in pis[tau]:
            if i!=0:
                D = conf.T * n_1s[i] * (1- math.exp((-2*ks[i] * tau)/conf.T))/(2*ks[i]*tau) + conf.T * n_2s[i] * (1- math.exp((-ks[i] * tau)/conf.T))/(ks[i]*tau)
                average_num += pi * D
            i += 1
        theoritical_result.append(average_num)
    with open('latex_files_for_comparison_with_theory/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("\\addplot[] plot coordinates {")
        for i in range(len(theoritical_result)):
            fout.write("(" + str(taus[i]) + "," + str(theoritical_result[i]) + ')')
        fout.write("};\n")

    # exponential results
    with open('latex_files_for_comparison_with_theory/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("\\addplot+[blue,mark=* ,only marks,] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]["average"]
        std = json_file[strtau]["std"]
        with open('latex_files_for_comparison_with_theory/binary_diversity_and_std.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ')')
    with open('latex_files_for_comparison_with_theory/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("};")


if __name__ == '__main__':
    with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    pis= computes_pis(taus)
    #print(pis)
    write_latex_nb_of_sensors(pis)
    write_latex_nb_of_emissions()
    write_latex_nb_of_perturbations(pis)
    write_latex_diversity_and_std(pis)
