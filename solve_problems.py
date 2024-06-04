import pickle
import argparse
import numpy as np

from parallel_machines import Job, Machine, Problem
from parallel_machines import Variables, Implement_QUBO
from parallel_machines import solve_on_DWave, check_solutions



def case1():
    """ tmax = 8  #m = 2, #j = 5"""

    P = Problem(tmax = 8)
    machines_list = (Machine(1),Machine(2))
    P.add_machines(machines_list)

    P.machine_occupation(1, occupied_till=4)
        
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                Job(id=2, release_t=2, process_t=2, priority=0.2),
                Job(id=3, release_t=1, process_t=4, priority=0.8),
                Job(id=4, release_t=5, process_t=2, priority=0.8),
                Job(id=5, release_t=0, process_t=5, priority=0.8),
                )
            
    P.add_jobs(jobs_list)

    return P


def case2():
    """ tmax = 8  #m = 2, #j = 6"""

    P = Problem(tmax = 8)
    machines_list = (Machine(1),Machine(2))
    P.add_machines(machines_list)

    P.machine_occupation(1, occupied_till=2)
        
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                Job(id=2, release_t=2, process_t=2, priority=0.2),
                Job(id=3, release_t=1, process_t=4, priority=0.8),
                Job(id=4, release_t=5, process_t=2, priority=0.8),
                Job(id=5, release_t=0, process_t=5, priority=0.8),
                Job(id=6, release_t=2, process_t=2, priority=0.8),
                )
            
    P.add_jobs(jobs_list)

    return P


def case3():
    """ tmax = 12  #m = 3, #j = 10"""
    
    P = Problem(tmax = 12)
    machines_list = (Machine(1),Machine(2), Machine(3))
    P.add_machines(machines_list)

    P.machine_occupation(1, occupied_till=4)
    P.machine_occupation(3, occupied_till=1)
        
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                Job(id=2, release_t=2, process_t=2, priority=0.2),
                Job(id=3, release_t=1, process_t=4, priority=0.2),
                Job(id=4, release_t=5, process_t=2, priority=0.2),
                Job(id=5, release_t=0, process_t=5, priority=0.2),
                Job(id=6, release_t=0, process_t=4, priority=0.8),
                Job(id=7, release_t=1, process_t=3, priority=0.8),
                Job(id=8, release_t=2, process_t=3, priority=0.8),
                Job(id=9, release_t=5, process_t=2, priority=0.8),
                Job(id=10, release_t=0, process_t=6, priority=0.8),
                )
            
    P.add_jobs(jobs_list)

    return P

def case4():
    """ tmax = 20  #m = 3, #j = 12"""
    P = Problem(tmax = 20)
    machines_list = (Machine(1),Machine(2), Machine(3))
    P.add_machines(machines_list)

    P.machine_occupation(1, occupied_till=4)
    P.machine_occupation(3, occupied_till=1)
        
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                Job(id=2, release_t=2, process_t=2, priority=0.2),
                Job(id=3, release_t=1, process_t=4, priority=0.2),
                Job(id=4, release_t=5, process_t=2, priority=0.2),
                Job(id=5, release_t=0, process_t=5, priority=0.2),
                Job(id=6, release_t=0, process_t=4, priority=0.8),
                Job(id=7, release_t=1, process_t=3, priority=0.8),
                Job(id=8, release_t=2, process_t=3, priority=0.8),
                Job(id=9, release_t=5, process_t=2, priority=0.8),
                Job(id=10, release_t=0, process_t=6, priority=0.8),
                Job(id=11, release_t=1, process_t=8, priority=0.8),
                Job(id=12, release_t=1, process_t=7, priority=0.8),
                )
            
    P.add_jobs(jobs_list)

    return P



if __name__ == "__main__":


    parser = argparse.ArgumentParser("mode of problem solving: computation /  output analysis")

    parser.add_argument(
        "--case",
        type=int,
        help="problem case",
        default=1,
    )

    parser.add_argument(
        "--real",
        help="if True simulated annealing (via DWave software), if False real annealing",
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    parser.add_argument(
        "--no_compute",
        help="if True computations are not performed but only data are read from file",
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    parser.add_argument(
        "--at",
        type=float,
        help="annealing time for real device",
        default=1.,
    )

    parser.add_argument(
        "--no_runs",
        type=int,
        help="number of runs on the simulated or real device",
        default=4,
    )

    parser.add_argument(
        "--psum",
        type=float,
        help="sum penalty",
        default=100.,
    )

    parser.add_argument(
        "--ppair",
        type=float,
        help="pair penalty",
        default=100.,
    )

    parser.add_argument(
        "--show_all",
        help="if True show all solutions, else show only feasible",
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    parser.add_argument(
        "--exp",
        help="if True uses exponential objective",
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()
        
    if args.case == 1:
        P = case1()

    if args.case == 2:
        P = case2()

    if args.case == 3:
        P = case3()

    if args.case == 4:
        P = case4()
     
            
    Vars = Variables(P)
    print("QUBO size = ", Vars.size)
    

    if args.exp:
        Q = Implement_QUBO(psum=args.psum, ppair=args.ppair, objective=lambda tau : np.exp(tau))
    else:
        Q = Implement_QUBO(psum=args.psum, ppair=args.ppair, objective=lambda tau : tau**2)
    
    Q.make_QUBO(Vars, P)

    
    file = f"parallel_machines/solutions/sim_case{args.case}_psum{round(args.psum)}_ppair{round(args.ppair)}.pkl"
    if args.exp:
        file = file.replace("case", "exp_case")

    if args.real:
        file = file.replace("sim", f"real_at{args.at}")

    if not args.no_compute:
        solutions = solve_on_DWave(Q.qubo_terms, no_runs = args.no_runs, real= args.real, at = args.at)

        with open(file, 'wb') as fp:
            pickle.dump(solutions.record, fp)

    with open(file, 'rb') as fp:
        sol = pickle.load(fp)

    check_solutions(Vars, P, Q, sol, print_not_feasible = args.show_all)


        
