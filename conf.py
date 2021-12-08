import math
"""
This file gathers the different parameters set for the simulations
"""

n = 200
C = 200
c_e = 1
c_r = 1
#tau = 1 # reception every 5 minutes


T = 10 #spread factor of the utility function

activation_times = [i * (20+math.pi) for i in range(n)]


json_dir = "json_storage.json"



