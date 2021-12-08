import matplotlib.pyplot as plt
import statistics
import conf
import random


import worker
import M_cycling_function

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
        plt.scatter([elt - t_0 for elt in emission_time_per_sensor[sensor_name]],
                    [i for j in range(len(emission_time_per_sensor[sensor_name]))], edgecolor='none')
        if not_yet is True:
            plt.scatter([elt - t_0 for elt in changed_period[sensor_name]],
                        [i for j in range(len(changed_period[sensor_name]))], color='none',
                        edgecolor='black', linewidth=3, label="change of period instruction")
            not_yet = False
        else:
            plt.scatter([elt - t_0 for elt in changed_period[sensor_name]],
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

    plt.title("representation of the sensor emission over time")
    plt.xlabel("time line")
    plt.ylabel("index of the sensor")
    plt.legend(loc='lower center')
    plt.show()


if __name__ == '__main__':
    n = int(input("Enter the number of sensors :"))
    C = float(input("REMEMBER consumption of 1 emission=consumption of 1 reception = 1\n enter the capacity of each sensor :"))
    maxi = float(input("enter the size of the sensor activation time interval.\n The sensors will be activated randomly between 0 and this limit :"))
    M = int(input("enter the parameter M :"))
    tau = float(input("enter the parameter tau :"))

    t_i = []
    for i in range(n):
        t_i.append(random.uniform(0, maxi))
    names, event = worker.initialisation_of_sensors(t_i, battery=C)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0 = worker.monitoring_of_sensor_emissions(M_cycling_function.cycling_over_M, tau, M, event, names)
    plot_inter_arrival(dt, simul_time, emission_time_per_sensor, changed_period, t_0, tau)