import json
import logging
import math
import random

logging.getLogger().setLevel(logging.INFO)

import binary_tree_v1
import conf
from simulation import simulation_of_transmissions, diversity_and_nb_of_active_sensors
from f_M_Tau import f_M_tau
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

def comparison_f_m_tua_binary(json_to_fill_binary, json_file_f_M_tau, tau_list, nb_of_iterations, stopping_time):
    """with open(json_to_fill_binary, 'r') as file:
        binray_file = json.load(file)
    with open(json_file_f_M_tau, 'r') as file:
        f_m_tau_file = json.load(file)"""
    for tau in tau_list:
        for i in range(nb_of_iterations):

            t_i = []
            t_s = []
            t = 0
            p = random.uniform(0, 1)
            t -= math.log(p) / conf.lambda_
            while t < stopping_time:
                t_i.append(t)
                p = random.uniform(0, 1)
                new_time = t - math.log(p) / conf.mu
                t_s.append(new_time)
                p = random.uniform(0, 1)
                t -= math.log(p) / conf.lambda_
            # binary
            logging.info(
                    "filling the data base '" + json_to_fill_binary + "' with parameters  tau=" + str(
                        round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C, battery_type=2,
                                                                                 shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v1.binary_tree, tau, event, sensor_names, known_battery=False, stopping_time=stopping_time)
            Q = diversity_and_nb_of_active_sensors.compute_average_diversity(emission_time_per_sensor, t_0, simul_time, conf.T)
            store_one_new_value_in_json_db(simul_time - t_0, Q, nb_of_changes, tau, json_to_fill_binary)
            #f_m_tau

            logging.info(
                "filling the data base '" + json_file_f_M_tau + "' with parameters  tau=" + str(
                    round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C,
                                                                                        battery_type=2,
                                                                                        shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                f_M_tau.cycling_over_M, tau, event, sensor_names,M=None, known_battery=False,stopping_time=stopping_time)
            Q = diversity_and_nb_of_active_sensors.compute_average_diversity(emission_time_per_sensor, t_0, simul_time, conf.T)

            store_one_new_value_in_json_db(simul_time - t_0, Q, nb_of_changes, tau, json_file_f_M_tau)


def initialise_if_empty(tau):
    with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
        json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
    strtau = str(round(tau, 3))
    if strtau not in json_file.keys():
        json_file[strtau] = {"battery_exponential": [], "discrete_consumption": []}
    #json_file[strtau]["battery_exponential"].append(average_number)
    with open(conf.json_dir_binary_nb_of_sensors, 'w+') as file:
        json.dump(json_file, file)


def do_simulation_multiple_times_and_get_metrics( tau_list, nb_of_iterations, stopping_time):
    nb_of_sensor = conf.json_dir_binary_nb_of_sensors
    """nb_of_emissions =
    nb_of_pertubation =
    average_diversity_with_std ="""
    for tau in tau_list:
        for i in range(nb_of_iterations):

            t_i = []
            t_s = []
            t = 0
            p = random.uniform(0, 1)
            t -= math.log(p) / conf.lambda_
            while t < stopping_time:
                t_i.append(t)
                p = random.uniform(0, 1)
                new_time = t - math.log(p) / conf.mu
                t_s.append(new_time)
                p = random.uniform(0, 1)
                t -= math.log(p) / conf.lambda_
            # binary
            logging.info(
                    "filling the data base with parameters  tau=" + str(
                        round(tau, 3)))
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C, battery_type=2,
                                                                                 shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v1.binary_tree, tau, event, sensor_names, known_battery=False, stopping_time=stopping_time)
            average_number = diversity_and_nb_of_active_sensors.average_number_of_active_sensors(emission_time_per_sensor, t_0, simul_time)
            diversities =diversity_and_nb_of_active_sensors.compute_diversity_thanks_to_sample_step(emission_time_per_sensor, t_0, simul_time, conf.T, conf.sample_step)
            with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            strtau = str(round(tau, 3))
            json_file[strtau].append(average_number)
            with open(conf.json_dir_binary_nb_of_sensors, 'w+') as file:
                json.dump(json_file, file)
            if strtau not in json_file.keys():
                json_file[strtau] = {"battery_exponential": [], "discrete_consumption": []}

            with open(conf.json_dir_binary_nb_of_sensors, 'w+') as file:
                json.dump(json_file, file)

            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C,
                                                                                        battery_type=1,
                                                                                        shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v1.binary_tree, tau, event, sensor_names, known_battery=False, stopping_time=stopping_time)
            average_number = diversity_and_nb_of_active_sensors.average_number_of_active_sensors(
                emission_time_per_sensor, t_0, simul_time)

            with open(nb_of_sensor, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            strtau = str(round(tau, 3))
            json_file[strtau]["discrete_consumption"].append(average_number)
            with open(nb_of_sensor, 'w+') as file:
                json.dump(json_file, file)


if __name__ == '__main__':
    #tau_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0 ]
    tau_list = [0.32 + 0.02 * i for i in range (10) ]
    stopping_time = 100000
    nb_of_iterations = 20

    initialisation_of_json_file(conf.json_dir_binary_nb_of_sensors)

    do_simulation_multiple_times_and_get_metrics(tau_list, nb_of_iterations, stopping_time)

    """
    json_to_fill_binary = conf.json_dir_for_db_binary_tree_function_v1
    json_file_f_M_tau = conf.json_dir_f_M_tau_for_comparison
    #initialisation_of_json_file(json_file_f_M_tau)
    #initialisation_of_json_file(json_to_fill_binary)
    tau_list = [0.1 + 0.1 * i for i in range(10)]
    tau_list = [1]
    stopping_time = 50000
    nb_of_iterations = 20
    #tau_list = [0.1 + 0.2 * i for i in range(50)]
    #tau_list = [0.8, 1.4, 2.2, 3.2, 4.4, 5.8, 7.4]
    #M_list = [i for i in range(1, 200, 2)]
    comparison_f_m_tua_binary(json_to_fill_binary, json_file_f_M_tau, tau_list, nb_of_iterations, stopping_time)"""
