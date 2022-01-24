import conf
import math

from simulation.abstractions_of_sensors import information_system


def remove_evt_from_active_sensors(elt_in_memory_that_will_die, type, simul_time, tau, leaf, branch):
    if len(leaf)==0 and len(branch)==0:
        return [],[]
    print("REMOOVING")
    print(leaf)
    print(branch)
    print(elt_in_memory_that_will_die)
    if type == "leaf":
        last_id_of_the_dead_sensor = int(elt_in_memory_that_will_die["id_tree"][len(elt_in_memory_that_will_die["id_tree"])-1])
        id_to_find = elt_in_memory_that_will_die["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)] + str(1 - last_id_of_the_dead_sensor)
        leaf,found_elt = find_elt_in_list_by_id_tree(id_to_find, leaf)
        found_elt["id_tree"] = found_elt["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)]
        branch.append(found_elt)
    else:
        last_id_of_the_dead_sensor = int(elt_in_memory_that_will_die["id_tree"][len(elt_in_memory_that_will_die["id_tree"])-1])
        id_to_find = elt_in_memory_that_will_die["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)] + str(1 - last_id_of_the_dead_sensor) + str(0)
        leaf, found_elt = find_elt_in_list_by_id_tree(id_to_find, leaf)
        if found_elt is not False:
            id_to_find_2 = elt_in_memory_that_will_die["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)] + str(1 - last_id_of_the_dead_sensor) + str(1)
            leaf, found_elt_2 = find_elt_in_list_by_id_tree(id_to_find_2, leaf)
            if found_elt["next_emission"] > found_elt_2["next_emission"]:
                found_elt,found_elt_2 = found_elt_2,found_elt
            found_elt["id_tree"] = elt_in_memory_that_will_die["id_tree"]
            if found_elt["next_emission"] < elt_in_memory_that_will_die["next_emission"]:
                found_elt["later_emission"] = elt_in_memory_that_will_die["next_emission"]
            else:
                found_elt["later_emission"] = elt_in_memory_that_will_die["next_emission"] + tau*math.pow(2,(len(elt_in_memory_that_will_die["id_tree"])))
            found_elt_2["id_tree"] = elt_in_memory_that_will_die["id_tree"][:(len(elt_in_memory_that_will_die["id_tree"]) - 1)] + str(1 - last_id_of_the_dead_sensor)
            branch.append(found_elt)
            branch.append(found_elt_2)
        else:
            leaf, elt = next_emmiting_sensor_according_to_type(leaf)
            """print("find the leaves that will take the relay")
            print(elt)
            print(leaf)"""
            leaf, leaf_elt = find_elt_in_list_by_id_tree(elt["id_tree"], leaf)
            last_id_of_the_dead_sensor = int(leaf_elt["id_tree"][len(leaf_elt["id_tree"])-1])
            id_to_find = leaf_elt["id_tree"][:(len(leaf_elt["id_tree"]) - 1)] + str(
                1 - last_id_of_the_dead_sensor)
            leaf, complementary_leaf = find_elt_in_list_by_id_tree(id_to_find, leaf)
            leaf_elt["id_tree"] = elt_in_memory_that_will_die["id_tree"]
            if leaf_elt["next_emission"] <elt_in_memory_that_will_die["next_emission"]:
                leaf_elt["later_emission"] = elt_in_memory_that_will_die["next_emission"]
            else:
                leaf_elt["later_emission"] = elt_in_memory_that_will_die["next_emission"] + tau*math.pow(2,(len(elt_in_memory_that_will_die["id_tree"])))
            complementary_leaf["id_tree"] = complementary_leaf["id_tree"][:(len(complementary_leaf["id_tree"]) - 1)]
            branch.append(complementary_leaf)
            branch.append(leaf_elt)
    return leaf, branch

def next_emmiting_sensor_according_to_type(leaf_or_branch):
    min_elt = leaf_or_branch[0]
    for elt in leaf_or_branch:
        if elt["next_emission"] < min_elt["next_emission"]:
            min_elt = elt
    return leaf_or_branch, min_elt


def find_elt_in_list_by_id_tree(id_to_find, leaf_or_branch):
    for i in range(len(leaf_or_branch)):
        if leaf_or_branch[i]["id_tree"] == id_to_find:
            found_elt = leaf_or_branch.pop(i)
            return leaf_or_branch, found_elt
    return leaf_or_branch, False


def find_elt_by_name(evt, leaf, branch):
    for i in range(len(leaf)):
        if leaf[i]["name"] == evt.name:
            leaf_elt = leaf.pop(i)
            return leaf, branch,leaf_elt,"leaf"
    for i in range(len(branch)):
        if branch[i]["name"] == evt.name:
            branch_elt = branch.pop(i)
            return leaf, branch,branch_elt,"branch"
    #print("troooppp bizaarrrre")





def add_new_sensor(evt, simul_time, tau, leaf,branch):
    branch, elt_that_will_be_a_leaf = next_emmiting_sensor_according_to_type(branch)
    branch, elt_that_will_be_a_leaf = find_elt_in_list_by_id_tree(elt_that_will_be_a_leaf["id_tree"], branch)
    height = len(elt_that_will_be_a_leaf["id_tree"])
    if "later_emission" in elt_that_will_be_a_leaf.keys():
        new_period = - simul_time + tau*math.pow(2,(height))
    else:
        new_period = elt_that_will_be_a_leaf["next_emission"] - simul_time + tau*math.pow(2,(height))
    new_elt = {"name": evt.name, "next_emission": elt_that_will_be_a_leaf["next_emission"] + tau*math.pow(2,(height)), "id_tree": elt_that_will_be_a_leaf["id_tree"]+"1"}
    elt_that_will_be_a_leaf["id_tree"] = elt_that_will_be_a_leaf["id_tree"] + "0"
    #elt_that_will_be_a_leaf["later_emission"] = elt_that_will_be_a_leaf["next_emission"] + tau*math.pow(2, (heignt+1))
    leaf.append(new_elt)
    leaf.append(elt_that_will_be_a_leaf)
    if len(branch) == 0:
        branch = leaf
        leaf = []
    return new_period, leaf, branch



def binary_tree(evt, simul_time, tau, M=0):
    global leaf
    global branch
    global sensor_view_list

    new_period = None
    if evt is None:
        leaf = []
        branch = []
        sensor_view_list = information_system()
        return new_period
    else:
        print("gu")
        print(evt.name)
        print(leaf)
        print(branch)
        if leaf ==[] and branch == []:
            sensor_view_list.update(evt, knowledge_on_battery=False)
            branch.append({"name": evt.name, "next_emission": simul_time + tau, "id_tree": ""})
        else:
            if not sensor_view_list.is_in(evt):
                sensor_view_list.update(evt, knowledge_on_battery=False)
                #print("he ho")
                #print(branch)
                new_period,leaf,branch = add_new_sensor(evt, simul_time, tau, leaf,branch)
            else:
                leaf, branch,elt_in_memory, type = find_elt_by_name(evt, leaf, branch)
                if "later_emission" not in elt_in_memory.keys():
                    if abs(round(tau * math.pow(2,len(elt_in_memory["id_tree"])) - evt.period,3)) == 0:
                        new_period = None
                        elt_in_memory["next_emission"] = simul_time + evt.period
                    else:
                        new_period = tau * math.pow(2,len(elt_in_memory["id_tree"]))
                        elt_in_memory["next_emission"] = simul_time + new_period
                else:
                    new_period = elt_in_memory["later_emission"] - simul_time
                    elt_in_memory.pop("later_emission", None)
                    elt_in_memory["next_emission"] = simul_time + new_period

                if (evt.can_emit_again and evt.can_change_period) or (evt.can_emit_again and new_period is None):
                    if type == "branch":
                        branch.append(elt_in_memory)
                    else:
                        leaf.append(elt_in_memory)
                    return new_period
                if evt.can_emit_again is False or (evt.can_emit_again and evt.can_change_period is False and new_period is not None):
                    if len(leaf) == 0:
                        leaf = branch
                        branch = []
                        type = "leaf"
                    leaf,branch = remove_evt_from_active_sensors(elt_in_memory, type, simul_time, tau, leaf,branch)
                    sensor_view_list.remove(evt)
        return new_period
