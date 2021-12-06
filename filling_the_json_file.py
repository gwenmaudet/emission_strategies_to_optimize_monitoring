import json
import time

import M_cycling_function
import conf
import worker
import diversity


"""
the format of the json stored will be for a given number of element, activating at the same time, with same energy parameters
json_file = {M_1:{tau_1 : [Monitoring_time, Diversity, emissions_time_per_sensor], tau_2 : [...]}, M_2:{tau_1:[...],tau_2:[..]}}
"""
def initialisation_of_json_file(M_list=[], tau_list=[]):
    json_initialised = {}
    if len(M_list) == 0:
        with open('json_storage.json', 'w+') as file:
            json.dump(json_initialised, file)
    else:
        for M in M_list:
            json_initialised[M] = {}
            for tau in tau_list:
                json_initialised[M][tau] =None
        with open('json_storage.json', 'w+') as file:
            json.dump(json_initialised, file)

def store_in_json_format(monitoring_time, diversity, emission_time_per_sensor, M, tau):


    with open('json_storage.json', 'r') as file:
        json_file = json.load(file) #The so called 'json_file' as the structure explained just above
        if M not in json_file:
            json_file[M] = {}
        if tau in json_file[M]:
            print("WARNING - ALLREADY A VALUE ENTERED for M: " + M + "and tau:" + tau)
        else:
            json_file[M][tau] = [monitoring_time, diversity, emission_time_per_sensor]
    with open('json_storage.json', 'w+') as file:
        json.dump(json_file, file)


def add_values_in_json_file(M_list,tau_list):
    for M in M_list:
        for tau in tau_list:
            time.sleep(1)
            print(M,tau)
            sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
            simul_time, dt, emission_time_per_sensor, changed_period, t_0 = worker.monitoring_of_sensor_emissions(
                M_cycling_function.cycling_over_M, tau, M, event, sensor_names)
            Q = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau, conf.T)
            store_in_json_format(simul_time-t_0, Q, emission_time_per_sensor, M, tau)


if __name__ == '__main__':
    #initialisation_of_json_file(M_list=[], tau_list=[])
    M_list = [i for i in range(2,conf.n)]
    tau_list = [0.5 + 0.1 * i for i in range(10)]
    add_values_in_json_file(M_list, tau_list)
    with open('json_storage.json', 'r') as file:
        json_file = json.load(file)
        print(json_file["2"])