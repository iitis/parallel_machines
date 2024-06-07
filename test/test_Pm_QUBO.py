import pytest

from parallel_machines import Job, Machine, Problem
from parallel_machines import Variables, Implement_QUBO
from parallel_machines import solve_on_DWave, check_solutions


def test_jobs_machines_variables():

    J = Job(id=1, release_t=0, process_t=3, priority=0.4)
    assert J.priority == 0.4

    P = Problem(tmax = 3)
    machines_list = (Machine(1),Machine(2))
    P.add_machines(machines_list)
    assert P.machines[1].id == 1
    assert P.machines[2].id == 2
    P.machine_occupation(1, occupied_till=1)
    assert P.machines[1].occupied_till == 1
    assert P.machines[2].occupied_till == 0

    assert P.no_machines == 2

    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                    Job(id=2, release_t=2, process_t=2, priority=0.8)
                    )
        
    P.add_jobs(jobs_list)
    assert P.no_jobs == 2
    Vars = Variables(P)

    assert Vars.q_vars[1].m == 1
    assert Vars.q_vars[1].j == 1
    assert Vars.q_vars[1].t == 1
    assert Vars.q_vars[2].t == 2
    assert Vars.q_vars[3].t == 3

    assert Vars.q_vars[4].m == 1
    assert Vars.q_vars[4].j == 2
    assert Vars.q_vars[4].t == 2
    assert Vars.q_vars[5].t == 3

    assert Vars.size == 11

    assert Vars.get_k_and_varval(t_in=3,m_in=1,j_in=2) == (5, -1)


def test_qubo_implementation():


    P = Problem(tmax = 3)
    machines_list = (Machine(1),Machine(2))
    P.add_machines(machines_list)
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                    Job(id=2, release_t=2, process_t=2, priority=0.8)
                    )
        
    P.add_jobs(jobs_list)
    P.machine_occupation(1, occupied_till=1)

    Vars = Variables(P)

    Q = Implement_QUBO(psum=10, ppair=10, objective=lambda tau : tau**2)

    Q.objective(Vars, P)


    assert Vars.multiindices == {1: (1, 1, 1), 2: (2, 1, 1), 3: (3, 1, 1), 4: (2, 1, 2), 5: (3, 1, 2), 
                        6: (0, 2, 1), 7: (1, 2, 1), 8: (2, 2, 1), 9: (3, 2, 1), 10: (2, 2, 2), 11: (3, 2, 2)}
        
    assert Q.qubo_terms == {(1,1): 0.8, (2,2): 1.8, (3,3): 3.2, (4,4): 3.2, (5,5): 7.2, 
                                (6,6): 0.2, (7,7): 0.8, (8,8): 1.8, (9,9): 3.2, (10,10): 3.2, (11,11): 7.2}

    inds_check1, inds_check2 = Q.sum_constraint(Vars)
    assert list(inds_check1.values()) == [(1, 1, 1), (2, 1, 1), (3, 1, 1), (2, 1, 2), (3, 1, 2), 
                                            (0, 2, 1), (1, 2, 1), (2, 2, 1), (3, 2, 1), (2, 2, 2), (3, 2, 2)]
        
    v = [[(1, 1, 1), (2, 1, 1)], [(1, 1, 1), (3, 1, 1)], [(1, 1, 1), (0, 2, 1)], [(1, 1, 1), (1, 2, 1)], [(1, 1, 1), (2, 2, 1)], [(1, 1, 1), (3, 2, 1)], 
    [(2, 1, 1), (1, 1, 1)], [(2, 1, 1), (3, 1, 1)], [(2, 1, 1), (0, 2, 1)], [(2, 1, 1), (1, 2, 1)], [(2, 1, 1), (2, 2, 1)], [(2, 1, 1), (3, 2, 1)], 
    [(3, 1, 1), (1, 1, 1)], [(3, 1, 1), (2, 1, 1)], [(3, 1, 1), (0, 2, 1)], [(3, 1, 1), (1, 2, 1)], [(3, 1, 1), (2, 2, 1)], [(3, 1, 1), (3, 2, 1)], 
    [(2, 1, 2), (3, 1, 2)], [(2, 1, 2), (2, 2, 2)], [(2, 1, 2), (3, 2, 2)], 
    [(3, 1, 2), (2, 1, 2)], [(3, 1, 2), (2, 2, 2)], [(3, 1, 2), (3, 2, 2)], 
    [(0, 2, 1), (1, 1, 1)], [(0, 2, 1), (2, 1, 1)], [(0, 2, 1), (3, 1, 1)], [(0, 2, 1), (1, 2, 1)], [(0, 2, 1), (2, 2, 1)], [(0, 2, 1), (3, 2, 1)], 
    [(1, 2, 1), (1, 1, 1)], [(1, 2, 1), (2, 1, 1)], [(1, 2, 1), (3, 1, 1)], [(1, 2, 1), (0, 2, 1)], [(1, 2, 1), (2, 2, 1)], [(1, 2, 1), (3, 2, 1)], 
    [(2, 2, 1), (1, 1, 1)], [(2, 2, 1), (2, 1, 1)], [(2, 2, 1), (3, 1, 1)], [(2, 2, 1), (0, 2, 1)], [(2, 2, 1), (1, 2, 1)], [(2, 2, 1), (3, 2, 1)], 
    [(3, 2, 1), (1, 1, 1)], [(3, 2, 1), (2, 1, 1)], [(3, 2, 1), (3, 1, 1)], [(3, 2, 1), (0, 2, 1)], [(3, 2, 1), (1, 2, 1)], [(3, 2, 1), (2, 2, 1)], 
    [(2, 2, 2), (2, 1, 2)], [(2, 2, 2), (3, 1, 2)], [(2, 2, 2), (3, 2, 2)], 
    [(3, 2, 2), (2, 1, 2)], [(3, 2, 2), (3, 1, 2)], [(3, 2, 2), (2, 2, 2)]]
        
    assert list(inds_check2.values()) == v


    inds_check = Q.pair_constraint(Vars, P)

    assert list(inds_check.values()) == [[(2, 1, 1), (2, 1, 2)], [(3, 1, 1), (2, 1, 2)], [(3, 1, 1), (3, 1, 2)], # m=1
                                        [(2, 1, 2), (2, 1, 1)], [(2, 1, 2), (3, 1, 1)], [(3, 1, 2), (3, 1, 1)], # m=1
                                        [(2, 2, 1), (2, 2, 2)], [(3, 2, 1), (2, 2, 2)], [(3, 2, 1), (3, 2, 2)], # m=2
                                        [(2, 2, 2), (2, 2, 1)], [(2, 2, 2), (3, 2, 1)], [(3, 2, 2), (3, 2, 1)]] # m=2
    

