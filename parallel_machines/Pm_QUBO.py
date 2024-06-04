# make QUBO for the Pm problem

from copy import deepcopy
import itertools
import neal

from dwave.system import EmbeddingComposite, DWaveSampler
from dwave.system.composites import FixedEmbeddingComposite
from minorminer import find_embedding

# Problem input

class Job():
    """ stores jobs """
    def __init__(self, id: int, release_t: int, process_t: int, priority: float):
        """ initialize with job i.d. and job parameters """
        self.id = id
        self.release_t = release_t
        self.process_t = process_t
        self.priority = priority
        # initialize with non-physical values
        self.start = -1
        self.end = -1
        self.machine = 0

    
    def set_processing(self, Vars):
        """ set info about processing job on the machine """
        for k, (t,m,j) in Vars.multiindices.items():
            if j == self.id:
                if Vars.q_vars[k].value == 1:
                    self.start = t
                    self.end = t + self.process_t
                    self.machine = m



class Machine():
    """ store machine  """
    def __init__(self, id):
        self.id = id
        self.occupied_till = 0


class Problem():
    """ class of the scheduling problem """
    def __init__(self, tmax):
        self.tmax = tmax
        self.no_jobs = 0
        self.no_machines = 0
        self.machines = {}
        self.jobs = {}

    def add_machines(self, machines_list:list):
        """ add machines to the problem """
        for m in machines_list:
            self.machines[m.id] = m
        self.no_machines = len(machines_list)

    
    def machine_occupation(self, machine:int, occupied_till:int):
        """ add machine occupation time - brkdw constraint """
        self.machines[machine].occupied_till = occupied_till


    def add_jobs(self, jobs_list:list):
        """ add jobs to the problem """
        for j in jobs_list:
            self.jobs[j.id] = j
        self.no_jobs = len(jobs_list)





# QUBO variables

class QUBO_var():
    """ QUBO variable """
    def __init__(self, t:int, m:int, j:int, id:int):
        """ initial multi-index of QUBO variable """
        self.t = t
        self.m = m
        self.j = j
        self.id = id
        # initialize with non-physical values
        self.value = -1


class Variables():
    """ class of QUBO variables """
    def __init__(self, P):
        self.multiindices = self.make_multiindices(P)
        self.q_vars = {}
        for k, (t,m,j) in self.multiindices.items():
            q = QUBO_var(t, m, j, k)
            self.q_vars[k] = q
        self.size = k


    
    def make_multiindices(self, P) -> dict:
        """ return dict of multi indices given the problem class """
        multiindices = {}
        k = 0
        for m_id, m in P.machines.items():
            for j_id, j in P.jobs.items():
                for t in range(P.tmax+1):
                    m = P.machines[m_id]
                    if t >= j.release_t and t >= m.occupied_till:  # check r_j, brkdw
                        k += 1
                        multiindices[k] = (t, m_id, j_id)
        return multiindices
    

    def set_values(self, vals):
        """ set values of QUBO_var, given list or array in vals """
        assert len(vals) == self.size
        for i, v in enumerate(vals):
            assert v in [0,1]
            self.q_vars[i+1].value = v  # renumbering, Python is form 0
                        
        
    def get_k_and_varval(self, t_check:int, m_check:int, j_check:int):
        """ return index and [0,1] value of the QUBO variable of t_check,m_check,j_check """
        for k, (t,m,j) in self.multiindices.items():
            if (t,m,j) == (t_check,m_check,j_check):
                return k, self.q_vars[k].value
        return -1, -1
    

  


