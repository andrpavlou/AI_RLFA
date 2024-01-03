from newcsp import *
import linecache 
import sys

class Model():
    def file_path(prefix):
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
        return final_var, final_ctr, final_dom

    

    def info_ret(prefix):
        final_var, final_ctr, final_dom = Model.file_path(prefix)
        

        vartxt = open(final_var, 'r')
        ctrtxt = open(final_ctr, 'r')

        var = []
        n_dict = {}
        dom_dict = {}
        neighbors = []
        
        #Retrieve variables
        for v_lines in vartxt.readlines()[1:]:
            var.append(v_lines.split()[0]) #Stores variables. 
            int_var = [eval(i) for i in var] #Transforms string to int.

            dom = (v_lines.split()[-1]) #Get domain number.
            dom = int(dom)

            values = linecache.getline(final_dom, dom + 2)
            values = ' '.join(values.split()[1:]) #ignore first word.
            values = values.split()

            #Stores domains of each variable.
            int_values = [eval(i) for i in values]
            dom_dict[int(var[-1])] = int_values

            for ctr_lines in ctrtxt.readlines()[1:]:
                ctr_lines = ctr_lines.split()


                var_check = int(ctr_lines[0])
                curr_neig = int(ctr_lines[1])

                #Find neighbors of current variable. 
                if var_check == int(var[-1]):
                    neighbors.append(int(curr_neig))
                elif curr_neig == int(var[-1]):
                    neighbors.append(int(var_check))

            #Stores the neighbors of current variable(last appended).
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
            
            con_dict[var1] = list(con_list) #For each variable it is stored, its constraints.
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
            first_var = int(con[0][0]) #First variable of the constraint.
            second_var = int(con[0][1]) #Second variable of the constraint.
            symbol = (con[0][2]) #Store the symbol so there can be identified if the values (a, b) satisfie the constraint.
            k = int(con[0][3])  #Constant of each constrant
        
            #Identify if the current constraint is the one.
            if (first_var == A and second_var == B) or (first_var == B and second_var == A):
                if symbol == '>' and sub > k:
                    return True
            
                if symbol == '=' and sub == k:
                    return True
                    
                return False
                
        #In A and B are not neighbors.
        print("Does not exit!")            
        return False

    #Map the arguements given in command line into the actual functions that will be used.
    def map_arguements():
        var_order_match = {}
        var_order_match["mrv"] = mrv
        var_order_match["wdeg"] = NewCSP.wdeg

        algorithm_match = {}
        algorithm_match["fc"] = NewCSP.forward_checking2
        algorithm_match["mac"] = NewCSP.mac2


        search_algo = {}
        search_algo["bt"] = NewCSP.backtracking_search2
        search_algo["cbj"] = NewCSP.cbj_search
        search_algo["min_conflicts"] = min_conflicts
        return var_order_match, algorithm_match, search_algo
    
    def wrong_input(vo_map, inf_map, search_map):
        run, inference, search_method, var_ordering, instance = sys.argv

        if inference not in inf_map.keys() and search_method != "min_conflicts":
            print("\n---Wrong Inference, try again. Run example: python3 solve.py fc bt wdeg 2-f25---\n\n\n\n")
            exit()

        if search_method not in search_map.keys():
            print("\n---Wrong search algorithm, try again. Run example: python3 solve.py fc bt wdeg 2-f25---\n\n\n\n")
            exit()

        if var_ordering not in vo_map.keys() and search_method != "min_conflicts":
            print("\n---Wrong heuristic, try again. Run example: python3 solve.py fc bt wdeg 2-f25---\n\n\n\n")
            exit()
    
