import json
import math
import logging

logging.getLogger().setLevel(logging.INFO)

import M_cycling_function
import conf
import worker
import diversity
import filling_json_files


def store_in_json_file(M_list, numerical_monitoring_times, numerical_diversities,
                       analytical_monitoring_times, analytical_diversities, Q):
    with open(conf.json_dir_for_research_of_optimum, 'r') as file:
        json_file = json.load(file)
    if str(Q) not in json_file:
        json_file[str(Q)] = {}
    for i in range (len(M_list)):
        M = M_list[i]
        dic = {"num_D":numerical_monitoring_times[i], "num_Q": numerical_diversities[i],
               "ana_D": analytical_monitoring_times[i], "ana_Q": analytical_diversities[i]}
        json_file[str(Q)][str(M)] = dic
    with open(conf.json_dir_for_research_of_optimum, 'w+') as file:
        json.dump(json_file, file)


def finding_numericaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M):
    tau_min = 0.2
    is_ok = False
    while is_ok is False:
        sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
        monitoring_info = worker.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_min, M, event, sensor_names)
        if monitoring_info is not False:
            simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
            Q_max = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau_min, conf.T)
            D = simul_time - t_0
            if Q_max > Q:
                is_ok = True
            else:
                tau_min -= 0.05
        else:
            tau_min += 0.02
    tau_max = - conf.T * math.log(1 - 1 / Q)
    is_ok = False
    while is_ok is False:
        sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
        monitoring_info = worker.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_max, M, event, sensor_names)
        simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
        Q_min = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau_max, conf.T)
        if Q_min < Q:
            is_ok = True
        else:
            tau_max += 0.1
    while tau_max - tau_min > conf.dif_tau:
        tau_inter = tau_min + (tau_max - tau_min) / 2
        sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
        monitoring_info = worker.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_inter, M, event, sensor_names)
        simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
        Q_inter = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau_inter, conf.T)
        if Q_inter > Q:
            tau_min = tau_inter
            Q_max = Q_inter
            D = simul_time - t_0
        else:
            # Q_min = Q_inter
            tau_max = tau_inter
    return Q_max, D


def analytical_function(M, tau):
    return (1 - math.exp(-tau * M / conf.T)) / (1 - math.exp(-tau / conf.T))


def finding_analyticaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M):
    tau_min = 0.2
    is_ok = False
    while is_ok is False:
        if analytical_function(M, tau_min) > Q:
            is_ok = True
        else:
            tau_min -= 0.05
    tau_max = - conf.T * math.log(1 - 1 / Q)
    while tau_max - tau_min > conf.dif_tau:
        tau_inter = tau_min + (tau_max - tau_min) / 2
        if analytical_function(M, tau_inter) > Q:
            tau_min = tau_inter
        else:
            tau_max = tau_inter
    sensor_names, event = worker.initialisation_of_sensors(conf.activation_times)
    monitoring_info = worker.monitoring_of_sensor_emissions(
        M_cycling_function.cycling_over_M, tau_min, M, event, sensor_names)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
    Q = diversity.compute_diversity(emission_time_per_sensor, t_0, simul_time, tau_min, conf.T)
    return Q, simul_time - t_0


def storing_the_fitting_tau_and_M_for_a_fixed_Q(Q, M_list):
    # M_min = math.ceil(Q)
    numerical_monitoring_times = []
    numerical_diversities = []
    analytical_monitoring_times = []
    analytical_diversities = []
    for M in M_list:
        logging.info("time for the parameter M= " + str(M))
        diver, monitoring_time = finding_numericaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M)
        numerical_monitoring_times.append(monitoring_time)
        numerical_diversities.append(diver)

        diver, monitoring_time = finding_analyticaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M)
        analytical_monitoring_times.append(monitoring_time)
        analytical_diversities.append(diver)
    store_in_json_file(M_list, numerical_monitoring_times, numerical_diversities,
                       analytical_monitoring_times, analytical_diversities, Q)

def show_the_results_of_the_research_of_optimum():



if __name__ == '__main__':
    storing_the_fitting_tau_and_M_for_a_fixed_Q(2.5, [10,20,30])
    #filling_json_files.initialisation_of_json_file(conf.json_dir_for_research_of_optimum)

