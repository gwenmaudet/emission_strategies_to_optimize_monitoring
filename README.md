# Emission Strategies to Optimize Monitoring

## General information
This project includes all the code used for the creation of the figures, as well as for the simulations of : "Emission Strategies to Optimize Monitoring". 

![](https://github.com/gwenmaudet/emission_strategies_to_optimize_monitoring/blob/master/images/Logo_IMT_Atlantique.png)


## Start
All the code is writen in Python. The packages used are :

    math, matplotlib, numpy, random, statistics
    
## Functions, modules and their use
### simulation_and_metrics
The module named 'simulation_and_metrics" is a generic module to simulate emissions of sensors, according to an period update function (file "using_of_Cycle_M_and_vizualisation/M_cycling_function.py"), and provide the performance metrics.

### Parameters
All the parameters fixed in the paper are represented in the file 
```
conf.py
```

### Use of the toy example
In ordre to simulate the type of examples presented in the definitions of the period update function.


Run the file :
```
using_of_Cycle_M_and_vizualisation/toy_example.py
```

### Filling up the data base
You will file the data-base named "json_files/data_base_for_choice_of_f.json". It is already in the reppository. Otherwise, you can run :
```
using_of_Cycle_M_and_vizualisation/filling_json_db.py
```
By default, it initialise the json file (function "initialisation_of_json_file(json_to_fill)"), then fill it with the metrics of time of monitoring and diversity penalty for functions with parameters of M and tau : 
```
M_list = [1, 2, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 125, 150, 200]
tau_list = [0.1 + 0.1 * i for i in range(120)]
```

### Vizualisation of the data base 
By default, it will show the data base following the order of the figures shown in the paper, from the part named "simulation".




## Authors
Mireille BATTON-HUBERT, EMSE

Patrick MAILLE, INRIA, IRISA, Dyonisos

Gwen MAUDET, IMT Atlantique, IRISA, OCIF

Laurent TOUTAIN, IMT Atlantique, IRISA, OCIF


