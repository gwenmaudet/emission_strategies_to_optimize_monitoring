# Emission Strategies to Optimize Monitoring

## General information
This project includes all the code used for the creation of the figures, as well as for the simulations of : "Emission Strategies to Optimize Monitoring". 

![](https://github.com/gwenmaudet/emission_strategies_to_optimize_monitoring/blob/master/images/Logo_IMT_Atlantique.png)


## Start
All the code is writen in Python. The packages used are :

    math, matplotlib, numpy, random, statistics
    
## Functions, modules and their use
### conf
All the parameters fixed in the paper are represented in this file.

### simulation
The module named 'simulation" is a generic module to simulate emissions of sensors, according to an period update function (here the function is the file "f_M_tau_function_and_plots/f_M_tau.py"), and provide the performance metrics.

### f_M_tau_function_and_plots
Represent the function f_M_tau and all the function helping for the plots of the refered paper.
#### Use of the toy example
In ordre to simulate the type of examples presented in the definitions of the period update function.

Run the file :
```
using_of_Cycle_M_and_vizualisation/toy_example.py
```
You will be asked for the parameters to be set, and the function will display an illustration of the emissions.
#### Filling up the data base
You will file the data-base named "json_files/data_base_for_choice_of_f.json". It is already in the reppository. Otherwise, you can run :
```
using_of_Cycle_M_and_vizualisation/filling_json_db.py
```
By default, it initialise the json file (function "initialisation_of_json_file(json_to_fill)"), then fill it with the metrics of time of monitoring and diversity penalty for functions with parameters of M and tau : 
```
M_list = [1, 2, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 125, 150, 200]
tau_list = [0.05 + 0.05 * i for i in range(250)]
```

#### Vizualisation of the data base 
By default, it will show the data base following the order of the figures shown in the paper, from the part named "simulation".


### binary_tree_function_periodic_recept & binary_tree_function_no_hypothesis
These modules are used for further publications.

## Authors
Gwen MAUDET, IMT Atlantique, IRISA, OCIF

Mireille BATTON-HUBERT, EMSE

Patrick MAILLE, IMT Atlantique, IRISA, Dyonisos

Laurent TOUTAIN, IMT Atlantique, IRISA, OCIF


