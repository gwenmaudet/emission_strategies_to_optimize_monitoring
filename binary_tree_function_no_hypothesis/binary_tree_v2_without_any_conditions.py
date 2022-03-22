import conf
import math

from simulation.abstractions_of_sensors import information_system


def remove_evt_from_active_sensors(elt_in_memory_that_will_die, type, simul_time, tau, children
                                   , parent):
    if len(children
           ) == 0 and len(parent) == 0:
        return [], []
    """print("REMOOVING")
    print(children
    )
    print(parent)
    print(elt_in_memory_that_will_die)"""
    if type == "children" \
               "":
        last_id_of_the_dead_sensor = int(
            elt_in_memory_that_will_die["id_tree"][len(elt_in_memory_that_will_die["id_tree"]) - 1])
        id_to_find = elt_in_memory_that_will_die["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)] + str(
            1 - last_id_of_the_dead_sensor)
        children, found_elt = get_elt_in_list_by_id_tree(id_to_find, children)
        found_elt["id_tree"] = found_elt["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)]
        parent.append(found_elt)
    else:

        children, elt = next_emmiting_sensor_according_to_type(children
                                                               )
        """print("find the leaves that will take the relay")
        print(elt)
        print(children
        )"""
        children, children_elt = get_elt_in_list_by_id_tree(elt["id_tree"], children)
        last_id_of_the_dead_sensor = int(children_elt["id_tree"][len(children_elt["id_tree"]) - 1])
        id_to_find = children_elt["id_tree"][:(len(children_elt["id_tree"]) - 1)] + str(
            1 - last_id_of_the_dead_sensor)
        children, complementary_children = get_elt_in_list_by_id_tree(id_to_find, children
                                                                      )
        children_elt["id_tree"] = elt_in_memory_that_will_die["id_tree"]
        complementary_children["id_tree"] = complementary_children["id_tree"][
                                            :(len(complementary_children["id_tree"]) - 1)]
        parent.append(complementary_children)
        parent.append(children_elt)
    return children, parent


def next_emmiting_sensor_according_to_type(children_or_parent):
    min_elt = children_or_parent[0]
    for elt in children_or_parent:
        if elt["next_emission"] < min_elt["next_emission"]:
            min_elt = elt
    return children_or_parent, min_elt


def get_elt_in_list_by_id_tree(id_to_find, children_or_parent):
    for i in range(len(children_or_parent)):
        if children_or_parent[i]["id_tree"] == id_to_find:
            found_elt = children_or_parent.pop(i)
            return children_or_parent, found_elt
    return children_or_parent, False


def find_elt_by_name(evt, children, parent):
    for i in range(len(children)):
        if children[i]["name"] == evt.name:
            children_elt = children \
                .pop(i)
            return children, parent, children_elt, "children"
    for i in range(len(parent)):
        if parent[i]["name"] == evt.name:
            parent_elt = parent.pop(i)
            return children, parent, parent_elt, "parent"
    # print("troooppp bizaarrrre")


def add_new_sensor(evt, simul_time, tau, children, parent):
    parent, elt_that_will_be_a_children = next_emmiting_sensor_according_to_type(parent)
    parent, elt_that_will_be_a_children = get_elt_in_list_by_id_tree(elt_that_will_be_a_children
                                                                     ["id_tree"], parent)
    new_period = tau * math.pow(2, len(elt_that_will_be_a_children["id_tree"]) + 1)
    new_elt = {"name": evt.name, "next_emission": simul_time + new_period,
               "id_tree": elt_that_will_be_a_children["id_tree"] + "1"}
    elt_that_will_be_a_children["id_tree"] = elt_that_will_be_a_children["id_tree"] + "0"
    # elt_that_will_be_a_children
    # ["later_emission"] = elt_that_will_be_a_children
    # ["next_emission"] + tau*math.pow(2, (heignt+1))
    children.append(new_elt)
    children.append(elt_that_will_be_a_children)
    if len(parent) == 0:
        parent = children
        children = []
    return new_period, children, parent


def binary_tree(evt, simul_time, tau, M=0, known_battery = False):
    global children

    global parent
    global sensor_view_list

    new_period = None
    if evt is None:
        children \
            = []
        parent = []
        sensor_view_list = information_system()
        return new_period
    else:
        """print("gu")
        print(evt.name)
        print(children)
        print(parent)"""
        if children \
                == [] and parent == []:
            sensor_view_list.update(evt, knowledge_on_battery=False)
            parent.append({"name": evt.name, "next_emission": simul_time + tau, "id_tree": ""})
        else:
            if not sensor_view_list.is_in(evt):
                sensor_view_list.update(evt, knowledge_on_battery=False)
                # print("he ho")
                # print(parent)
                new_period, children, parent = add_new_sensor(evt, simul_time, tau, children, parent)
            else:
                children, parent, elt_in_memory, type = find_elt_by_name(evt, children, parent)
                if abs(round(tau * math.pow(2, len(elt_in_memory["id_tree"])) - evt.period, 3)) == 0:
                    new_period = None
                    elt_in_memory["next_emission"] = simul_time + evt.period
                else:
                    new_period = tau * math.pow(2, len(elt_in_memory["id_tree"]))
                    elt_in_memory["next_emission"] = simul_time + new_period
                if evt.is_empty_value:
                    if len(children) == 0:
                        children = parent
                        parent = []
                        type = "children"
                    children, parent = remove_evt_from_active_sensors(elt_in_memory, type, simul_time, tau, children,
                                                                      parent)
                    sensor_view_list.remove(evt)
                else:
                    if type == "parent":
                        parent.append(elt_in_memory)
                    else:
                        children.append(elt_in_memory)
        return new_period
