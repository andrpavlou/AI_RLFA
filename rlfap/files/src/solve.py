from model import *
import sys
import time


"""
newcsp.py: Inherits csp class and implements:
    1)Dom/Wdeg Variable Ordering:
    For each variable which is not assigned, if its neighbor is not 
    assigned as well a sum is calculated that is stored in their constraint.
    (Each constraint counter is incremented by one when a domain wipe out occurres, 
    when that constraint is checked).
    For each variable after its sum is calculated, another value is caclulated 
    which takes into consideration the amount of values that the current domain
    of the variable has, devided by the previous created sum. At the end the 
    variable with the minimum ratio is returned.

    2)Conflict Directed Backtracking:
    Similar implementation of Backtracking, but instead for each variable
    there is a conflict set which stores the previous conflicted variables, 
    that were responsible for prunning values of its domain. When a solution 
    is not found and a domain wipe out takes in place, the algorithm backjumps
    to the "deepest" variable in the conflict set of the variable that was 
    previously assigned.
    

model.py: Functions created:
    1)info_ret: Retrieves necessary data from /textxs folder 
    and returns the following variables in the form:
    variables   A list of variables; each is atomic (e.g. int or string).
    domains     A dict of {var:[possible_value, ...]} entries.
    neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
    2)constraint_check: Checks wether the constraint is satisfied between
    two variables (neighbors), given certain values. 
    3)unpack_arguements: Retreives arguements from command line.

Available options to run an instance of RLFA and solve it:
Order Domain Values: LCV
Search Algorithm: BT/CBJ
Variable Ordering: DOM_WDEG/MRV
Inference: FC/MAC/MIN CONFLICTS


How to run examples: 
python3 solve.py inference search_algo heuristic instance 
(For min_conflicts-> inference + heuristic = None)

Example 1: python3 solve.py mac bt mrv 2-f25
Example 2: python3 solve.py fc cbj wdeg 3-f10
Example 3: python3 solve.py - min_conflicts - 2-f24
"""


if __name__== "__main__": 
    run, inference, search_method, var_ordering, instance = sys.argv
    vo_map, inf_map, search_map = Model.map_arguements()
    Model.wrong_input(vo_map, inf_map, search_map)


    print("|-----------------Running-----------------|")
    print("     Search Algorithm:", search_method.upper())
    print("     Select Unassigned Variable:", var_ordering.upper())
    print("     Order Domain Values: LCV")
    print("     Inference:", inference.upper())
    print("     Instance: ", instance)
    print("|-----------------------------------------|")


    variables, domains, neighbors, con_dict = Model.info_ret(instance)
    problem = NewCSP(variables, domains, neighbors, Model.constraint_check, con_dict)
    if search_method == "min_conflicts":
        start = time.time()
        result = search_map[search_method](problem, 10000)
        end = time.time()

        if result is None:
            print("     The instance does not have a solution.")
        else:
            print("     Result:", result)

        print("\n\n|------------------Result-----------------|")
        print("     Assignments:", problem.nassigns)
        print("     Checks:", problem.check)
        print("     Time elapsed:", (end - start))    
        print("|--------------------End------------------|")
        exit()


    start = time.time()
    
    result = search_map[search_method](problem, select_unassigned_variable = vo_map[var_ordering], 
                        order_domain_values = lcv, inference = inf_map[inference])
    end = time.time()


    print("\n\n|------------------Result-----------------|")
    if result is None:
        print("     The instance does not have a solution.")
    else:
        print("     Result:", result)

    print("     Assignments:", problem.nassigns)
    print("     Checks:", problem.check)
    print("     Time elapsed:", (end - start))
    print("|--------------------End------------------|")

    
    