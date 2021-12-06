import conf

from abstractions_of_sensors import sensor_view, information_system


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
    end_of_devices.append(new_death)


def get_the_first_death_of_sensor():
    global end_of_devices
    for elt in end_of_devices:
        if elt[1] != None:
            sensor_death = elt[1]
            elt[1] = None
            return sensor_death


def cycling_over_M(evt, simul_time, tau, M):
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
                    new_period = tau
                else:
                    new_period = tau - (
                            simul_time - t_0) % tau + (
                                         sensor_view_list.length() - 1) * tau
            else:  # it would switch of just after the death of the next sensor, with a period of tau
                beggining_of_this_sensor = get_the_first_death_of_sensor()
                new_period = beggining_of_this_sensor - simul_time
        else:
            sensor_view_list.update(evt)
            if evt.period != min(sensor_view_list.length(), M) * tau:
                new_period = min(sensor_view_list.length(), M) * tau
                if evt.battery < conf.c_e + conf.c_r:
                    sensor_view_list.remove(evt)
            else:
                if evt.battery < conf.c_e:
                    sensor_view_list.remove(evt)

        # updating of end_of_device
        # sensor that have changed their period to M\tau or that didn't chang their period but will do at next emission : one change of period
        sensor_death = None
        if new_period == M * tau:
            sensor_death = simul_time + ((evt.battery - conf.c_r) // conf.c_e + 1) * tau * M
        elif new_period is None and evt.period != M * tau:
            sensor_death = simul_time + evt.period + (
                        (evt.battery - conf.c_r - conf.c_e) // conf.c_e + 1) * tau * M
        # sensor have changed it period but would need to change a second time to be really scheduled : 2 change of period
        elif new_period is not None and new_period != M * tau:
            sensor_death = simul_time + new_period + (
                        (evt.battery - 2 * conf.c_r - conf.c_e) // conf.c_e + 1) * tau * M
        # if sensor_death is None : pas de changement de periode et deja la période finale : M * \tau
        if sensor_death is not None:
            update_end_of_devices([evt.name, sensor_death])
    return new_period
