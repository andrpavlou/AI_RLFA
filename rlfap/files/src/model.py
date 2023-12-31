from newcsp import *
import linecache 
import sys
import time

class Model():

    def info_ret(prefix):

        lastfix = ".txt"
        
        final_var = "../texts/var"
        final_ctr = "../texts/ctr"
        final_dom = "../texts/dom"

        final_var += prefix
        final_var += lastfix

        final_ctr += prefix
        final_ctr += lastfix

        final_dom += prefix
        final_dom += lastfix

        vartxt = open(final_var, 'r')
        ctrtxt = open(final_ctr, 'r')

        var = []
        n_dict = {}
        dom_dict = {}
        neighbors = []

        for v_lines in vartxt.readlines()[1:]:
            var.append(v_lines.split()[0]) #Stores variables 
            int_var = [eval(i) for i in var] #Transforms string to int 

            dom = (v_lines.split()[-1]) #Get domain number
            dom = int(dom)

            values = linecache.getline(final_dom, dom + 2)
            values = ' '.join(values.split()[1:]) #ignore first word
            values = values.split()

            int_values = [eval(i) for i in values]
            dom_dict[int(var[-1])] = int_values

            for ctr_lines in ctrtxt.readlines()[1:]:
                ctr_lines = ctr_lines.split()


                var_check = int(ctr_lines[0])
                curr_neig = int(ctr_lines[1])

                if var_check == int(var[-1]):
                    neighbors.append(int(curr_neig))
                elif curr_neig == int(var[-1]):
                    neighbors.append(int(var_check))


            n_dict[int(var[-1])] = list(neighbors)
            neighbors.clear()
            ctrtxt.seek(0)

        con_dict = {}
        con_list = []
        for var1 in int_var:
            for ctr_lines in ctrtxt.readlines()[1:]:
                ctr_lines = ctr_lines.split()   

                if int(var1) == int(ctr_lines[0]) or int(var1) == int(ctr_lines[1]):
                    con_list.append([ctr_lines, 1])

            con_dict[var1] = list(con_list)
            ctrtxt.seek(0) 
            con_list.clear()

        vartxt.close()
        ctrtxt.close()
        return int_var, dom_dict, n_dict, con_dict
    
    """
    con_list [0][0] first constraint
    con_list [0][0][0] first value of the first constraint
    con_list[0][1] counter of the first constraint
    """

    def constraint_check(A, a, B, b, con_dict):
        constraint = con_dict[A]
        sub = abs(a - b)

        for con in constraint:
            first_var = int(con[0][0])
            second_var = int(con[0][1])
            symbol = (con[0][2])
            k = int(con[0][3])
        

            if (first_var == A and second_var == B) or (first_var == B and second_var == A):
                if symbol == '>' and sub > k:
                    return True
            
                if symbol == '=' and sub == k:
                    return True
                    
                return False
                
        #Not found    
        print("Does not exit!")            
        return False

    def unpack_arguements(inference, search_method, var_ordering):
        var_order_match = {}
        var_order_match["mrv"] = mrv
        var_order_match["wdeg"] = wdeg

        algorithm_match = {}
        algorithm_match["fc"] = forward_checking2
        algorithm_match["mac"] = mac2

        search_algo = {}
        search_algo["bt"] = backtracking_search2
        search_algo["cbj"] = cbj_search
        return var_order_match, algorithm_match, search_algo
    


if __name__== "__main__": 
    inference = sys.argv[1]
    search_method = sys.argv[2]
    var_ordering = sys.argv[3]
    instance = sys.argv[4]
    

    vo_map, inf_map, search_map = Model.unpack_arguements(inference, search_method, var_ordering)

    if inference not in inf_map.keys():
        print("\n---Wrong Inference, try again. Run example: python3 model.py fc bt wdeg 2-f25 ---\n\n\n\n")
        exit()
    if search_method not in search_map.keys():
        print("\n---Wrong search algorithm, try again. Run example: python3 model.py fc bt wdeg 2-f25 ---\n\n\n\n")
        exit()

    if var_ordering not in vo_map.keys():
        print("\n---Wrong heuristic, try again. Run example: python3 model.py fc bt wdeg 2-f25 ---\n\n\n\n")
        exit()


    print("---------Running---------")
    print("Search Algorithm:", search_method.upper())
    print("select unassigned variable:", var_ordering.upper())
    print("order Domain Values: LCV")
    print("inference:", inference.upper())
    print("--------------------------")

    variables, domains, neighbors, con_dict = Model.info_ret(instance)
    problem = NewCSP(variables, domains, neighbors, Model.constraint_check, con_dict)
    start = time.time()
    
    result = search_map[search_method](problem, select_unassigned_variable = vo_map[var_ordering], 
                        order_domain_values = lcv, inference = inf_map[inference])
    end = time.time()

    print("\n\n---------Results---------")
    if result is None:
        print("The instance does not have a solution.")
    else:
        print("Result:", result)

    print("Assignments:", problem.nassigns)
    print("Time elapsed: ", (end - start))
    
    