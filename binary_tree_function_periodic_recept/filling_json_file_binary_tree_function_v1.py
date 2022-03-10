import json
import logging
import math
import random

logging.getLogger().setLevel(logging.INFO)

import binary_tree_v1
import conf
from simulation import simulation_of_transmissions, diversity
from f_M_Tau_function_and_plots import f_M_tau
"""
This file allows to fill a json file for the performance of a function for given parameters. 
We vary the parameters M and tau.

the format of the json stored will be for a given number of element, activating at the same time, with same energy parameters
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, nb_of_modification_of_period], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}
"""


def initialisation_of_json_file(json_name):
    json_initialised = {}
    with open(json_name, 'w+') as file:
        json.dump(json_initialised, file)


def store_one_new_value_in_json_db(monitoring_time, diversity, nb_of_changes, tau, json_name):
    with open(json_name, 'r') as file:
        json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
    strtau = str(round(tau, 3))
    if strtau not in json_file.keys():
        json_file[strtau] = {"monitoring_time":[],"diversity":[], "nb_of_changes":[]}
    json_file[strtau]["monitoring_time"].append(monitoring_time)
    json_file[strtau]["diversity"].append(diversity)
    json_file[strtau]["nb_of_changes"].append(nb_of_changes)
    with open(json_name, 'w+') as file:
        json.dump(json_file, file)

def fill_data_in_json_db(json_to_fill_binary, json_file_f_M_tau, tau_list,nb_of_iterations):
    """with open(json_to_fill_binary, 'r') as file:
        binray_file = json.load(file)
    with open(json_file_f_M_tau, 'r') as file:
        f_m_tau_file = json.load(file)"""
    for tau in tau_list:
        for i in range(nb_of_iterations):

            t_i = []
            t_s = []
            t = 0
            for i in range(conf.n):
                p = random.uniform(0, 1)
                t -= math.log(p) / conf.lambda_activation
                t_i.append(t)
                p = random.uniform(0, 1)
                new_time = t - math.log(p) / conf.lambda_shut_down
                t_s.append(new_time)
            # binary
            logging.info(
                    "filling the data base '" + json_to_fill_binary + "' with parameters  tau=" + str(
                        round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C, battery_type=2,
                                                                                 shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v1.binary_tree, tau, event, sensor_names, known_battery=False)
            Q = diversity.compute_average_diversity(emission_time_per_sensor, t_0, simul_time, conf.T)
            store_one_new_value_in_json_db(simul_time - t_0, Q, nb_of_changes, tau, json_to_fill_binary)
            #f_m_tau

            logging.info(
                "filling the data base '" + json_file_f_M_tau + "' with parameters  tau=" + str(
                    round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C,
                                                                                        battery_type=2,
                                                                                        shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                f_M_tau.cycling_over_M, tau, event, sensor_names,M=None, known_battery=False)
            Q = diversity.compute_average_diversity(emission_time_per_sensor, t_0, simul_time, conf.T)
            store_one_new_value_in_json_db(simul_time - t_0, Q, nb_of_changes, tau, json_file_f_M_tau)



if __name__ == '__main__':
    json_to_fill_binary = conf.json_dir_for_db_binary_tree_function_v1
    json_file_f_M_tau = conf.json_dir_f_M_tau_for_comparison
    initialisation_of_json_file(json_file_f_M_tau)
    initialisation_of_json_file(json_to_fill_binary)
    tau_list = [0.1 + 0.1 * i for i in range(10)]
    tau_list = [1]
    nb_of_iterations = 10
    #tau_list = [0.1 + 0.2 * i for i in range(50)]
    #tau_list = [0.8, 1.4, 2.2, 3.2, 4.4, 5.8, 7.4]
    #M_list = [i for i in range(1, 200, 2)]
    fill_data_in_json_db(json_to_fill_binary, json_file_f_M_tau, tau_list,nb_of_iterations)
    """with open(json_to_fill, 'r') as file:
        json_file = json.load(file)
        logging.info("All the values of tau in the DB are :" + str(json_file.keys()))"""
