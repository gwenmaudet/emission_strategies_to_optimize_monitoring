import random
import matplotlib.pyplot as plt

import conf
from simulation import simulation_of_transmissions, diversity
from binary_tree_function_periodic_recept import binary_tree_v1
import binary_tree_v2_without_any_conditions

if __name__ == '__main__':
    tau = 1

    names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
        binary_tree_v1.binary_tree, tau, event, names, known_battery=False)
    utilities = diversity.compute_diversity_thanks_to_sample_step(emission_time_per_sensor, t_0, simul_time, conf.T,
                                                                  conf.sample_step_for_diversity)
    utilities.sort()
    x = []
    y = []
    pct = 0
    n = len(utilities)
    while len(utilities) > 0:
        u = utilities.pop(0)
        x.append(u)
        pct += 1 / n
        y.append(pct)
    plt.plot(x, y, label="with periodic hypothesis")
    print("one done")
    names, event = simulation_of_transmissions.initialisation_of_sensors(conf.activation_times)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
        binary_tree_v2_without_any_conditions.binary_tree, tau, event, names, known_battery=False)
    utilities = diversity.compute_diversity_thanks_to_sample_step(emission_time_per_sensor, t_0, simul_time, conf.T,
                                                                  conf.sample_step_for_diversity)
    utilities.sort()
    x = []
    y = []
    pct = 0
    n = len(utilities)
    while len(utilities) > 0:
        u = utilities.pop(0)
        x.append(u)
        pct += 1 / n
        y.append(pct)
    plt.plot(x, y, label="without periodic hypothesis")
    plt.legend()
    plt.show()
