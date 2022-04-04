import logging

import conf
from simulation.abstractions_of_sensors import sensor, sensor_view



"""
This file represents the envelope of the simulation.

First, the initialization function of the sensors, with respect to their activation time.
Then, the simulation function of the sensors behavior, using the "event" object,
 which for any 'simul_time' instant, is an ordered list of sensors emission instant.
"""


def initialisation_of_sensors(activation_times, battery=conf.C, shut_down=None, battery_type = 0):
    event = []
    names = []
    for i in range(len(activation_times)):
        t_i = activation_times[i]
        if shut_down is None:
            s = sensor(name="sensor number " + str(i), fst_wake_up=t_i, event=event, battery=battery, shut_down=10000000000000000000000000000, battery_type=battery_type)
        else:
            s = sensor(name="sensor number " + str(i), fst_wake_up=t_i, event=event, battery=battery,
                       shut_down=shut_down[i], battery_type=battery_type)
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


def monitoring_of_sensor_emissions(management_function, tau,  event, sensor_names, M=None, known_battery=True,beggining_time=0, stopping_time = 100000000000000000000000000000000000000000):
    nb_of_changes = 0
    simul_time = 0
    dt = []
    emission_time_per_sensor = {}
    changed_period = {}
    nb_of_change_ids = 0
    t_0 = 0
    for name in sensor_names:
        emission_time_per_sensor[name] = []
        changed_period[name] = []
    management_function(None, 0, tau, M)
    while len(event) != 0 and (simul_time - t_0) < stopping_time:
        evt = event.pop(0)
        assert (evt.wake_up >= simul_time)
        if t_0 == 0:
            simul_time = evt.wake_up
            t_0 = simul_time
        else:
            if evt.is_empty_value is False:
                delta_t = evt.wake_up - simul_time

                simul_time = evt.wake_up
                if simul_time >beggining_time:
                    dt.append(delta_t)
            """if round(delta_t, 3) > round(tau, 3):
                logging.info("the result from the function with parameters M="
                             + str(M) + " and tau=" + str(tau) + " because the monitoring ends before all the sensors get included")
                #return False"""
        evt.draw()


        view = sensor_view(evt, battery=known_battery)
        new_period, change_id = management_function(view, evt.wake_up, tau, M, known_battery=known_battery)  ######## use of the management function. return the value if it has changed, None otherwise
        nb_of_change_ids += change_id
        if evt.is_empty_value is False:
            if new_period is not None and new_period != evt.period:
                evt.set_period(new_period)
                nb_of_changes += 1
                if simul_time > beggining_time:
                    changed_period[evt.name].append(evt.wake_up)
            evt.expected_next_emission = evt.wake_up + evt.period
            if simul_time > beggining_time:
                emission_time_per_sensor[evt.name].append(evt.wake_up)
        event = evt.sleep(evt.wake_up, event)

    return simul_time, dt, emission_time_per_sensor, changed_period, t_0, nb_of_changes, nb_of_change_ids


if __name__ == '__main__':
    A = 0
