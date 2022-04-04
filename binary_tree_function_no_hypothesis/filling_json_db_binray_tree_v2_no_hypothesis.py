import json
import logging
import math
import random
import statistics

logging.getLogger().setLevel(logging.INFO)

import binary_tree_v2_without_any_conditions
import conf
from simulation import simulation_of_transmissions, diversity_and_nb_of_active_sensors

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



def do_simulation_binary_to_get_metrics(tau_list):
    for tau in tau_list:
        strtau = str(round(tau, 3))
        with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
            json_file = json.load(file)
        if strtau not in json_file.keys():
            t_i = []
            t_s = []
            t = 0
            p = random.uniform(0, 1)
            t -= math.log(p) / conf.lambda_
            while t < conf.stopping_time:
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
            sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=conf.C,
                                                                                        battery_type=2,
                                                                                        shut_down=t_s)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes, nb_of_change_ids = simulation_of_transmissions.monitoring_of_sensor_emissions(
                binary_tree_v2_without_any_conditions.binary_tree, tau, event, sensor_names, known_battery=False, beggining_time=conf.beggining_time,
                stopping_time=conf.stopping_time)
            average_number = diversity_and_nb_of_active_sensors.average_number_of_active_sensors(
                emission_time_per_sensor, t_0, simul_time)
            diversities = diversity_and_nb_of_active_sensors.compute_diversity_thanks_to_sample_step(
                emission_time_per_sensor, simul_time)

            # store average number of sensor
            with open(conf.json_dir_binary_nb_of_sensors, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            json_file[strtau] = average_number
            with open(conf.json_dir_binary_nb_of_sensors, 'w+') as file:
                json.dump(json_file, file)

            # store average diversity and std
            with open(conf.json_dir_binary_diversity_and_std, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            json_file[strtau] = {"average": statistics.mean(diversities), "std": statistics.stdev(diversities)}
            with open(conf.json_dir_binary_diversity_and_std, 'w+') as file:
                json.dump(json_file, file)

            # total number of emissions
            with open(conf.json_dir_binary_nb_of_emissions, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            json_file[strtau]= len(dt)
            with open(conf.json_dir_binary_nb_of_emissions, 'w+') as file:
                json.dump(json_file, file)

            # nb_of_perturbations
            with open(conf.json_dir_binary_nb_of_perturbations, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            nb_of_perturbation = 0
            for sensor_name in changed_period:
                nb_of_perturbation += len(changed_period[sensor_name])
            json_file[strtau] = nb_of_perturbation
            with open(conf.json_dir_binary_nb_of_perturbations, 'w+') as file:
                json.dump(json_file, file)

            #nb of id changes
            with open(conf.json_dir_binary_nb_of_change_ids, 'r') as file:
                json_file = json.load(file)  # The so called 'json_file' as the structure explained just above
            json_file[strtau] = nb_of_change_ids
            with open(conf.json_dir_binary_nb_of_change_ids, 'w+') as file:
                json.dump(json_file, file)


if __name__ == '__main__':
    # tau_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0 ]
    #tau_list = [0.05 + 0.02 * i for i in range(48)]
    tau_list = [1.01 + 0.02 * i for i in range(24)]

    """initialisation_of_json_file(conf.json_dir_binary_nb_of_sensors)
    initialisation_of_json_file(conf.json_dir_binary_diversity_and_std)
    initialisation_of_json_file(conf.json_dir_binary_nb_of_emissions)
    initialisation_of_json_file(conf.json_dir_binary_nb_of_perturbations)
    initialisation_of_json_file(conf.json_dir_binary_nb_of_change_ids)
    """
    do_simulation_binary_to_get_metrics(tau_list)