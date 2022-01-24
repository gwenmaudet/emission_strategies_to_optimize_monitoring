import math
"""
This file gathers the different parameters set for the simulations
"""

n = 200
C = 500
c_e = 1
c_r = 1
#tau = 1 # reception every 5 minutes


T = 15 #spread factor of the utility function
#T = 20 #modified spred factor fo utility function

activation_times = [i * 15 *math.pi for i in range(n)]


json_dir_for_db_f_M_tau = "json_files/data_base_for_choice_of_f.json"
json_dir_for_db_binary_tree_function = "json_files/DB_binray_tree.json"

"""
Constraint to find the fitting tau for the research for the optimised solution
"""
dif_tau = 0.01