class Implement_QUBO():
    """ class of the QUBO formulation  Q[inds] = Q[i,i'] """
    def __init__(self, psum:float, ppair:float, objective):
        """ initialize  with penalty values and the objective function """
        self.psum = psum
        self.ppair = ppair
        self.obj = objective
        self.qubo_terms = {}


    def add_qubo_term(self, inds:tuple, value):
        """ 
        add QUBO term (value) to Q[inds] = Q[i,i']
        create a new entry if there is no entry, or add to an existing entry
        """
        if inds in self.qubo_terms:
            self.qubo_terms[inds] += value
        else:
            self.qubo_terms[inds] = value


    def sum_constraint(self, Vars):
        """ """
        inds_multiinds_same ={}
        inds_multiinds_different ={}
        for k, (t,m,j) in Vars.multiindices.items():
            for kp, (tp,mp,jp) in Vars.multiindices.items():
                # for each job
                if j == jp:
                    if m == mp and t == tp:
                        assert k == kp
                        self.add_qubo_term((k, kp), - self.psum)
                        inds_multiinds_same[(k,kp)] = (t,m,j)
                    else:
                        self.add_qubo_term((k, kp), self.psum)
                        inds_multiinds_different[(k,kp)] = [(t,m,j), (tp,mp,jp)]
        return inds_multiinds_same, inds_multiinds_different
    

    def pair_constraint(self, Vars, P):
        """ """
        inds_multiinds ={}
        for k, (t,m,j) in Vars.multiindices.items():
            for kp, (tp,mp,jp) in Vars.multiindices.items():
                # the same machine
                if m == mp:
                    # different jobs
                    if j != jp:
                        tau = P.jobs[j].process_t
                        taup = P.jobs[jp].process_t
                        if t-taup < tp < t+tau:
                            self.add_qubo_term((k, kp), self.ppair)
                            inds_multiinds[(k,kp)] = [(t,m,j), (tp, mp,jp)]
        
        return inds_multiinds
    

    def objective(self, Vars, P):
        """ add objective terms to QUBO terms """
        for k, (t,m,j) in Vars.multiindices.items():
            weight = P.jobs[j].priority
            penalty = weight*self.obj(t + P.jobs[j].process_t - P.jobs[j].release_t)
            self.add_qubo_term((k, k), penalty)

    def make_QUBO(self, Vars, P):
        """ make QUBO, initialize, then add terms of constraints and objective """
        self.sum_constraint(Vars)
        self.pair_constraint(Vars, P)
        self.objective(Vars, P)


    def chech_feasibility_pair_constraint(self, Vars, P) -> int:
        """ 
        returns an int, number of broken pair constraints of the solution in Vars and jobs in P
        returns 0 if no pair constraints are broken
        """
        broken_constraints = 0
        for (k,kp) in self.pair_constraint(Vars, P):
            if Vars.q_vars[k].value == Vars.q_vars[kp].value == 1:
                broken_constraints += 1

        # Each constraint is counted twice due to symmetry
        return broken_constraints//2
    

    def check_feasibility_sum_constraint(self, Vars, P) -> int:
        """
        returns an int, number of broken sum constraints of the solution in Vars and jobs in P
        returns 0 if no sum constraints are broken
        """
        broken_constraints = 0
        for j_check in P.jobs:
            starts = 0
            for k, (t,m,j) in Vars.multiindices.items():
                if j == j_check:
                    starts += Vars.q_vars[k].value
            if starts != 1:
                broken_constraints += 1
        return broken_constraints


    def compute_objective(self, Vars, P) -> float:
        """
        returns objective of the solution in Vars and jobs in P
        """
        objective = 0
        for k, (t,m,j) in Vars.multiindices.items():
            obj = Vars.q_vars[k].value * self.obj(t + P.jobs[j].process_t - P.jobs[j].release_t)
            obj = obj * P.jobs[j].priority
            objective += obj    
        return objective


# D-Wave and solutions

# https://docs.ocean.dwavesys.com/projects/neal/en/latest/

def solve_on_DWave(Q:dict, no_runs:int, real:bool, at:float = 0.):
    """ Solve  QUBO in Q on the D-Wave  """
    if not real:
        s = neal.SimulatedAnnealingSampler()
        sampleset = s.sample_qubo(
            Q, beta_range = (0.01, 10), num_sweeps = 200,
            num_reads = no_runs, beta_schedule_type="geometric"
        )
    else:

        solver = DWaveSampler(solver="Advantage_system4.1")

        __, target_edgelist, _ = solver.structure

        emb = find_embedding(Q, target_edgelist, verbose=1)

        no_logical = len(emb.keys())
        physical_qbits_lists = list(emb.values())
        physical_qbits_list = list(itertools.chain(*physical_qbits_lists))
        no_physical =  len( set(physical_qbits_list) )
        
        if no_logical < 70:
            print(emb)
        
        print("logical qbits = ", no_logical)

        print("physical qbits", no_physical)

        sampler = FixedEmbeddingComposite(solver, emb)
        
        # Above can be automatic
        #sampler = EmbeddingComposite(DWaveSampler(solver="Advantage_system4.1"))

        sampleset = sampler.sample_qubo(
                Q,
                num_reads=no_runs,
                annealing_time=at
        )

    return sampleset


def display_sol(Vars, P, Q:dict, sol, energy, print_not_feasible:bool):

    Vars.set_values(sol)

    no_feasible = 0
        
    broken_pairs = Q.chech_feasibility_pair_constraint(Vars, P)
    broken_sum = Q.check_feasibility_sum_constraint(Vars, P)

    if broken_pairs == broken_sum == 0:
        print(" ######################  feasible solution #########################")
        print_schedule(Vars, P)
        print("objective", Q.compute_objective(Vars, P))
        print("energy", energy)
        no_feasible += 1
    elif print_not_feasible:
        print(" ########################### not feasible ########################")
        print("broken pair constraint", broken_pairs)
        print("broken sum constraint", broken_sum)
    
    return no_feasible


def check_solutions(Vars, P, Q:dict, solutions, print_not_feasible:bool = False):
    """ check solutions """
    if len(solutions[0]) == 4:
        for (sol, energy, occ, chain_strength) in solutions:
            no_feas = display_sol(Vars, P, Q, sol, energy, print_not_feasible)

    elif len(solutions[0]) == 3:

        for (sol, energy, occ) in solutions:
            no_feas = display_sol(Vars, P, Q, sol, energy, print_not_feasible)
    
    print(no_feas, "feasible solutions out of", len(solutions))
            

            


def print_schedule(Vars, P):
    for job in P.jobs.values():
        job = deepcopy(job)
        job.set_processing(Vars)
        print("..... job", job.id, "......")
        print("machine", job.machine)
        print("release time", job.release_t)
        print("  start time", job.start)
        print("  end   time", job.end)        


