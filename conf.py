import math
"""
This file gathers the different parameters set for the simulations
"""

n = 200
C = 500
c_e = 1
c_r = 1
#tau = 1 # reception every 5 minutes


T = 5 #spread factor of the utility function

activation_times = [i * (50+math.pi) for i in range(n)]


json_dir_for_db = "json_files/data_base_for_choice_of_f.json"
json_dir_for_research_of_optimum = "json_files/research_of_optimum.json"


"""
Constraint to find the fitting tau for the research for the optimised solution
"""
dif_tau = 0.05