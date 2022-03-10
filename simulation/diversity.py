import math
import statistics

"""

"""


def update_stamp_indexes(next_emission_instant, emission_time_per_sensor, stamp_indexes_for_freshness):
    next_emission_instant
    for sensor_name in emission_time_per_sensor.keys():
        if stamp_indexes_for_freshness[sensor_name] == None:
            if emission_time_per_sensor[sensor_name][0] < next_emission_instant:
                stamp_indexes_for_freshness[sensor_name] = 0
        else:
            if stamp_indexes_for_freshness[sensor_name] < len(emission_time_per_sensor[sensor_name]) - 1:
                if emission_time_per_sensor[sensor_name][
                    stamp_indexes_for_freshness[sensor_name] + 1] < next_emission_instant:
                    stamp_indexes_for_freshness[sensor_name] += 1
    return stamp_indexes_for_freshness





def compute_diversity_thanks_to_sample_step(emission_time_per_sensor, t_0, simul_time, T, sample_step):
    utilities = []
    stamp_indexes_for_freshness = {}  ### at time t, it is the indexes times of the last emission before t of the sensors
    for sensor_name in emission_time_per_sensor.keys():
        stamp_indexes_for_freshness[sensor_name] = None
    t_minus_one = t_0



    emission_instant = t_0
    while emission_instant < simul_time:
        stamp_indexes_for_freshness = update_stamp_indexes(emission_instant, emission_time_per_sensor, stamp_indexes_for_freshness)
        utility = 0
        for sensor_name in emission_time_per_sensor.keys():
            if stamp_indexes_for_freshness[sensor_name] is not None:
                utility += math.exp(-(emission_instant - emission_time_per_sensor[sensor_name][stamp_indexes_for_freshness[sensor_name]])/T)
        utilities.append(utility)
        emission_instant += sample_step
    return utilities


def compute_average_diversity(emission_time_per_sensor, t_0, simul_time, T):
    utility = 0
    for sensor_name in emission_time_per_sensor:
        emission_list = emission_time_per_sensor[sensor_name]
        for i in range(1, len(emission_list)):
            utility += T * (1 - math.exp(-(emission_list[i] - emission_list[i - 1]) / T))
        utility += T * (1 - math.exp(-(simul_time - emission_list[len(emission_list) - 1]) / T))
    utility = utility / (simul_time - t_0)
    return utility
