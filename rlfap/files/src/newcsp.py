from csp import *

class NewCSP(CSP):
    def __init__(self, variables, domains, neighbors, constraints, constraint_dict):
        super().__init__(variables, domains, neighbors, constraints, constraint_dict)
        self.con_dict = constraint_dict
        self.check = 0
        self.last_var = None

        self.no_good = set()
        self.conflict_set = {var : set() for var in self.variables}
        self.past_fc = {var : set() for var in self.variables}  #For any unissigned variable a current 
                                                                #var is stored, which caused domain prunes.
        self.weight = {}
        for values, keys in neighbors.items():
            for key in keys:
                self.weight[(values, key)] = 1    
        

    def find_dom(csp, var):
        """Return all values for var that aren't currently ruled out."""
        if not csp.curr_domains: 
            return csp.domains[var]
        return csp.curr_domains[var]
    
    def dom_wdeg(csp, assignment, var): 
        weight = 0
        
        #Finds the ratio of the current value.
        for neighbor in csp.neighbors[var]:
            if neighbor not in assignment: weight += csp.weight[(var, neighbor)]

        dom_len = len(NewCSP.find_dom(csp, var))
        return dom_len / (weight or 1)

    def wdeg(assignment, csp):
        min_value, curr_value, min_var = float('inf'), -1, None

        #Finds the variable with the smallest ratio using function (dom_wdeg).
        for v in csp.variables:
            if v not in assignment:
                curr_value = NewCSP.dom_wdeg(csp, assignment, v)
            if min_value > curr_value and v not in assignment:
                min_value, min_var, curr_value = curr_value, v, float('inf')

        
        return min_var

    def revise2(csp, Xi, Xj, removals, checks=0):
        revised = False
        for x in csp.curr_domains[Xi][:]:
            # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
            # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            conflict = True
            for y in csp.curr_domains[Xj]:
                csp.check += 1
                if csp.constraints(Xi, x, Xj, y, csp.con_dict):
                    conflict = False
                checks += 1
                if not conflict:
                    break
            if conflict:
                csp.prune(Xi, x, removals)
                revised = True

            #Domain wipe out, +1 to the weight of the combination (var, neighbor).
            if len(csp.curr_domains[Xi]) == 0:
                csp.weight[(Xi, Xj)] += 1
                csp.weight[(Xj, Xi)] += 1

        return revised


    def AC3_2(csp, queue = None, removals = None, arc_heuristic = dom_j_up):
        """[Figure 6.3]"""
        if queue is None:
            queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
        csp.support_pruning()
        queue = arc_heuristic(csp, queue)
        checks = 0
        while queue:
            (Xi, Xj) = queue.pop()
            revised = NewCSP.revise2(csp, Xi, Xj, removals, checks)
            if revised:
                if not csp.curr_domains[Xi]:
                    return False  # CSP is inconsistent
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xj:
                        queue.add((Xk, Xi))
        return True  # CSP is satisfiable

    def mac2(csp, var, value, assignment, removals, constraint_propagation = AC3_2):
        """Maintain arc consistency."""
        return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)


    def forward_checking2(csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value."""
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    csp.check += 1
                    if not csp.constraints(var, value, B, b, csp.con_dict):
                        csp.prune(B, b, removals)
                        csp.past_fc[B].add(var)
                
                #Domain wipe out, +1 to the weight of the combination (var, neighbor).
                if len(csp.curr_domains[B]) == 0:
                    csp.weight[(var, B)] += 1
                    csp.weight[(B, var)] += 1
                        
                if not csp.curr_domains[B]:
                    csp.last_var = B
                    return False
        return True


    def cbj_search(csp, select_unassigned_variable = wdeg,
                    order_domain_values = lcv, inference = forward_checking2):

            def cbj(assignment):
                if len(assignment) == len(csp.variables):
                    return assignment
                
                var = select_unassigned_variable(assignment, csp)
                for value in order_domain_values(var, assignment, csp):
                    #Assign to the current variable, the current value of the domain.
                    csp.assign(var, value, assignment)
                    removals = csp.suppose(var, value)
                    
                    #Inference, to prune the unnecessary values of the neighbhors' domains.(Forward Checking in this case)
                    check = inference(csp, var, value, assignment, removals)
                    
                    #There wasn't a domain wipe out in the future variables.
                    #Recursively go to the next variable.
                    if check:
                        result = cbj(assignment)
                        
                        #Result has been found, outwise the current domain has checked, 
                        #all the values in its domain.
                        if result is not None:
                            return result

                        #If result was not found, it must backtrack to the variable in the
                        #csp.no_good set which might have caused problems.
                        #(The variable that it is searching is the deepest).
                        if var not in csp.no_good:
                            #If variable is not inside the no_good set we must restore 
                            #curr_domains and unassign the current variable.
                            csp.restore(removals)
                            csp.unassign(var, assignment)
                            return None

                        #The deepest variable has been found, hence the no_good set 
                        #must be merged with the conflict set of the current variable,
                        #so there will not be any lost information of conflicts.
                        csp.conflict_set[var] = csp.conflict_set[var].union(csp.no_good)
                        csp.conflict_set[var] -= {var}

                        #Restore conflict sets before the assignment of the previously,
                        #last assigned variable.
                        for variables in csp.past_fc[var]:
                            csp.conflict_set[variables] = set()
                    
                    #Wipe of future unassigned variable's domain. -> merge CS(var)+PFC(last_var)
                    if not check:
                        csp.conflict_set[var] = csp.conflict_set[var].union(csp.past_fc[csp.last_var])

                    csp.restore(removals)
                    csp.unassign(var, assignment)

                #Current variable's domain wipe out -> backtrack to the variable in no_good set (deepest).
                csp.no_good = csp.past_fc[var].union(csp.conflict_set[var])
                return None

            result = cbj({})
            assert result is None or csp.goal_test(result)
            return result


    def backtracking_search2(csp, select_unassigned_variable = first_unassigned_variable,
                            order_domain_values = unordered_domain_values, inference = forward_checking2):

            def backtrack(assignment):
                print(csp.nassigns)
                if len(assignment) == len(csp.variables):
                    return assignment
                var = select_unassigned_variable(assignment, csp)
                for value in order_domain_values(var, assignment, csp):
                    if 0 == csp.nconflicts(var, value, assignment):
                        csp.assign(var, value, assignment)
                        removals = csp.suppose(var, value)
                        if inference(csp, var, value, assignment, removals):
                            result = backtrack(assignment)
                            if result is not None:
                                return result
                        csp.restore(removals)
                csp.unassign(var, assignment)
                return None

            result = backtrack({})
            assert result is None or csp.goal_test(result)
            return result