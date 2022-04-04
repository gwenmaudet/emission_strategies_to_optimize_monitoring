import json
import statistics
import logging
import math

import conf

logging.getLogger().setLevel(logging.INFO)


def write_latex_nb_of_sensors():
    open("latex_files_for_comparison_with_other_function/binary_nb_of_sensors.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    #exponential results
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_sensors.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,mark options={draw=blue,fill=blue,}] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_other_function/binary_nb_of_sensors.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') ')
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_sensors.tex', 'a') as fout:
        fout.write("};")


def write_latex_nb_of_emissions():
    open("latex_files_for_comparison_with_other_function/binary_nb_of_emissions.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_emissions, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,mark options={draw=blue,fill=blue,}] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_other_function/binary_nb_of_emissions.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ')')
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_emissions.tex', 'a') as fout:
        fout.write("};")

def write_latex_nb_of_perturbations():
    open("latex_files_for_comparison_with_other_function/binary_nb_of_perturbations.tex", "w").close()

    with open(conf.json_dir_binary_nb_of_perturbations, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    total_time = conf.stopping_time - conf.beggining_time
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("\\addplot+[smooth,mark=*, only marks,mark options={draw=blue,fill=blue,}] plot coordinates{")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]
        with open('latex_files_for_comparison_with_other_function/binary_nb_of_perturbations.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean/total_time) + ')')
    with open('latex_files_for_comparison_with_other_function/binary_nb_of_perturbations.tex', 'a') as fout:
        fout.write("};")


def write_latex_diversity_and_std():
    open("latex_files_for_comparison_with_other_function/binary_diversity_and_std.tex", "w").close()

    with open(conf.json_dir_binary_diversity_and_std, 'r') as file:
        json_file = json.load(file)
    taus = [float(elt) for elt in json_file.keys()]
    taus = sorted(taus)
    with open('latex_files_for_comparison_with_other_function/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("\\addplot+[blue,smooth,mark=*, only marks,error bars/.cd, y dir=both, y explicit] plot coordinates {")
    for tau in taus:
        strtau = str(tau)
        mean = json_file[strtau]["average"]
        std = json_file[strtau]["std"]
        with open('latex_files_for_comparison_with_other_function/binary_diversity_and_std.tex', 'a') as fout:
            fout.write("(" + str(tau) + ',' + str(mean) + ') +- (0, '+ str(std) + ')')
    with open('latex_files_for_comparison_with_other_function/binary_diversity_and_std.tex', 'a') as fout:
        fout.write("};")



if __name__ == '__main__':
    write_latex_nb_of_sensors()
    write_latex_nb_of_emissions()
    write_latex_nb_of_perturbations()
    write_latex_diversity_and_std()

