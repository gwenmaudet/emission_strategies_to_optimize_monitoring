import conf

import math
import statistics

"""

"""


def update_stamp_indexes(next_emission_instant, emission_time_per_sensor, stamp_indexes_for_freshness, sensor_set):
    next_emission_instant
    for sensor_name in sensor_set:
        if stamp_indexes_for_freshness[sensor_name] == None:
            if emission_time_per_sensor[sensor_name][0] < next_emission_instant:
                stamp_indexes_for_freshness[sensor_name] = 0
        else:
            if stamp_indexes_for_freshness[sensor_name] < len(emission_time_per_sensor[sensor_name]) - 1:
                if emission_time_per_sensor[sensor_name][
                    stamp_indexes_for_freshness[sensor_name] + 1] < next_emission_instant:
                    stamp_indexes_for_freshness[sensor_name] += 1
    return stamp_indexes_for_freshness





def compute_diversity_thanks_to_sample_step(emission_time_per_sensor, simul_time,beggining_time = conf.beggining_time, T=conf.T, sample_step=conf.sample_step):
    utilities = []
    emission_instant = beggining_time
    sensor_set = list(emission_time_per_sensor.keys())
    for sensor_name in emission_time_per_sensor.keys():
        if len(emission_time_per_sensor[sensor_name])== 0:
            sensor_set.remove(sensor_name)
    stamp_indexes_for_freshness = {}  ### at time t, it is the indexes times of the last emission before t of the sensors
    for sensor_name in sensor_set:
        stamp_indexes_for_freshness[sensor_name] = None
    while emission_instant < simul_time:
        stamp_indexes_for_freshness = update_stamp_indexes(emission_instant, emission_time_per_sensor, stamp_indexes_for_freshness, sensor_set)
        utility = 0
        elt_to_remove = []
        for sensor_name in sensor_set:
            if stamp_indexes_for_freshness[sensor_name] is not None:
                delta_t = emission_instant - emission_time_per_sensor[sensor_name][stamp_indexes_for_freshness[sensor_name]]
                utility += math.exp(-(delta_t)/T)
            if emission_instant - emission_time_per_sensor[sensor_name][
                len(emission_time_per_sensor[sensor_name]) - 1] > conf.threshold_delta_t:
                    elt_to_remove.append(sensor_name)
        for elt in elt_to_remove:
            sensor_set.remove(elt)
        utilities.append(utility)
        emission_instant += sample_step
    return utilities


def compute_average_diversity(emission_time_per_sensor, t_0, simul_time, T):
    utility = 0
    for sensor_name in emission_time_per_sensor:
        emission_list = emission_time_per_sensor[sensor_name]
        if len(emission_list) != 0:
            for i in range(1, len(emission_list)):
                utility += T * (1 - math.exp(-(emission_list[i] - emission_list[i - 1]) / T))
            utility += T * (1 - math.exp(-(simul_time - emission_list[len(emission_list) - 1]) / T))
    utility = utility / (simul_time - t_0)
    return utility


def average_number_of_active_sensors(emission_time_per_sensor, t_0, simul_time):
    average_number = 0
    tot_time = conf.stopping_time - conf.beggining_time
    for sensor_name in emission_time_per_sensor:
        if len(emission_time_per_sensor[sensor_name])!=0:
            average_number += (emission_time_per_sensor[sensor_name][len(emission_time_per_sensor[sensor_name]) - 1] - emission_time_per_sensor[sensor_name][0])/tot_time
    return average_number


