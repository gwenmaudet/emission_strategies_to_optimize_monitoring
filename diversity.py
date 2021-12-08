import math
import statistics

"""

"""


def get_freshness(emission_time_per_sensor, t, sensor_begginning_indexes_for_freshness):
    freshness = {}

    for sensor_name in emission_time_per_sensor:
        i = sensor_begginning_indexes_for_freshness[sensor_name]
        found = False
        if i is None:
            if emission_time_per_sensor[sensor_name][0] > t:
                found = True
            else:
                i = 0
        while found is False:
            i += 1
            if len(emission_time_per_sensor[sensor_name]) == i:
                found = True
                sensor_begginning_indexes_for_freshness[sensor_name] = i - 1
                freshness[sensor_name] = t - emission_time_per_sensor[sensor_name][i - 1]
            elif emission_time_per_sensor[sensor_name][i] > t:
                found = True
                sensor_begginning_indexes_for_freshness[sensor_name] = i - 1
                freshness[sensor_name] = t - emission_time_per_sensor[sensor_name][i - 1]

    return freshness, sensor_begginning_indexes_for_freshness


def compute_freshness_expo(freshness, T):
    sum = 0
    for sensor_names in freshness:
        sum += math.exp(- freshness[sensor_names]/T)

    return sum



def compute_diversity(emission_time_per_sensor,t_0, simul_time, tau,  T):
    utility = []
    stamp_indexes_for_freshness = {}
    for sensor_name in emission_time_per_sensor.keys():
        stamp_indexes_for_freshness[sensor_name] = None

    for k in range(0, int((simul_time - t_0) / tau)):
        t = t_0 + k * tau
        freshness, stamp_indexes_for_freshness = get_freshness(emission_time_per_sensor, t,
                                                                           stamp_indexes_for_freshness)
        utility.append(compute_freshness_expo(freshness, T))
    mean_utility = statistics.mean(utility)
    return mean_utility