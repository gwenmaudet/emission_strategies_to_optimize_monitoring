import random
import statistics
import matplotlib.pyplot as plt
import numpy as np
from math import log, ceil
import time
import conf
import math

elm = 0
M = 1

"""
TOOLBOX
"""


def insert_event(elm, event):
    for i in range(len(event)):
        if event[i].wake_up > elm.wake_up:
            event.insert(i, elm)
            return event

    # last element
    event.append(elm)
    return event


def get_the_first_death_of_sensor():
    global end_of_devices
    for elt in end_of_devices:
        if elt[1] != None:
            sensor_death = elt[1]
            elt[1] = None
            return sensor_death


def update_end_of_devices(new_death):
    global end_of_devices
    index_to_delete = None

    for i in range(len(end_of_devices)):
        if end_of_devices[i][0] == new_death[0]:
            if end_of_devices[i][1] == new_death[1] or end_of_devices[i][1] == None:
                return
            else:
                index_to_delete = i
    if index_to_delete is not None:
        del end_of_devices[index_to_delete]

    for i in range(len(end_of_devices)):
        if end_of_devices[i][1] is not None and end_of_devices[i][1] > new_death[1]:
            end_of_devices.insert(i, new_death)
            return
    time.sleep(0.01)
    end_of_devices.append(new_death)


def is_in_end_of_devices(name):
    global end_of_devices
    for elt in end_of_devices:
        if elt[0] == name:
            return True
    return False


def get_freshness(sensor_emissions_dic, t, sensor_begginning_indexes_for_freshness):
    freshness = {}

    for sensor_name in sensor_emissions_dic:
        i = sensor_begginning_indexes_for_freshness[sensor_name]
        found = False
        if i is None:
            if sensor_emissions_dic[sensor_name][0] > t:
                found = True
            else:
                i = 0
        while found is False:
            i += 1
            if len(sensor_emissions_dic[sensor_name]) == i:
                found = True
                sensor_begginning_indexes_for_freshness[sensor_name] = i - 1
                freshness[sensor_name] = t - sensor_emissions_dic[sensor_name][i - 1]
            elif sensor_emissions_dic[sensor_name][i] > t:
                found = True
                sensor_begginning_indexes_for_freshness[sensor_name] = i - 1
                freshness[sensor_name] = t - sensor_emissions_dic[sensor_name][i - 1]

    return freshness, sensor_begginning_indexes_for_freshness


def compute_freshness_expo(freshness, alpha):
    sum = 0
    for sensor_names in freshness:
        sum += math.exp(- alpha * freshness[sensor_names])

    return sum


"""
sensor class for initialisation of sensors, and management of their comportment
"""


class sensor:
    def __init__(self, period=0, error=None, err_args=None, name="sensor",
                 battery=conf.C, fst_wake_up=0, time_out_of_scope=None, event=[]):
        global elm
        self.period = period
        self.battery = battery
        self.name = "{}_{:04}".format(name, elm)
        elm += 1
        self.expected_next_emission = None
        self.need_one_changing_of_period = False
        self.time_out_of_scope = time_out_of_scope
        self.is_out_of_scope = False
        # self.wake_up = fst_wake_up + random.uniform(0, self.period)
        self.wake_up = fst_wake_up
        self.fst_emission = self.wake_up
        event = insert_event(self, event)

    def sleep(self, simul_time, event):
        if self.time_out_of_scope is not None and simul_time + self.period > self.time_out_of_scope:
            self.is_out_of_scope = True
        if self.battery < conf.c_e:  # when battery is empty
            return False, event
        # self.wake_up = simul_time + random.uniform(0, self.period)
        self.wake_up = simul_time + self.period
        event = insert_event(self, event)
        return True, event

    def draw(self):
        if self.is_out_of_scope is False:
            self.battery -= conf.c_e
            return 0  # self.value
        # else:
        #    return None  ##meaning that the sensor has been taken out of the environment

    def set_period(self, period):
        p = random.random()
        if p < 1:
            self.period = period
            self.battery -= conf.c_r


"""
View of a sensor from the gateway
"""


