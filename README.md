Artificial Intelligence
Radio Link Frequency Assignment Problem


Figure 1: Results/Reportt in /pdfs

Based on the above results, the following conclusions are drawn:
The use of the DOM/WDEG heuristic produces consistent results each time as it does not depend on any random factor.

As in theory, it is now verified that the nodes assigned and the checks for each algorithm are:

FC-CBJ <= FC -BT and MAC < FC-BT, 

without any conclusion for MAC/FC-CBJ. The equality between FC-CBJ/FC-BT appears in two instances, where there was a final result after minimal checks/assignments. Primarily, the use of CBJ instead of BT significantly contributes to solving instances in much less time.

Min_conflicts: It does not seem to be efficient, as most times it does not even terminate with a result. The results vary since there is a random factor (variable selection). Therefore, this random variable selection contributes to the algorithm's poor efficiency because it is repeated many times randomly until the solution is found.

Implementations/Changes: All changes are in the new class NewCSP.

DOM/WDEG: Consists of the functions wdeg, dom_wdeg, find_dom. Initially, each uninitialized variable is checked. For each such variable, its uninitialized neighbors are checked, and the weight of the combination (var, neighbor) is added to a new counter (this weight is due to a domain wipe out during a constraint check). A new variable is then found, which depends on the ratio of its domain size (if curr_domain[var] is empty, domain[var] is considered) to the previous counter. Finally, the variable with the smallest ratio is returned.
Weight Increases

Forward_Check2: Weight increase by 1 between (var, B), (B, var) at the moment when the domain of variable B becomes empty due to prunes resulting from assigning a value to var.

Mac: In the revise2 function, similar to Forward_Check2.

Conflict Directed Backjumping
Main Structures:

Past_FC (dictionary of sets)
Conflict_set (dictionary of sets)
no_good (set)

Key Points of the Algorithm:
1) Addition to Past_FC of an unassigned variable, the current assigned variable that caused a prune in the domain of a previous unassigned variable.

2) During a domain wipe out of an unassigned variable, the conflict_set of the current variable is updated with the union of the conflict_set of the current variable and the past_fc of the variable that experienced the domain wipe out.

3) Updating the no_good set with the union of past_fc and conflict_set of the current variable after checking all values of the current variable.

4) During backtracking, the variable that caused a conflict is found in the previous set and must be the "deepest."

5) Once the deepest variable is found, its conflict_set is updated to retain information about previous conflicts.

6) Updating all conflict_sets that changed during the assignment of the new variable
