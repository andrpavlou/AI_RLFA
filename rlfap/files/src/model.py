from csp import *
import linecache 


"""     variables: A list of variables; each is atomic (e.g. int or string).
        domains: A dict of {var:[possible_value, ...]} entries.

        neighbors: A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.

        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b"""



# print([x.split() for x in open('../texts/var11.txt').readlines()])        

class Model():
    def __init__(self):
        self.score = 0

    def info_ret():
        vartxt = open('../texts/var11.txt', 'r')
        ctrtxt = open('../texts/ctr11.txt', 'r')

        var = []
        n_dict = {}
        dom_dict = {}
        neighbors = []

        for v_lines in vartxt.readlines()[1:]:
            var.append(v_lines.split()[0]) #Stores variables 
            dom = (v_lines.split()[-1]) #Get domain number
            dom = int(dom)

            values = linecache.getline('../texts/dom11.txt', dom + 2)
            values = ' '.join(values.split()[1:]) #ignore first word
            values = values.split()
            dom_dict[var[-1]] = values

            #### can optimize later if sort file and then go through the file -> O(n)
            for ctr_lines in ctrtxt.readlines()[1:]:
                ctr_lines = ctr_lines.split()
                var_check = int(ctr_lines[0])
                curr_neig = int(ctr_lines[1])
                if var_check == int(var[-1]):
                    neighbors.append(curr_neig)
                elif curr_neig == int(var[-1]):
                    neighbors.append(var_check)


            n_dict[var[-1]] = list(neighbors)
            neighbors.clear()
            ctrtxt.seek(0)


        vartxt.close()
        ctrtxt.close()

        return var, dom_dict, n_dict
    

    #TODO: constraints:function if A, B satisfies the constraint


# print([x.split(' ')[0] for x in open('../texts/var11.txt').readlines()])        
def main(): 
    var, dom_dict, n_dict = Model.info_ret()
    print(n_dict)

    


if __name__== "__main__": 
    main() 