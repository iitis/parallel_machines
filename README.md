

Quantum annealing
In ```parallel_machines```  the problems of scheduling on parallel machines are solved via QUBO and quantum (or simulated) annealing

Arguments:

--case - default ```1``` - problem cases ```1``` to ```4``` determining various scheduling problems in increasing size
--runs  - defalut ```4``` - number of runs on quantum or simulated device
--sim - by default: True - use simulated or real annealing,
--show_all -by default: False - show also not feasible solutions
--psum  - by default 100 - sum peanlty
--ppair - by defaault 100 - pair penalty


Example use 

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100

```


```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --show_all 1

```

