

## Quantum annealing
In ```parallel_machines```  the problems of scheduling on parallel machines are solved via QUBO and quantum (or simulated) annealing

## Arguments:

--case - default ```1``` - problem cases ```1``` to ```4``` determining various scheduling problems in increasing size
--runs  - default ```4``` - number of runs on quantum or simulated device
--real - by default: ```False``` - use real annealing if true or simullated one if false
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


```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --show_all

```

to read file with data only:

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --no_compute

```



### Real annealing

```
python3 solve_problems.py --case 1 --no_runs 4 --psum 100 --ppair 100 --real --at 1.

```

