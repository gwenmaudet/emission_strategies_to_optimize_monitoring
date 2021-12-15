import json
import math
import logging

logging.getLogger().setLevel(logging.INFO)

import M_cycling_function
import conf
import simulation_of_transmissions
import diversity

"""
This file allows to fill a json file for the performance of a function for given parameters. 
We vary the parameters M and tau.

the format of the json stored will be for a given number of element, activating at the same time, with same energy parameters
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}
"""


def initialisation_of_json_file(json_name):
    json_initialised = {}
    with open(json_name, 'w+') as file:
        json.dump(json_initialised, file)


def store_one_new_value_in_json_db(monitoring_time, diversity, M, tau, json_name):
    with open(json_name, 'r') as file:
        json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
    strM = str(round(M, 3))
    strtau = str(round(tau, 3))
    if strM not in json_file:
        json_file[strM] = {}
    json_file[strM][strtau] = [monitoring_time, diversity]
    with open(json_name, 'w+') as file:
        json.dump(json_file, file)


def add_values_in_json_db(M_list, tau_list, json_name):
    with open(json_name, 'r') as file:
        json_file = json.load(file)
    for M in M_list:
        for tau in tau_list:

            if str(M) in json_file.keys() and str(round(tau, 3)) in json_file[str(M)].keys():
                a = 0
            else:
                logging.info(
                    "filling the data base '" + json_name + "' with parameters M=" + str(M) + " and tau=" + str(
                        round(tau, 3)))
                sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
                monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
                    M_cycling_function.cycling_over_M, tau, M, event, sensor_names)
                if monitoring_info is not False:
                    simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
                    Q = diversity.compute_diversity_penalty(emission_time_per_sensor, t_0, simul_time, tau, conf.T)
                    store_one_new_value_in_json_db(simul_time - t_0, Q, M, tau, json_name)


def fill_data_in_json_db(json_name):
    # M_list = [i for i in range(1, conf.n, 10)]
    M_list = [1, 2, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 125, 150, 200]
    # M_list = [15, 20, 30, 40, 50, 75, 100, 125, 150, 200]
    tau_list = [0.1 + 0.1 * i for i in range(120)]
    add_values_in_json_db(M_list, tau_list, json_name)


if __name__ == '__main__':
    json_to_fill = conf.json_dir_for_db

    #initialisation_of_json_file(json_to_fill)
    fill_data_in_json_db(json_to_fill)
    with open(json_to_fill, 'r') as file:
        json_file = json.load(file)
        logging.info("All the values of M in the DB are :")
        for M in json_file.keys():
            logging.info("M=" + str(M) + " with values of tau =" + str(json_file[M].keys()))
