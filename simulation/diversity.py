import math
import statistics

"""

"""


def get_the_next_emission_and_sensor(simul_time, emission_time_per_sensor, stamp_indexes_for_freshness):
    next_emission_instant = simul_time
    next_emmitting_sensor = None
    for sensor_name in emission_time_per_sensor.keys():
        if stamp_indexes_for_freshness[sensor_name] == None:
            if emission_time_per_sensor[sensor_name][0] < next_emission_instant:
                next_emission_instant = emission_time_per_sensor[sensor_name][0]
                next_emmitting_sensor = sensor_name
        else:
            if stamp_indexes_for_freshness[sensor_name] < len(emission_time_per_sensor[sensor_name]) - 1:
                if emission_time_per_sensor[sensor_name][
                    stamp_indexes_for_freshness[sensor_name] + 1] < next_emission_instant:
                    next_emission_instant = emission_time_per_sensor[sensor_name][
                        stamp_indexes_for_freshness[sensor_name] + 1]
                    next_emmitting_sensor = sensor_name
    return next_emission_instant, next_emmitting_sensor


def update_stamps(stamp_indexes_for_freshness, next_emmitting_sensor):
    if stamp_indexes_for_freshness[next_emmitting_sensor] == None:
        stamp_indexes_for_freshness[next_emmitting_sensor] = 0
    else:
        stamp_indexes_for_freshness[next_emmitting_sensor] += 1
    return stamp_indexes_for_freshness


def compute_utility_between(emission_instant, t_minus_one, emission_time_per_sensor, stamp_indexes_for_freshness, T):
    utility = 0
    for sensor_name in emission_time_per_sensor.keys():
        if stamp_indexes_for_freshness[sensor_name] is not None:
            last_emission_time = emission_time_per_sensor[sensor_name][stamp_indexes_for_freshness[sensor_name]]
            utility += T * (math.exp(-(t_minus_one - last_emission_time) / T) - math.exp(
                -(emission_instant - last_emission_time) / T))
    return utility


def compute_diversity_part_by_part(emission_time_per_sensor, t_0, simul_time, T):
    utility = 0
    stamp_indexes_for_freshness = {}  ### at time t, it is the indexes times of the last emission before t of the sensors
    for sensor_name in emission_time_per_sensor.keys():
        stamp_indexes_for_freshness[sensor_name] = None
    t_minus_one = t_0
    emission_instant, next_emmitting_sensor = get_the_next_emission_and_sensor(simul_time, emission_time_per_sensor,
                                                                               stamp_indexes_for_freshness)
    while emission_instant != simul_time:
        adding_utility = compute_utility_between(emission_instant, t_minus_one, emission_time_per_sensor,
                                           stamp_indexes_for_freshness, T)
        utility += adding_utility
        stamp_indexes_for_freshness = update_stamps(stamp_indexes_for_freshness, next_emmitting_sensor)
        t_minus_one = emission_instant
        emission_instant, next_emmitting_sensor = get_the_next_emission_and_sensor(simul_time, emission_time_per_sensor,
                                                                                   stamp_indexes_for_freshness)
    adding_utility = compute_utility_between(emission_instant, t_minus_one, emission_time_per_sensor,
                                             stamp_indexes_for_freshness, T)
    utility += adding_utility
    utility = utility / (simul_time - t_0)
    return 1 / utility


def compute_average_diversity_penalty(emission_time_per_sensor, t_0, simul_time, T):
    utility = 0
    for sensor_name in emission_time_per_sensor:
        emission_list = emission_time_per_sensor[sensor_name]
        for i in range(1, len(emission_list)):
            utility += T * (1 - math.exp(-(emission_list[i] - emission_list[i - 1]) / T))
        utility += T * (1 - math.exp(-(simul_time - emission_list[len(emission_list) - 1]) / T))
    utility = utility / (simul_time - t_0)
    return 1 / utility