class sensor_view:
    def __init__(self, sensor):
        self.name = sensor.name
        self.period = sensor.period
        self.battery = sensor.battery
        self.expected_next_emission = sensor.expected_next_emission

    def give_view(self):
        print("###")
        print(self.name)
        print(self.period)
        print(self.expected_next_emission)


"""
information system knowledge
"""


class information_system:
    def __init__(self):
        self.sensor_view_list = {}

    def update(self, sensor):
        self.sensor_view_list[sensor.name] = [sensor_view(sensor)]

    def remove(self, sensor):
        if sensor.name in self.sensor_view_list:
            del self.sensor_view_list[sensor.name]

    def is_in(self, sensor):
        if sensor.name in self.sensor_view_list:
            return True
        else:
            return False

    def length(self):
        return len(self.sensor_view_list)


"""
Initialisation of the sensors
"""


def initialisation_of_sensors(fixed_arrival=False, begginning_time_list=None):
    event = []

    names = []
    stopping_times = {}
    begginning_times = {}
    # print("sensor startin from the begginning finishing early")
    if begginning_time_list is not None:
        for i in range(conf.n):
            s = sensor(name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning_time_list[i],
                       event=event)
            names.append(s.name)
        return names, event, begginning_time_list
    begginning_time_list = []
    if fixed_arrival is False:
        for i in range(conf.n):
            begginning = random.uniform(0, ((conf.C - conf.c_r) // conf.c_e) * conf.tau * int(i))
            begginning = random.uniform(0, 50)
            begginning_time_list.append(begginning)
            s = sensor(name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning, event=event)
            names.append(s.name)
    else:
        t_i = 0
        for i in range(conf.n):
            begginning = random.uniform(t_i + conf.tau * (i + 2),
                                        t_i + conf.tau * (i + 5))
            # begginning = 10
            begginning_time_list.append(begginning)
            # s = sensor(12, name="class C", error=random.gauss, err_args=(0, 2))
            s = sensor(name="class C", error=random.gauss, err_args=(0, 2), fst_wake_up=begginning, event=event)
            t_i = s.fst_emission

            # print(s.name)
            # print(end)
            names.append(s.name)
            # stopping_times[s.name] = end
            begginning_times[s.name] = s.fst_emission
    return names, event, begginning_time_list


"""
General monitoring of sensor emission, taking initial sensor emissions, and an algorithm of emission management
"""


def monitoring_of_sensor_emissions(management_function, event, sensor_names):
    # global sensor_view_list
    simul_time = 0
    dt = []
    emission_time_per_sensor = {}
    changed_period = {}
    initial_time = 0
    for name in sensor_names:
        emission_time_per_sensor[name] = []
        changed_period[name] = []

    management_function(None, 0)
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        delta_t = evt.wake_up - simul_time
        if initial_time == 0:
            initial_time = simul_time
        sensor_value = evt.draw()
        simul_time = evt.wake_up
        view = sensor_view(evt)
        new_period = management_function(view, simul_time)  ######## use of the management function
        if sensor_value is not None:  # le message recu n'indique pas que le capteur est passé en dehors de l'environnement
            dt.append(delta_t)
            emission_time_per_sensor[evt.name].append(simul_time)
            if new_period is not None and evt.battery >= conf.c_r:
                evt.set_period(new_period)
                changed_period[evt.name].append(simul_time)
            evt.expected_next_emission = simul_time + evt.period
            bool, event = evt.sleep(simul_time, event)
            # if bool is False:
            #    sensor_view_list.remove(evt)
        # else:
        #    sensor_view_list.remove(evt)
    return simul_time, dt, emission_time_per_sensor, changed_period, initial_time


"""
Function that takes a number of active sensor M, and propose a solution that cycle all avor the time M
"""


def cycling_over_M(evt, simul_time):
    global M
    global t_0
    global end_of_devices
    global sensor_view_list
    new_period = None
    if evt is None:
        sensor_view_list = information_system()
        t_0 = 0
        end_of_devices = []
    else:
        if sensor_view_list.is_in(evt) is False:  # first emission of the sensor
            sensor_view_list.update(evt)
            if sensor_view_list.length() <= M:  # it will directly be included in the cycle
                if sensor_view_list.length() == 1:
                    t_0 = simul_time
                    new_period = conf.tau
                else:
                    new_period = conf.tau - (
                            simul_time - t_0) % conf.tau + (
                                         sensor_view_list.length() - 1) * conf.tau
            else:  # it would switch of just after the death of the next sensor, with a period of tau
                beggining_of_this_sensor = get_the_first_death_of_sensor()
                new_period = beggining_of_this_sensor - simul_time
        else:
            sensor_view_list.update(evt)
            if evt.period != min(sensor_view_list.length(), M) * conf.tau:
                new_period = min(sensor_view_list.length(), M) * conf.tau
                if evt.battery < conf.c_e + conf.c_r:
                    sensor_view_list.remove(evt)
            else:
                if evt.battery < conf.c_e:
                    sensor_view_list.remove(evt)

        # updating of end_of_device
        # sensor that have changed their period to M\tau or that didn't chang their period but will do at next emission : one change of period
        sensor_death = None
        if new_period == M * conf.tau:
            sensor_death = simul_time + ((evt.battery - conf.c_r) // conf.c_e + 1) * conf.tau * M
        elif new_period is None and evt.period != M * conf.tau:
            sensor_death = simul_time + evt.period + (
                        (evt.battery - conf.c_r - conf.c_e) // conf.c_e + 1) * conf.tau * M
        # sensor have changed it period but would need to change a second time to be really scheduled : 2 change of period
        elif new_period is not None and new_period != M * conf.tau:
            sensor_death = simul_time + new_period + (
                        (evt.battery - 2 * conf.c_r - conf.c_e) // conf.c_e + 1) * conf.tau * M
        # if sensor_death is None : pas de changement de periode et deja la période finale : M * \tau
        if sensor_death is not None:
            update_end_of_devices([evt.name, sensor_death])
    return new_period


# structure de l'enregistrement de division cycling : [[instants du prochain capteur qui a une période \tau
def smart_insert(memory_stamp, name, next_emission, multiplicator, is_new=False):
    if not is_new:
        is_deleted = False
        i = 0
        while not is_deleted and i != len(memory_stamp):
            if memory_stamp[i]["name"] == name:
                del memory_stamp[i]
                is_deleted = True
            i += 1
    for i in range(len(memory_stamp)):
        if memory_stamp[i]["multiplicator"] > multiplicator \
                or (memory_stamp[i]["multiplicator"] == multiplicator and memory_stamp[i][
            "next_emission"] >= next_emission):
            memory_stamp.insert(i, {"name": name, "next_emission": next_emission,
                                    "multiplicator": multiplicator})
            return memory_stamp
    memory_stamp.append({"name": name, "next_emission": next_emission,
                         "multiplicator": multiplicator})
    return memory_stamp


#  {"name":, "next_emission":, "multiplicator":, "view":}
def find_the_new_period_and_update(memory_stamp, evt, simul_time):
    elt = memory_stamp[0]
    elt["multiplicator"] += 1
    memory_stamp = smart_insert(memory_stamp, elt["name"], elt["next_emission"], elt["multiplicator"])
    new_period = elt["next_emission"] - simul_time + conf.tau * math.pow(2, elt["multiplicator"] - 1)
    memory_stamp = smart_insert(memory_stamp, evt.name, new_period + simul_time, elt["multiplicator"], is_new=True)
    return new_period, memory_stamp


def find_elt_in_memory_stamp(evt, memory_stamp):
    for elt in memory_stamp:
        if elt["name"] == evt.name:
            return elt

"""
def update_the_death_in_memory_stamp(memory_stamp, next_emissions_to_modify, multiplicator):

    i = 0
    is_found = False
    while i < len(memory_stamp):
        elt = memory_stamp[i]
        if round(elt["next_emission"] - next_emissions_to_modify, 3) == 0:
            if elt["multiplicator"] == multiplicator:
                #elt["need_to_replace_the_dead"] = True
                elt["multiplicator"] -= 1
                return memory_stamp
            else:
                if not is_found:
                    elt["need_to_replace_the_dead"] = True
                    next_emissions_to_modify = next_emissions_to_modify + math.pow(2, elt["multiplicator"]-1)
                    is_found = True
                #update_the_death_in_memory_stamp(memory_stamp, next_emissions_to_modify, multiplicator)
                elt["multiplicator"] -= 1

        i += 1
    return memory_stamp

"""
def update_the_death_in_memory_stamp(memory_stamp, simul_time, period, multiplicator):
    i = 0
    next_emission_to_modify = simul_time + period / 2
    #is_found = False
    elt = memory_stamp[0]
    if elt["multiplicator"] == multiplicator:
        i = 0
        while i < len(memory_stamp):
            elt = memory_stamp[i]
            if round(elt["next_emission"] - next_emission_to_modify, 3) == 0:
                if elt["multiplicator"] == multiplicator:
                    # elt["need_to_replace_the_dead"] = True
                    elt["multiplicator"] -= 1
                    return memory_stamp
                else:

                    memory_stamp = update_the_death_in_memory_stamp(memory_stamp, elt["next_emission"],
                                                                    math.pow(2, elt["multiplicator"]),
                                                                    elt["multiplicator"])

                    elt["multiplicator"] = multiplicator
                    elt["new_imposed_period"] = math.pow(2, elt["multiplicator"]-1) * conf.tau
            i += 1

    else:
        a=0


    return memory_stamp



def division_cycling(evt, simul_time):
    global memory_stamp
    global sensor_view_list
    #global multiplimax

    new_period = None
    if evt is None:
        memory_stamp = []
        sensor_view_list = information_system()
        return new_period
    else:
        #print(memory_stamp)
        #print(simul_time)
        #evt.give_view()
        if memory_stamp == []:
            sensor_view_list.update(evt)
            memory_stamp.append({"name": evt.name, "next_emission": simul_time + conf.tau, "multiplicator": 0})
        else:
            if not sensor_view_list.is_in(evt):
                sensor_view_list.update(evt)
                new_period, memory_stamp = find_the_new_period_and_update(memory_stamp, evt, simul_time)
            else:
                elt = find_elt_in_memory_stamp(evt, memory_stamp)
                if "new_imposed_period" in elt.keys():
                    new_period = elt["new_imposed_period"]
                    del elt["new_imposed_period"]
                    memory_stamp = smart_insert(memory_stamp, evt.name, new_period + simul_time, elt["multiplicator"])

                elif evt.period != math.pow(2, elt["multiplicator"]) * conf.tau:
                    new_period = math.pow(2, elt["multiplicator"]) * conf.tau
                    memory_stamp = smart_insert(memory_stamp, evt.name, new_period + simul_time, elt["multiplicator"])
                else:
                    memory_stamp = smart_insert(memory_stamp, evt.name, simul_time + evt.period, elt["multiplicator"])
    if new_period is not None and evt.battery < conf.c_e + conf.c_r:
        sensor_view_list.remove(evt)
        memory_stamp = update_the_death_in_memory_stamp(memory_stamp, simul_time, new_period, elt["multiplicator"])
    if new_period is None and evt.battery < conf.c_e:
        sensor_view_list.remove(evt)
        memory_stamp = update_the_death_in_memory_stamp(memory_stamp, simul_time, evt.period, elt["multiplicator"])
    if new_period is not None and new_period<=0 :
        print(new_period)
    return new_period


def plot_inter_arrival(dt, monitoring_time, sensor_emissions_dic, changed_period, t_0):
    plt.scatter([i for i in range(len(dt))], dt, label="inter-arrival over time")
    plt.title("inter arrival over time")
    plt.xlabel("iteration of reception")
    plt.ylabel("time difference between the last 2 reception")
    plt.legend()
    plt.show()
    print("interarrival:", statistics.mean(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]),
          statistics.pvariance(dt[int(len(dt) / 5):int(len(dt) * 3 / 5)]))
    print(monitoring_time)

    sensor_names = []
    sensor_fst = []
    for sensor_name in sensor_emissions_dic:
        if sensor_names is []:
            sensor_names.append(sensor_name)
            sensor_fst.append(sensor_emissions_dic[sensor_name][0])
        else:
            done = False
            for i in range(len(sensor_names)):
                if done is False and sensor_emissions_dic[sensor_name][0] < sensor_fst[i]:
                    sensor_names.insert(i, sensor_name)
                    sensor_fst.insert(i, sensor_emissions_dic[sensor_name][0])
                    done = True
            if done is False:
                sensor_names.append(sensor_name)
                sensor_fst.append(sensor_emissions_dic[sensor_name][0])
                done = True
    i = 0
    maxi = 0
    not_yet = True

    for sensor_name in sensor_names:
        plt.scatter([elt - t_0 for elt in sensor_emissions_dic[sensor_name]],
                    [i for j in range(len(sensor_emissions_dic[sensor_name]))], edgecolor='none')
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
        if maxi < max(sensor_emissions_dic[sensor_name]):
            maxi = max(sensor_emissions_dic[sensor_name])
    time = 0
    plt.axvline(x=time, linestyle='--', label="footstep", linewidth=0.5)
    while time < maxi - t_0:
        time += conf.tau
        plt.axvline(x=time, linestyle='--', linewidth=0.5)
    plt.title("representation of the sensor emission over time")
    plt.xlabel("time line")
    plt.ylabel("index of the sensor")
    plt.legend(loc='lower center')
    plt.show()

    x = []
    utility = []
    sensor_begginning_indexes_for_freshness = {}
    for sensor_name in sensor_emissions_dic:
        sensor_begginning_indexes_for_freshness[sensor_name] = None
    for k in range(0, int((maxi - t_0) / conf.tau)):
        t = t_0 + k * conf.tau
        freshness, sensor_begginning_indexes_for_freshness = get_freshness(sensor_emissions_dic, t,
                                                                           sensor_begginning_indexes_for_freshness)
        utility.append(compute_freshness_expo(freshness, conf.alpha))
        x.append(k)
    plt.plot(x, utility)
    plt.title("Sum of the utilities over time")
    plt.xlabel("footstep")
    plt.ylabel("utility ")
    plt.legend(loc='lower center')
    plt.show()


def plot_duration_and_utility_function_of_M():
    global M
    x = []
    durations = []
    utilities = []
    names, event_stamp, begginning_time_list = initialisation_of_sensors(fixed_arrival=True)
    for M in range(1, conf.n + 1):
        names, event, begginning_time_list = initialisation_of_sensors(fixed_arrival=True,
                                                                       begginning_time_list=begginning_time_list)
        sensor_names = names
        x.append(M)
        simul_time, dt, sensor_emissions_dic, changed_period, t_0 = monitoring_of_sensor_emissions(cycling_over_M,
                                                                                                   event, sensor_names)

        durations.append(simul_time - t_0)
        utility = []
        sensor_begginning_indexes_for_freshness = {}
        for sensor_name in sensor_emissions_dic:
            sensor_begginning_indexes_for_freshness[sensor_name] = None
        for k in range(0, int((simul_time - t_0) / conf.tau)):
            t = t_0 + k * conf.tau
            freshness, sensor_begginning_indexes_for_freshness = get_freshness(sensor_emissions_dic, t,
                                                                               sensor_begginning_indexes_for_freshness)
            utility.append(compute_freshness_expo(freshness, conf.alpha))
        mean_utility = statistics.mean(utility)
        utilities.append(mean_utility)

    plt.plot(x, utilities)
    plt.title("Mean utilities according to M")
    plt.xlabel("M")
    plt.ylabel("mean utility ")
    plt.legend(loc='lower center')
    plt.show()

    plt.plot(x, durations)
    plt.title("monitoring time according to M")
    plt.xlabel("M")
    plt.ylabel("monitoring time ")
    plt.legend(loc='lower center')
    plt.show()

    compromise = []
    for i in range(len(x)):
        compromise.append(42 * utilities[i] + durations[i])

    plt.plot(x, compromise)
    plt.title("compromise curve")
    plt.xlabel("M")
    plt.ylabel("monitoring time ")
    plt.legend(loc='lower center')
    plt.show()

def fill_json_file_with_values



if __name__ == "__main__":
    """M = 10000
    sensor_names, event, begginnings = initialisation_of_sensors(fixed_arrival=True)
    simul_time, dt, emission_time_per_sensor, changed_period, t_0 = monitoring_of_sensor_emissions(division_cycling,
                                                                                                   event, sensor_names)
    plot_inter_arrival(dt, simul_time - t_0, emission_time_per_sensor, changed_period, t_0)"""

    #plot_duration_and_utility_function_of_M()


