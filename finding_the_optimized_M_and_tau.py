import json
import math
import logging

logging.getLogger().setLevel(logging.INFO)

import M_cycling_function
import conf
import simulation_of_transmissions
import diversity
import filling_json_db


def store_in_json_file(M, numerical_monitoring_time, numerical_diversitie, numerical_tau,
                       analytical_monitoring_time, analytical_diversitie, analytical_tau, Q):
    with open(conf.json_dir_for_research_of_optimum, 'r') as file:
        json_file = json.load(file)
    if str(Q) not in json_file:
        json_file[str(Q)] = {}
    dic = {"num_D": numerical_monitoring_time, "num_Q": numerical_diversitie, "num_tau": numerical_tau,
           "ana_D": analytical_monitoring_time, "ana_Q": analytical_diversitie,
           "ana_tau": analytical_tau}
    json_file[str(Q)][str(M)] = dic
    with open(conf.json_dir_for_research_of_optimum, 'w+') as file:
        json.dump(json_file, file)


def finding_numericaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M):
    tau_min = 0.2
    is_ok = False
    while is_ok is False:
        sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
        monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_min, M, event, sensor_names)
        if monitoring_info is not False:
            simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
            Q_max = diversity.compute_diversity_penalty(emission_time_per_sensor, t_0, simul_time, tau_min, conf.T)
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
        sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
        monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_max, M, event, sensor_names)
        simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
        Q_min = diversity.compute_diversity_penalty(emission_time_per_sensor, t_0, simul_time, tau_max, conf.T)
        if Q_min < Q:
            is_ok = True
        else:
            tau_max += 0.1
    while tau_max - tau_min > conf.dif_tau:
        tau_inter = tau_min + (tau_max - tau_min) / 2
        sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
        monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
            M_cycling_function.cycling_over_M, tau_inter, M, event, sensor_names)
        simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
        Q_inter = diversity.compute_diversity_penalty(emission_time_per_sensor, t_0, simul_time, tau_inter, conf.T)
        if Q_inter > Q:
            tau_min = tau_inter
            Q_max = Q_inter
            D = simul_time - t_0
        else:
            # Q_min = Q_inter
            tau_max = tau_inter
    return Q_max, D, tau_min


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
    sensor_names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
    monitoring_info = simulation_of_transmissions.monitoring_of_sensor_emissions(
        M_cycling_function.cycling_over_M, tau_min, M, event, sensor_names)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_info
    Q = diversity.compute_diversity_penalty(emission_time_per_sensor, t_0, simul_time, tau_min, conf.T)
    return Q, simul_time - t_0, tau_min


def storing_the_fitting_tau_and_M_for_a_fixed_Q(Q, M_list):
    # M_min = math.ceil(Q)
    for M in M_list:
        logging.info("time for the parameter M= " + str(M))
        diver, monitoring_time,tau = finding_numericaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M)
        numerical_monitoring_time = monitoring_time
        numerical_diversitie = diver
        numerical_tau = tau

        diver, monitoring_time, tau = finding_analyticaly_the_fitting_tau_for_a_given_M_with_diver_Q(Q, M)
        analytical_monitoring_time = monitoring_time
        analytical_diversitie = diver
        analytical_tau = tau
        store_in_json_file(M, numerical_monitoring_time, numerical_diversitie, numerical_tau,
                          analytical_monitoring_time, analytical_diversitie, analytical_tau, Q)

def print_the_results_of_the_research_of_optimum_for_latex(Q):
    with open(conf.json_dir_for_research_of_optimum, 'r') as file:
        json_file = json.load(file)




if __name__ == '__main__':
    #filling_json_files.initialisation_of_json_file(conf.json_dir_for_research_of_optimum)
    storing_the_fitting_tau_and_M_for_a_fixed_Q(2.5, [10,50,100,150])
    Q = 2.5
    M = 100
    a = - conf.T * math.log(1 - 1 / Q)
    print(a)
    b = 2.5173448669732355
    print(analytical_function(M, a))
    print(analytical_function(M, 0.2))
    print(analytical_function(M, b))


