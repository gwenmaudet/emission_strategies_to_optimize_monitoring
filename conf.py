import math
"""
This file gathers the different parameters set for the simulations
"""

n = 300
C = 500
c_e = 1
c_r = 1


"""lambda_battery = 0.001
lambda_activation = 0.03
lambda_shut_down = 0.005
"""
lambda_battery = 0.001
lambda_activation = 0.1
lambda_shut_down = 0.05
#tau = 1 # reception every 5 minutes


T = 20 #spread factor of the utility function
#T = 20 #modified spred factor fo utility function

sample_step_for_diversity = T/100

activation_times = [i * 15 *math.pi for i in range(n)]


json_dir_for_db_f_M_tau = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\f_M_Tau_function_and_plots\\json_files\\data_base_for_choice_of_f.json'
json_dir_f_M_tau_for_comparison = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_periodic_recept\\json_files\\DB_f_M_tau_for_comparison.json'
json_dir_for_db_binary_tree_function_v1 = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_periodic_recept\\json_files\\DB_binray_tree_v1.json'
json_dir_for_db_binary_tree_v2_no_hypothesis = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis\\json_files\\DB_binary_tree_V2_no_hypothesis.json'
"""
Constraint to find the fitting tau for the research for the optimised solution
"""