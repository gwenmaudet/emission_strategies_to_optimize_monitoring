import math
"""
This file gathers the different parameters set for the simulations
"""

n = 200
C = 1000
c_e = 1
c_r = 1
#tau = 1 # reception every 5 minutes


T = 5 #spread factor of the utility function
#T = 20 #modified spred factor fo utility function

activation_times = [i * (90+math.pi) for i in range(n)]


json_dir_for_db = "json_files/data_base_for_choice_of_f.json"
json_dir_for_db_with_modified_T = "json_files/data_base_for_choice_of_f_with_modified_T.json"
json_dir_for_db_with_modified_activation_times = "json_files/data_base_for_choice_of_f_with_modified_activation_times.json"

json_dir_for_research_of_optimum = "json_files/research_of_optimum.json"


"""
Constraint to find the fitting tau for the research for the optimised solution
"""
dif_tau = 0.01