def test_solutions():

    P = Problem(tmax = 3)
    machines_list = (Machine(1),Machine(2))
    P.add_machines(machines_list)
    jobs_list = (Job(id=1, release_t=0, process_t=1, priority=0.2),
                    Job(id=2, release_t=2, process_t=2, priority=0.8)
                    )
        
    P.add_jobs(jobs_list)
    P.machine_occupation(1, occupied_till=1)

    Vars = Variables(P)

    Q = Implement_QUBO(psum=10, ppair=10, objective=lambda tau : tau**2)

    Q.make_QUBO(Vars, P)


    var_list = [0,0,0,1,0,1,0,0,0,0,0]
    Vars.set_values(var_list)
    obj = Q.compute_objective(Vars, P)
    assert obj == pytest.approx(3.4)
    assert Q.chech_feasibility_pair_constraint(Vars, P) == 0
    broken_constraints = Q.check_feasibility_sum_constraint(Vars, P)
    assert broken_constraints == 0
        

    var_list = [0,0,0,0,0,1,0,0,0,1,0]
    Vars.set_values(var_list)
    obj = Q.compute_objective(Vars, P)
    assert obj == pytest.approx(3.4)
    assert Q.chech_feasibility_pair_constraint(Vars, P) == 0
    broken_constraints = Q.check_feasibility_sum_constraint(Vars, P)
    assert broken_constraints == 0


    var_list = [0,1,0,0,0,0,0,0,0,1,0]
    Vars.set_values(var_list)
    obj = Q.compute_objective(Vars, P)
    assert obj == pytest.approx(5.0)
    assert Q.chech_feasibility_pair_constraint(Vars, P) == 0
    broken_constraints = Q.check_feasibility_sum_constraint(Vars, P)
    assert broken_constraints == 0


    var_list = [0,1,0,1,0,0,0,0,0,0,0]
    Vars.set_values(var_list)
    assert Q.chech_feasibility_pair_constraint(Vars, P) == 1
    broken_constraints = Q.check_feasibility_sum_constraint(Vars, P)
    assert broken_constraints == 0


    var_list = [0,0,0,1,0,1,0,0,0,1,0]
    Vars.set_values(var_list)
    assert Q.chech_feasibility_pair_constraint(Vars, P) == 0
    broken_constraints = Q.check_feasibility_sum_constraint(Vars, P)
    assert broken_constraints == 1


    solutions = solve_on_DWave(Q.qubo_terms, no_runs = 1, real = False, hyb = False)

    check_solutions(Vars, P, Q, solutions.record)
