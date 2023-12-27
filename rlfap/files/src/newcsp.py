from csp import *

class NewCSP(CSP):
    def __init__(self, variables, domains, neighbors, constraints, constraint_dict):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(variables, domains, neighbors, constraints, constraint_dict)
        self.con_dict = constraint_dict
        self.cs = {}

        for var in variables:
            self.cs[var] = ()

        # print(self.cs[5])


def dom_wdeg(csp, assignment, var): 
    weight = 1
    for con in csp.con_dict[var]:
        if int(con[0][0]) not in assignment and int(con[0][1]) not in assignment:
            weight += con[1]

    return len(csp.curr_domains[var]) / weight    

    
def wdeg(assignment, csp):
    # print(csp.nassigns)
    """Minimum-remaining-values heuristic."""
    if csp.curr_domains is None:
        return first_unassigned_variable(assignment, csp)
    
    min_value = float('inf')
    min_var = 0
    for v in csp.variables:
        if v not in assignment:
            curr_value = dom_wdeg(csp, assignment, v)
            if min_value >= curr_value:
                min_value = curr_value
                min_var = v

    return min_var
    
    
# ______________________________________________________________________________
# Constraint Propagation with AC3


def revise2(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y, csp.con_dict):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True

###################################
    if len(csp.curr_domains[Xi]) == 0:
        constraint = csp.con_dict[Xi]
        for i in range(len(constraint)):
            if int(constraint[i][0][0]) == int(Xi) and int(constraint[i][0][1]) == int(Xj) or \
            int(constraint[i][0][0]) == int(Xj) and int(constraint[i][0][1]) == int(Xi):
                constraint[i][1] += 1
        
        constraint = csp.con_dict[Xj]
        for i in range(len(constraint)):
            if int(constraint[i][0][0]) == int(Xi) and int(constraint[i][0][1]) == int(Xj) or \
            int(constraint[i][0][0]) == int(Xj) and int(constraint[i][0][1]) == int(Xi):
                constraint[i][1] += 1


    return revised
def AC3_2(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised = revise2(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True  # CSP is satisfiable
def mac2(csp, var, value, assignment, removals, constraint_propagation=AC3_2):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def forward_checking2(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    cs_neighbors = []
    last_var = None

    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b, csp.con_dict):
                    csp.prune(B, b, removals)

                    cs_neighbors.append(B)
###########
###########
###########
            if len(csp.curr_domains[B]) == 0:
                constraint = csp.con_dict[var]
                for i in range(len(constraint)):
                    if int(constraint[i][0][0]) == int(var) and int(constraint[i][0][1]) == int(B) or \
                    int(constraint[i][0][0]) == int(B) and int(constraint[i][0][1]) == int(var):
                        constraint[i][1] += 1
                    
            if len(csp.curr_domains[B]) == 0:
                constraint = csp.con_dict[B]
                for i in range(len(constraint)):
                    if int(constraint[i][0][0]) == int(var) and int(constraint[i][0][1]) == int(B) or \
                    int(constraint[i][0][0]) == int(B) and int(constraint[i][0][1]) == int(var):
                        constraint[i][1] += 1


            if not csp.curr_domains[B]:
                last_var = B
                return False, cs_neighbors, last_var
    return True, cs_neighbors, last_var


def cbj_search(csp, select_unassigned_variable = wdeg,
                order_domain_values = lcv, inference = forward_checking2):
    

    def merge(var, jump_var):
        union_cs =  []
        

        for conflict in csp.conflict_set[jump_var]:
            if conflict != var:
                union_cs.append(conflict)
        
        for conflict in csp.conflict_set[var]:
            if conflict not in union_cs:
                union_cs.append(conflict)

        # print(union_cs)
        csp.conflict_set[var].clear()
        csp.conflict_set[jump_var].clear()
        csp.conflict_set[var] = union_cs

        return csp.conflict_set
    


    def update_conflicts(var, cs_neighbors):
        if cs_neighbors is None:
            return csp.conflict_set
        
        for neighbor in cs_neighbors:
            if var not in csp.conflict_set[neighbor]:
                csp.conflict_set[neighbor].append(var)
                
        return csp.conflict_set
    
    def find_deepest_var(var, csp):
        for conflicts in reversed(csp.conflict_set[var]):
            if conflicts in csp.assignment_list:
                return conflicts
        return None


    def clear_cs(var):
        csp.conflict_set[var].clear()
        return csp.conflict_set

    def cbj(assignment):
        print(csp.nassigns)
        last_var = None
        cs_neighbors = []
        if len(assignment) == len(csp.variables):
            return assignment
        

        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)

                if var not in csp.assignment_list:
                    csp.assignment_list.append(var)

                removals = csp.suppose(var, value)
                check, cs_neighbors, last_var = inference(csp, var, value, assignment, removals)
                csp.conflict_set = update_conflicts(var, cs_neighbors) 

                if not check:
                    merge(var, last_var)
                
                if check:
                    result = cbj(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
                

            if csp.last_value_dom[var] == value:
                last_var = find_deepest_var(var, csp)   
                if last_var != None:
                    var = last_var
            
            csp.unassign(var, assignment)            
            
        return None

    result = cbj({})

    assert result is None or csp.goal_test(result)
    return result

    