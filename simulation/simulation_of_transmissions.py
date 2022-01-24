import logging

import conf
from simulation.abstractions_of_sensors import sensor, sensor_view



"""
This file represents the envelope of the simulation.

First, the initialization function of the sensors, with respect to their activation time.
Then, the simulation function of the sensors behavior, using the "event" object,
 which for any 'simul_time' instant, is an ordered list of sensors emission instant.
"""


def initialisation_of_sensors(activation_times, battery=conf.C):
    event = []
    names = []
    for i in range(len(activation_times)):
        t_i = activation_times[i]
        s = sensor(name="sensor number " + str(i), fst_wake_up=t_i, event=event, battery=battery)
        names.append(s.name)

    return names, event


"""
This file returns :
Return False if a new sensor emmit after all the sensor are dead : means that the inter arrival is more than tau

simul_time : the time instant of the last emission
dt : the list of the time difference beween 2 consecutives emissions
emission_time_per_sensor : dictionary of sensor name and their emision time = {sensor_name_1:[emission_time1,emission_time2],
                                                                                ,sensor_name_1:[emission_time1,..]..}
changed_period :  dictionary of sensors and their period change time  = {sensor_name_1:[changing_time1,changing_time2],
                                                                                ,sensor_name_1:[changing_time1,..]..}
t_0 : initial emission
"""


def monitoring_of_sensor_emissions(management_function, tau,  event, sensor_names, M=None, known_battery=True):
    nb_of_changes = 0
    simul_time = 0
    dt = []
    emission_time_per_sensor = {}
    changed_period = {}
    t_0 = None
    for name in sensor_names:
        emission_time_per_sensor[name] = []
        changed_period[name] = []
    management_function(None, 0, tau, M)
    while len(event) != 0:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)

        if t_0 is not None:
            delta_t = evt.wake_up - simul_time
            dt.append(delta_t)
            """if round(delta_t, 3) > round(tau, 3):
                logging.info("the result from the function with parameters M="
                             + str(M) + " and tau=" + str(tau) + " because the monitoring ends before all the sensors get included")
                #return False"""
        evt.draw()
        simul_time = evt.wake_up
        if t_0 is None:
            t_0 = simul_time
        if known_battery is False:
            if evt.battery >= conf.c_e + conf.c_r:
                can_change_period = True
                can_emit_again = True
            elif evt.battery >= conf.c_e:
                can_emit_again = True
                can_change_period = False
            else:
                can_emit_again = False
                can_change_period = False
        else:
            can_emit_again = None
            can_change_period = None
        view = sensor_view(evt, battery=known_battery, can_emit_again=can_emit_again, can_change_period=can_change_period)
        new_period = management_function(view, simul_time, tau, M)  ######## use of the management function. return the value if it has changed, None otherwise
        emission_time_per_sensor[evt.name].append(simul_time)
        if new_period is not None and evt.battery >= conf.c_r:
            evt.set_period(new_period)
            changed_period[evt.name].append(simul_time)
            nb_of_changes += 1
        evt.expected_next_emission = simul_time + evt.period
        event = evt.sleep(simul_time, event)
    return simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes


if __name__ == '__main__':
    A = 0
