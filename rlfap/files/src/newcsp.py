from csp import *

class NewCSP(CSP):
    def __init__(self, variables, domains, neighbors, constraints, constraint_dict):
        self.con_dict = constraint_dict
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(variables, domains, neighbors, constraints, constraint_dict)


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))


def dom_wdeg(csp, assignment, var):
    # print(csp.nassigns)
    if csp.curr_domains is None:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])
    
    if var in assignment:
        return float('inf')
    
    weight = 0
    for con in csp.con_dict[var]:
        if ((int(con[0][1]) == var) or \
        (int(con[0][0]) == var)):
            weight += con[1]
   
    if weight:
            return len(csp.curr_domains[var]) / weight

    return float('inf')
    

    

def wdeg(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: dom_wdeg(csp, assignment, var))

# ______________________________________________________________________________
# Constraint Propagation with AC3


def no_arc_heuristic(csp, queue):
    return queue


def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def AC3b(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        # Si_p values are all known to be supported by Xj
        # Sj_p values are all known to be supported by Xi
        # Dj - Sj_p = Sj_u values are unknown, as yet, to be supported by Xi
        Si_p, Sj_p, Sj_u, checks = partition(csp, Xi, Xj, checks)
        if not Si_p:
            return False, checks  # CSP is inconsistent
        revised = False
        for x in set(csp.curr_domains[Xi]) - Si_p:
            csp.prune(Xi, x, removals)
            revised = True
        if revised:
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
        if (Xj, Xi) in queue:
            if isinstance(queue, set):
                # or queue -= {(Xj, Xi)} or queue.remove((Xj, Xi))
                queue.difference_update({(Xj, Xi)})
            else:
                queue.difference_update((Xj, Xi))
            # the elements in D_j which are supported by Xi are given by the union of Sj_p with the set of those
            # elements of Sj_u which further processing will show to be supported by some vi_p in Si_p
            for vj_p in Sj_u:
                for vi_p in Si_p:
                    conflict = True
                    if csp.constraints(Xj, vj_p, Xi, vi_p):
                        conflict = False
                        Sj_p.add(vj_p)
                    checks += 1
                    if not conflict:
                        break
            revised = False
            for x in set(csp.curr_domains[Xj]) - Sj_p:
                csp.prune(Xj, x, removals)
                revised = True
            if revised:
                for Xk in csp.neighbors[Xj]:
                    if Xk != Xi:
                        queue.add((Xk, Xj))
    return True, checks  # CSP is satisfiable



def mac(csp, var, value, assignment, removals, constraint_propagation=AC3b):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def forward_checking2(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()

    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b, csp.con_dict):
                    csp.prune(B, b, removals)

            if len(csp.curr_domains[B]) == 0:
                constraint = csp.con_dict[B]
                for i in range(len(constraint)):

                    if int(constraint[i][0][0]) == int(var) and int(constraint[i][0][1]) == int(B) or \
                    int(constraint[i][0][0]) == int(B) and int(constraint[i][0][1]) == int(var):
                        constraint[i][1] += 1
                        break

            if not csp.curr_domains[B]:
                return False
    return True

# The search, proper


def backtracking_search2(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def backtrack2(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack2(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None
    
    result = backtrack2({})

    assert result is None or csp.goal_test(result)
    return result
