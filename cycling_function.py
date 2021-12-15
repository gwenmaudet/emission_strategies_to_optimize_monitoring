import conf
import math

from simulation_and_metrics.abstractions_of_sensors import information_system

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
