import conf


def insert_event_in_event_list(elm, event):
    for i in range(len(event)):
        if event[i].wake_up > elm.wake_up:
            event.insert(i, elm)
            return event

    # last element
    event.append(elm)
    return event

"""
sensor class for initialisation of sensors, and management of their comportment
"""
class sensor:
    def __init__(self, period=0, name="sensor",
                 battery=conf.C, fst_wake_up=0, event=[]):
        self.expected_next_emission = None
        self.period = period
        self.battery = battery
        self.name = name
        self.is_out_of_scope = False
        self.wake_up = fst_wake_up
        self.fst_emission = self.wake_up
        event = insert_event_in_event_list(self, event)

    def sleep(self, simul_time, event):
        if self.battery < conf.c_e:  # when battery is empty
            return event
        # self.wake_up = simul_time + random.uniform(0, self.period)
        self.wake_up = simul_time + self.period
        event = insert_event_in_event_list(self, event)
        return event


    def set_period(self, period):
        self.period = period
        self.battery -= conf.c_r

    def draw(self):
        self.battery -= conf.c_e



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
