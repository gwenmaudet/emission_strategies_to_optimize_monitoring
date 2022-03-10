import matplotlib.pyplot as plt
import statistics
import random
import logging
import math

logging.getLogger().setLevel(logging.INFO)

from simulation import simulation_of_transmissions,diversity
from f_M_Tau_function_and_plots import f_M_tau
import conf

"""
This file allows to see the behavior of the sensors in a graphical way (see explanatory figures in the paper). 
For the requested parameters, it will be displayed a curve of representation of the time between two consecutive emissions 
as well as a visualization of the emissions of each sensor, with their respective period changes.

USE IT LIKE A TOOL
"""

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
                    [i for j in range(len(emission_time_per_sensor[sensor_name]))], edgecolor='none',s=15)
        if not_yet is True:
            plt.scatter([(elt - t_0) for elt in changed_period[sensor_name]],
                        [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=2, label="change of period instruction",s=15)
            not_yet = False
        else:
            plt.scatter([(elt - t_0) for elt in changed_period[sensor_name]],
                        [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=2,s=15)
        i += 1
        if maxi < max(emission_time_per_sensor[sensor_name]):
            maxi = max(emission_time_per_sensor[sensor_name])
    time = 0
    plt.axvline(x=time, linestyle='--', label="footstep", linewidth=0.2)
    while time < maxi - t_0:
        time += tau
        plt.axvline(x=time, linestyle='--', linewidth=0.2)

    plt.title("Representation of the sensor emission over time")
    plt.xlabel("Time line")
    plt.ylabel("Index of the sensor")
    plt.legend(loc='lower right')
    plt.savefig("plots/toy_example.pdf", dpi=80, figsize=(10, 6))
    plt.show()


if __name__ == '__main__':
    """n = int(input("Enter the number of sensors :"))
    C = float(input("REMEMBER consumption of 1 emission=consumption of 1 reception = 1\n enter the capacity of each sensor :"))
    maxi = float(input("enter the size of the sensor activation time interval.\n The sensors will be activated randomly between 0 and this limit :"))
    M = int(input("enter the parameter M :"))
    tau = float(input("enter the parameter tau :"))"""
    n = 10
    C = 20
    maxi = 30
    M =3
    tau = 1
    t_i = []
    for i in range(n):
        t_i.append(random.uniform(0, maxi))
    names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=C)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
        f_M_tau.cycling_over_M, tau, event, names, M=M)

    #plot_inter_arrival(dt, simul_time, emission_time_per_sensor, changed_period, t_0, tau)

    t_i = []
    t_s = []
    t = 0
    for i in range(n):
        p = random.uniform(0, 1)
        t -= math.log(p) / conf.lambda_activation
        t_i.append(t)
        p = random.uniform(0, 1)
        new_time = t - math.log(p) / conf.lambda_shut_down
        t_s.append(new_time)
    names, event = simulation_of_transmissions.initialisation_of_sensors(t_i, battery=C, battery_type=2, shut_down=t_s)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes = simulation_of_transmissions.monitoring_of_sensor_emissions(
        f_M_tau.cycling_over_M, tau, event, names, M=None, known_battery=False)
    plot_inter_arrival(dt, simul_time, emission_time_per_sensor, changed_period, t_0, tau)