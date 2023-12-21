from csp import *

"""variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b"""



# print([x.split() for x in open('../texts/var11.txt').readlines()])        

class Model():
    def __init__(self):
        self.score = 0

    def info_ret():
        vartxt = open('../texts/var11.txt', 'r')
        domtxt = open('../texts/dom11.txt', 'r')
        ctrtxt = open('../texts/ctr11.txt', 'r')

        firstline = 0

        var = []
        dom = []
        neighbors = []

        for lines in vartxt.readlines():
            if firstline != 0 : var.append(lines.split()[0]), dom.append(lines.split()[-1]) 
            firstline += 1

        vartxt.close()
        domtxt.close()
        ctrtxt.close()

        return var, dom
    

    #TODO: constraints:function if A, B satisfies the constraint




# print([x.split(' ')[0] for x in open('../texts/var11.txt').readlines()])        
def main(): 
    # var  = ([])
    var, dom = Model.info_ret()
    # print(var[1], dom[1])
    


if __name__== "__main__": 
    main() 