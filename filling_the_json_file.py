import json

import M_cycling_function
import conf
import worker
import diversity


"""
This file allows to fill a json file for the performance of a function for given parameters. 
We vary the parameters M and tau.

the format of the json stored will be for a given number of element, activating at the same time, with same energy parameters
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}
"""

def initialisation_of_json_file(M_list=[], tau_list=[]):
    json_initialised = {}
    with open('json_storage.json', 'w+') as file:
        json.dump(json_initialised, file)

def store_in_json_format(monitoring_time, diversity, emission_time_per_sensor, M, tau):
    with open(conf.json_dir, 'r') as file:
        json_file = json.load(file) #The so called 'json_file' as the structure explained just above
    strM = str(round(M, 3))
    strtau = str(round(tau,3))
    if strM not in json_file:
        json_file[strM] = {}
    if strtau in json_file[strM]:
        print("WARNING - ALLREADY A VALUE ENTERED for M: " + strM + "and tau:" + strtau)
    else:
        json_file[strM][strtau] = [monitoring_time, diversity, emission_time_per_sensor]
    with open(conf.json_dir, 'w+') as file:
        json.dump(json_file, file)


def add_values_in_json_file(M_list,tau_list):
    for M in M_list:
        for tau in tau_list:
            print(M,tau)
            sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0 = worker.monitoring_of_sensor_emissions(
                M_cycling_function.cycling_over_M, tau, M, event, sensor_names)
            Q = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau, conf.T)
            store_in_json_format(simul_time-t_0, Q, emission_time_per_sensor, M, tau)


if __name__ == '__main__':
    #initialisation_of_json_file(M_list=[], tau_list=[])
    M_list = [i for i in range(1, conf.n, 10)]
    tau_list = [4.6 + 0.2 * i for i in range(21)]
    add_values_in_json_file(M_list, tau_list)
    with open('json_storage.json', 'r') as file:
        json_file = json.load(file)
        print(json_file.keys())
