import json
import logging
import math


logging.getLogger().setLevel(logging.INFO)

import binary_tree_v2_without_any_conditions
import conf
from simulation import simulation_of_transmissions, diversity

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

    json_file[strtau] = [monitoring_time, diversity, nb_of_changes]
    with open(json_name, 'w+') as file:
        json.dump(json_file, file)


def add_values_in_json_db(tau_list, json_name):
    with open(json_name, 'r') as file:
        json_file = json.load(file)
    for tau in tau_list:

        if str(round(tau, 3)) in json_file.keys():
            a = 0
        else:
            logging.info(
                "filling the data base '" + json_name + "' with parameters  tau=" + str(
                    round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
            monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v2_without_any_conditions.binary_tree, tau, event, sensor_names, known_battery=False)
            if monitoring_info is not False:
                simul_time, dt, emission_time_per_sensor, changed_period, t_0,nb_of_changes = monitoring_info
                Q = diversity.compute_average_diversity(emission_time_per_sensor, t_0, simul_time, conf.T)
                store_one_new_value_in_json_db(simul_time - t_0, Q,nb_of_changes, tau, json_name)


def fill_data_in_json_db(json_name,tau_list):
    add_values_in_json_db(tau_list, json_name)


if __name__ == '__main__':
    json_to_fill = conf.json_dir_for_db_binary_tree_v2_no_hypothesis

    #initialisation_of_json_file(json_to_fill)
    tau_list = [0.1 + 0.05 * i for i in range(250)]
    #tau_list = [0.1 + 0.2 * i for i in range(50)]
    #tau_list = [0.8, 1.4, 2.2, 3.2, 4.4, 5.8, 7.4]
    #M_list = [i for i in range(1, 200, 2)]
    fill_data_in_json_db(json_to_fill, tau_list)
    with open(json_to_fill, 'r') as file:
        json_file = json.load(file)
        logging.info("All the values of tau in the DB are :" + str(json_file.keys()))
