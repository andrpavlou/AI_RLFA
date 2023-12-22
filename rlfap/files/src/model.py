from newcsp import *
import linecache 
  
import time

class Model():
    def __init__(self):
        self.score = 0

    def info_ret():
        vartxt = open('../texts/var2-f24.txt', 'r')
        ctrtxt = open('../texts/ctr2-f24.txt', 'r')

        var = []
        n_dict = {}
        dom_dict = {}
        neighbors = []

        for v_lines in vartxt.readlines()[1:]:
            var.append(v_lines.split()[0]) #Stores variables 
            int_var = [eval(i) for i in var] #Transforms string to int 

            dom = (v_lines.split()[-1]) #Get domain number
            dom = int(dom)

            values = linecache.getline('../texts/dom2-f24.txt', dom + 2)
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


        vartxt.close()
        ctrtxt.close()

        return int_var, dom_dict, n_dict
    

    def constraint_check(A, a, B, b):
        ctrtxt = open('../texts/ctr2-f24.txt', 'r')
        for ctr_lines in ctrtxt.readlines()[1:]:
            ctr_lines = ctr_lines.split()
            first_var = int(ctr_lines[0])
            second_var = int(ctr_lines[1])
            symbol = ctr_lines[2]
            k = int(ctr_lines[3])
            sub = abs(a - b)

            if (first_var == A and second_var == B) or (first_var == B and second_var == A):
                
                if symbol == '>' and sub > k:
                    ctrtxt.close()
                    return True
                
                if symbol == '=' and sub == k:
                    ctrtxt.close()
                    return True
        
                ctrtxt.close()                    
                return False
                
        #Not found    
        print("Does not exit!")            
        return False


if __name__== "__main__": 
    variables, domains, neighbors = Model.info_ret()
    problem = NewCSP(variables, domains, neighbors, Model.constraint_check)

    start = time.time()
    result = backtracking_search2(problem, select_unassigned_variable=mrv, inference=forward_checking) is not None
    end = time.time()


    print("Time elapsed: ", (end - start))
