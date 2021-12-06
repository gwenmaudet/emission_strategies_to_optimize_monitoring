import conf
import diversity
from abstractions_of_sensors import sensor, sensor_view
import M_cycling_function

def initialisation_of_sensors(activation_times):
    event = []
    names = []
    for i in range(len(activation_times)):
        t_i = activation_times[i]
        s = sensor(name="sensor number "+str(i), fst_wake_up=t_i, event=event)
        names.append(s.name)

    return names, event

def monitoring_of_sensor_emissions(management_function, tau, M, event, sensor_names):
    # global sensor_view_list
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
        delta_t = evt.wake_up - simul_time
        if t_0 is None:
            t_0 = simul_time
        evt.draw()
        simul_time = evt.wake_up
        view = sensor_view(evt)
        new_period = management_function(view, simul_time, tau, M)  ######## use of the management function
        dt.append(delta_t)
        emission_time_per_sensor[evt.name].append(simul_time)
        if new_period is not None and evt.battery >= conf.c_r:
            evt.set_period(new_period)
            changed_period[evt.name].append(simul_time)
        evt.expected_next_emission = simul_time + evt.period
        event = evt.sleep(simul_time, event)
            # if bool is False:
            #    sensor_view_list.remove(evt)
        # else:
        #    sensor_view_list.remove(evt)
    return simul_time, dt, emission_time_per_sensor, changed_period, t_0







if __name__ == '__main__':
    A = 0

