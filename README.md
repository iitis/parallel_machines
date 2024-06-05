

## Quantum annealing
In ```parallel_machines```  the problems of scheduling on parallel machines are solved via QUBO and quantum (or simulated) annealing

## Arguments:

- --case - default ```1``` - problem cases ```1``` to ```4``` determining various scheduling problems in increasing size
- --runs  - default ```4``` - number of runs on quantum or simulated device
- --real - by default: ```False``` - use real annealing if true or simullated one if false
- --at - by default ```1.```, annealing time [in \mu s] for real annelaing
- --show_all -by default: ```False``` - show also not feasible solutions
- --psum  - by default ```100.``` - sum penalty
- --ppair - by default ```100.``` - pair penalty
- --no_compute by default ```False```, if ```True``` computaiton is not performed
- --exp -by default: ```False``` - use expotnecial objective


## Example use 

### Simulated annealing

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100

```

#### show all results also these are not feasible

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --show_all

```

#### Read file with data only:

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --no_compute

```


#### Exponential objective

```
python3 solve_problems.py --case 1 --no_runs 100 --psum 1000 --ppair 1000 --exp

```



### Real annealing

```
python3 solve_problems.py --case 1 --no_runs 4 --psum 100 --ppair 100 --real --at 1.

```

