

## Quantum annealing
In ```parallel_machines```  the problems of scheduling on parallel machines are solved via QUBO and quantum (or simulated) annealing

## Arguments:

- --case - default ```1``` - problem cases ```1``` to ```5``` determining various scheduling problems in increasing size
- --runs  - default ```1``` - number of runs on quantum or simulated device
- --real - by default: ```False``` - use real annealing if ```True``` or simulated one if ```False```
- --hyb - by default: ```False``` - use hybrid bqm solver if ```True```
- --at - by default ```1.```, annealing time [in \mu s] for real annealing
- --plot_item - by default ```0```, number of item to be plotted (items are feasible and sorted due to objective)
- --show_all -by default: ```False``` - show also not feasible solutions
- --psum  - by default ```100.``` - sum penalty
- --ppair - by default ```100.``` - pair penalty
- --no_compute by default ```False```, if ```True``` computation is not performed


## Example use 

### Simulated annealing

```
python3 solve_problems.py --case 1 --no_runs 100 --psum 100 --ppair 50

```

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100

```

#### Show all results also these that are not feasible

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --show_all

```

#### Read file with data only:

```
python3 solve_problems.py --case 4 --no_runs 25 --psum 200 --ppair 100 --no_compute

```

#### Plot chart of ```--plot_item``` realisation


```
python3 solve_problems.py --case 1 --no_runs 25 --psum 200 --ppair 100 --plot_item 1

```



#### Exponential objective

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

