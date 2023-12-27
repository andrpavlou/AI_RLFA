from newcsp import *
import linecache 
  
import time

class Model():

    def info_ret():
        vartxt = open('../texts/var6-w2.txt', 'r')
        ctrtxt = open('../texts/ctr6-w2.txt', 'r')

        var = []
        n_dict = {}
        dom_dict = {}
        neighbors = []

        for v_lines in vartxt.readlines()[1:]:
            var.append(v_lines.split()[0]) #Stores variables 
            int_var = [eval(i) for i in var] #Transforms string to int 

            dom = (v_lines.split()[-1]) #Get domain number
            dom = int(dom)

            #3-f11.txt
            values = linecache.getline('../texts/dom6-w2.txt', dom + 2)
            values = ' '.join(values.split()[1:]) #ignore first word
            values = values.split()

            int_values = [eval(i) for i in values]
            dom_dict[int(var[-1])] = int_values

            #### can optimize later if sort file and then go through the file -> O(n)
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


    """
    con_list [0][0] first constraint
    con_list [0][0][0] first value of the first constraint
    con_list[0][1] counter of the first constraint
    """
if __name__== "__main__": 
    variables, domains, neighbors, con_dict = Model.info_ret()



    problem = NewCSP(variables, domains, neighbors, Model.constraint_check, con_dict)
    problem2 = NewCSP(variables, domains, neighbors, Model.constraint_check, con_dict)


    print("------WDEG------\n")

    # print("------MAC------")
    # start = time.time()
    # result = backtracking_search2(problem, select_unassigned_variable=wdeg, inference=mac2) is not None
    # print(problem.nassigns)
    # print(result)
    # end = time.time()
    # print("Time elapsed: ", (end - start))

    print("------MAC------")
    start = time.time()
    result2 = cbj_search(problem2, select_unassigned_variable=wdeg, order_domain_values=lcv, inference=forward_checking2) is not None
    print(problem2.nassigns)
    print(result2)
    end = time.time()
    print("Time elapsed: ", (end - start))

