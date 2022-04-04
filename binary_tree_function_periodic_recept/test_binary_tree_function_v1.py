import matplotlib.pyplot as plt
import statistics
import random
import os
import math
import csv
import time

from simulation import simulation_of_transmissions
from binary_tree_function_periodic_recept import binary_tree_v1
import conf

def plot_inter_arrival(dt, simul_time, emission_time_per_sensor, changed_period, t_0, tau):
    plt.scatter([i for i in range(len(dt))], dt, label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    print("interarrival:", statistics.mean(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]),
          statistics.pvariance(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]))
    print(simul_time)

    sensor_names_ordered_by_arrival_order = []
    sensor_fst = []
    for sensor_name in emission_time_per_sensor:
        if sensor_names_ordered_by_arrival_order is []:
            sensor_names_ordered_by_arrival_order.append(sensor_name)
            sensor_fst.append(emission_time_per_sensor[sensor_name][0])
        else:
            done = False
            for i in range(len(sensor_names_ordered_by_arrival_order)):
                if done is False and emission_time_per_sensor[sensor_name][0] < sensor_fst[i]:
                    sensor_names_ordered_by_arrival_order.insert(i, sensor_name)
                    sensor_fst.insert(i, emission_time_per_sensor[sensor_name][0])
                    done = True
            if done is False:
                sensor_names_ordered_by_arrival_order.append(sensor_name)
                sensor_fst.append(emission_time_per_sensor[sensor_name][0])
                done = True
    maxi = 0
    not_yet = True
    i = 0
    for sensor_name in sensor_names_ordered_by_arrival_order:
        plt.scatter([(elt - t_0) for elt in emission_time_per_sensor[sensor_name]],
                    [i for j in range(len(emission_time_per_sensor[sensor_name]))], edgecolor='none')
        if not_yet is True:
            plt.scatter([(elt - t_0) for elt in changed_period[sensor_name]],
                        [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3, label="change of period instruction")
            not_yet = False
        else:
            plt.scatter([(elt - t_0) for elt in changed_period[sensor_name]],
                        [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3)
        i += 1
        if maxi < max(emission_time_per_sensor[sensor_name]):
            maxi = max(emission_time_per_sensor[sensor_name])
    time = 0
    plt.axvline(x=time, linestyle='--', label="footstep", linewidth=0.5)
    while time < maxi - t_0:
        time += tau
        plt.axvline(x=time, linestyle='--', linewidth=0.5)

    plt.title("Representation of the sensor emission over time")
    plt.xlabel("Time line")
    plt.ylabel("Index of the sensor")
    plt.legend(loc='lower center')
    plt.savefig("plots/toy_example_binary_tree_v1.pdf", dpi=80, figsize=(10, 6))
    plt.show()

    #Write latex file
    open("latex_files/toy_example.tex", "w").close()

    i = 1
    period_change_data = []
    for sensor_name in emission_time_per_sensor:
        data = []
        for elt in emission_time_per_sensor[sensor_name]:
            data.append([elt - t_0, i])
        for elt in changed_period[sensor_name]:
            period_change_data.append([elt - t_0, i])

        with open('latex_files/toy_example.tex', 'a') as fout:
            fout.write(("\\begin{filecontents}{toy_example"+ str(i) + ".csv}\n x,y\n"))
            for elt in data:
                fout.write(str(elt[0]) + ' , ' + str(elt[1]) + '\n')
            fout.write("\end{filecontents}\n")
        i += 1
    with open('latex_files/toy_example.tex', 'a') as fout:
        fout.write("\\begin{filecontents}{toy_example_period_changes.csv}\n")
        fout.write('x,y\n')
        for elt in period_change_data:
            fout.write(str(elt[0]) + ' , ' + str(elt[1]) + '\n')
        fout.write("\end{filecontents}")
    print(len(emission_time_per_sensor))


if __name__ == '__main__':
    n = 10
    C = 5
    tau = 1
    stopping_time = 35
    t_i = []
    t_s = []
    t = 0
    p = random.uniform(0, 1)
    t -= math.log(p) / conf.lambda_
    while t<stopping_time:
        t_i.append(t)
        p = random.uniform(0, 1)
        new_time = t - math.log(p)/conf.mu
        t_s.append(new_time)
        p = random.uniform(0, 1)
        t -= math.log(p) / conf.lambda_
    names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=C, battery_type=2, shut_down=t_s)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
        binary_tree_v1.binary_tree, tau, event, names, known_battery=False, stopping_time=stopping_time)
    print(emission_time_per_sensor)
    print(t_0)
    plot_inter_arrival(dt, simul_time, emission_time_per_sensor, changed_period, t_0, tau)