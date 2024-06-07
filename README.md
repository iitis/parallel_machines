

## Quantum annealing
In ```parallel_machines```  the problems of scheduling on parallel machines are solved via QUBO and quantum (or simulated) annealing

## Arguments:

--case - default ```1``` - problem cases ```1``` to ```4``` determining various scheduling problems in increasing size
--runs  - default ```1``` - number of runs on quantum or simulated device
--real - by default: ```False``` - use real annealing if ```True``` or simullated one if ```False```
--real - by default: ```False``` - use hybrid bqm solver if ```True```
--at - by default ```1.```, annealing time [in \mu s] for real annelaing
--show_all -by default: ```False``` - show also not feasible solutions
--psum  - by default ```100.``` - sum penalty
--ppair - by default ```100.``` - pair penalty
--no_compute by default ```False```, if ```True``` computaiton is not performed


## Example use 

### Simulated annealing

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100

```

#### show all results also these not feasible

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --show_all

```

#### read file with data only:

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --no_compute

```


#### expotencial objective

```
python3 solve_problems.py --case 1 --no_runs 1000 --psum 10000 --ppair 10000 --exp

```



### Real annealing

```
python3 solve_problems.py --case 1 --no_runs 4 --psum 100 --ppair 100 --real --at 1.

```


### Hybrid solver

```
python3 solve_problems.py --case 1 --psum 100 --ppair 100 --hyb.

```

