import math
"""
This file gathers the different parameters set for the simulations
"""

n = 100

c_e = 1
c_r = 1

"""
lambda_battery = 0.001
lambda_activation = 0.03
lambda_shut_down = 0.005
"""
gamma = 0.01
lambda_ = 0.1
mu = 0.001
C = 1 / gamma
#tau = 1 # reception every 5 minutes

beggining_time = 10000
stopping_time = 100000


T = 20 #spread factor of the utility function
sample_step = T/50
threshold_delta_t = T*10


#T = 20 #modified spred factor fo utility function

sample_step_for_diversity = T/100

activation_times = [i * 15 *math.pi for i in range(n)]


json_dir_binary_nb_of_sensors = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis/json_files/DB_binary_nb_of_sensors.json'
json_dir_binary_nb_of_emissions = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis/json_files/DB_binary_nb_of_emissions.json'
json_dir_binary_nb_of_perturbations = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis/json_files/DB_binary_nb_of_perturbations.json'
json_dir_binary_nb_of_change_ids = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis/json_files/DB_binary_nb_of_change_ids.json'

json_dir_binary_diversity_and_std = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_no_hypothesis/json_files/DB_binary_diversity_and_std.json'



json_dir_f_M_tau_nb_of_sensors = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\f_M_Tau/json_files\\DB_f_M_tau_nb_of_sensors.json'
json_dir_f_M_tau_nb_of_emissions = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\f_M_Tau/json_files\\DB_f_M_tau_nb_of_emissions.json'
json_dir_f_M_tau_nb_of_perturbations = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\f_M_Tau/json_files\\DB_f_M_tau_nb_of_perturbations.json'
json_dir_f_M_tau_diversity_and_std = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\f_M_Tau/json_files\\DB_f_M_tau_diversity_and_std.json'



json_dir_for_db_f_M_tau = 'f_M_Tau/json_files\\data_base_for_choice_of_f.json'


json_dir_f_M_tau_for_comparison = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_periodic_recept\\json_files\\DB_f_M_tau_for_comparison.json'
json_dir_for_db_binary_tree_function_v1 = 'C:\\Users\\Gwen Maudet\\PycharmProjects\\emission_strategies_to_optimize_monitoring\\binary_tree_function_periodic_recept\\json_files\\DB_binray_tree_v1.json'


json_dir_for_db_binary_tree_v2_no_hypothesis = 'binary_tree_function_no_hypothesis/json_files\\DB_binary_tree_V2_no_hypothesis.json'
"""
Constraint to find the fitting tau for the research for the optimised solution
"""