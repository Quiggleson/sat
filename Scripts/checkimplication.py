# Given an instance and a (2 clause) implication, 
# return whether or not the instance implies the implication

import itertools
from tqdm import tqdm
import random
from main import write_blockages
from optimize import process
import time
import copy

# Return clauses not contributing to implications
def get_complete_data(instance, implications):
    
    # Clauses that contribute to the implication
    contributing_clauses = []

    # Iterate clauses
    for clause in instance:
        # print(f'checking clause {clause}')

        # Iterate implications
        for implication in implications:

            # valid if it should be uncontributing
            valid_clause = True

            # Iterate terminals
            for terminal in implication:

                # If a terminal from the impl. is not in the clause
                # Then that clause
                if terminal not in clause:
                    valid_clause = False

            if valid_clause:
                contributing_clauses.append(clause)

    uncontributing_clauses = []

    # TODO: find an algo that doesn't take hecka long
    for clause in instance:
        if clause not in contributing_clauses:
            uncontributing_clauses.append(clause)

    return uncontributing_clauses

# Get implications of length k
# assume instance is already pruned to only contain clauses of length
# k + 1
def get_implications(instance, k):
    
    implications = []
    
    # Loop through all clauses excecpt the last one
    for idx, clause1 in enumerate(instance[:-1]):

        # Loop through the remaining clauses
        for clause2 in instance[idx+1:]:

            shared = []

            negated = []

            for terminal in clause1:

                if terminal in clause2:

                    shared.append(terminal)

            # After adding shared terminals, try negated terminal
            for terminal in clause1:

                if -1 * terminal in clause2 \
                    and terminal not in shared \
                    and -1 * terminal not in shared:

                    negated.append(terminal)

            if len(shared) == k and len(negated) == 1:

                # sort implication
                shared.sort(key=lambda x: abs(x))

                # add impliciation to the list
                implications.append(shared)

                # print(f'adding implication {shared} from clauses: {clause1} {clause2}')

    # print(f'adding implications {implications}')
    return implications

# Input: instance and implications
# Output: a list of clauses that provide no additional info 
# beyond the implications
# TODO: rename to get_redundant_clauses
def get_contributing_clauses(clauses, implications):

    # Track contributing clauses
    contributing_clauses = []

    # Iterate implications
    for implication in implications:

        # iterate clauses whose length is 1 greater than the implication
        for clause in [x for x in clauses if len(x) == len(implication) + 1]:

            # track shared terminals
            shared = []

            # iterate terminals in the implication
            for terminal in implication:

                # if terminal is in both clause + implication
                if terminal in clause:

                    # add it to shared
                    shared.append(terminal)

            # if all terminals in implication are in shared
            if len(shared) == len(implication):

                # clause implies the implication
                contributing_clauses.append(clause)

    # return contributing clauses
    return contributing_clauses

# Given a list of clauses and the number of terminals, n
# return all clauses of length
# k + 1 that are implied by the clauses
# example, given [[1]], return [1, 2], [1, -2], [1, 3], [1, -3]...
# note that not all clauses have to be the same length
def expand(clauses: list[list], n):

    # store clauses to return
    expansions = []

    for clause in clauses:

        # iterate terminals - do not include current terminal in any form
        for terminal in [x for x in range(1, n+1) if x not in clause and -1 * x not in clause]:

            # create clauses
            new_clause1 = clause.copy()
            new_clause2 = clause.copy()

            # Add new terminals to clause
            new_clause1.append(terminal)
            new_clause2.append(-1 * terminal)

            # Sort the clauses
            new_clause1.sort(key=lambda x: abs(x))
            new_clause2.sort(key=lambda x: abs(x))
            
            # Add new clauses to clauses
            expansions.append(new_clause1)
            expansions.append(new_clause2)

    return expansions

# Get implications by Stronger Lemma I
# Note: only gets clauses of length k +- 1
# Loops through all given clauses, but only considers clauses shorter than 4
def process_clauses(clauses: list[list], n):

    implications = []

    # don't want to imply clauses of length >= 4
    for clause in [x for x in clauses if len(x) < 4]:

        # Maybe doesn't need to be the same length?
        for comp in [x for x in clauses if len(x) == len(clause)]:

            # make new clause a set to avoid duplicates
            new_clause = set()

            # iterate terminals in clause
            for terminal in clause:

                # if the compared clause contains a negated term
                if -1 * terminal in comp:

                    # add all terminals in clause that are not the negated term
                    for c in [x for x in clause if x != terminal]:
                        new_clause.add(c)

                    # add all terminals in comp that are not the negated term
                    for c in [x for x in comp if -1 * x != terminal]:
                        new_clause.add(c)

            # if it's a valid clause
            if len(new_clause):

                # convert to list
                new_clause = list(new_clause)

                # sort
                new_clause.sort(key=lambda x: abs(x))

                # add to implications
                implications.append(new_clause)
                
    return implications

# Return the satisfying assignment
# Or "" if none exists
def solve(instance, n, assignment=[]):

    # print(f'instance: {[x for x in instance if len(x) < 3]}')
    # print(f'assignment: {assignment}')
    
    # Update assignment if it's the first call
    if len(assignment) == 0:
        assignment = ['Y']
        assignment.extend(['X' for _ in range(n)])

    # Get implications of length 2
    implications = get_implications([x for x in instance if len(x) == 3], 2)

    # Get clauses made redundant by the implications
    contributing_clauses = get_contributing_clauses(instance, implications)

    # Remove redundant clauses from instance
    instance = [x for x in instance if x not in contributing_clauses]

    # Add implications to instance, not adding duplicates
    for implication in implications:
        if implication not in instance:
            # print(f'adding implication {implication}')
            instance.append(implication)
        
    # Get implications of length 1
    implications = get_implications([x for x in instance if len(x) == 2], 1)

    # Get clauses made redundant by the implications
    contributing_clauses = get_contributing_clauses(instance, implications)

    # Remove redundant clauses from instance
    instance = [x for x in instance if x not in contributing_clauses]

    # Add implications to instance, not adding duplicates
    for implication in implications:
        if implication not in instance:
            # print(f'adding implication: {implication}')
            instance.append(implication)

    # Remember clauses to remove from instance
    clauses_to_remove = []

    # Remove clauses like [1, 2, -1] because 1 or -1 will be true in every instance
    for clause in instance:
        if len(clause) == 3:
            for terminal in clause:
                if -1 * terminal in clause:
                    clauses_to_remove.append(clause)

    # update instance
    instance = [x for x in instance if x not in clauses_to_remove]

    # Remove clauses consistent with the assignment
    clauses_to_remove = []

    # Iterate terminals
    for terminal in range(1,n+1):

        # Iterate clauses in instance
        for clause in instance:

            # If terminal is consistent with clause
            if assignment[terminal] == 0 and -1 * terminal in clause \
            or assignment[terminal] == 1 and terminal in clause:
                
                # Add clause to removable clauses
                clauses_to_remove.append(clause)

    # Remove clauses
    instance = [x for x in instance if x not in clauses_to_remove]

    # If the instance is empty, return assignment
    if len(instance) == 0:
        return assignment
    
    # Sort the implications
    instance.sort(key=lambda x: len(x))

    # Process the first clause
    clause = instance[0]

    # print(f'instance: {instance}')
    # print(f'assignment: {assignment}')

    # Process one term implications
    if len(clause) == 1:
        
        # int form of terminal
        terminal = clause[0]

        # If the clause is inconsistent with the assignment, return ""
        if terminal < 0 and assignment[abs(terminal)] == 1 \
        or terminal > 0 and assignment[terminal] == 0:
            return ""
        
        # Otherwise, set the terminal value in assignment
        assignment[abs(terminal)] = 1 if terminal > 0 else 0

        # Return solution with new instance
        return solve(instance[1:], n, assignment)

    # Process two terminal implications
    elif len(clause) == 2:

        # Iterate terminals
        for terminal in clause:

            # If the terminal is consistent, just call the function
            if terminal < 0 and assignment[abs(terminal)] == 0 \
            or terminal > 0 and assignment[terminal] == 1:
                
                # We already gained data we need from this clause, call with new instance
                return solve(instance[1:], n, assignment)
            
            # If the terminal is inconsistent, make a new one-term clause
            # with the other terminal and recursively return
            elif terminal < 0 and assignment[abs(terminal)] == 1 \
              or terminal > 0 and assignment[abs(terminal)] == 0:
                
                # Get the other terminal
                other_terminal = [x for x in clause if x != terminal]

                # Add it to the instance and return
                instance.append(other_terminal)

                # Recursively call
                return solve(instance[1:], n, assignment)
            
        # After testing both terminals, try both assignments
        for idx, terminal in enumerate(clause):

            # copy assignment object
            temp_assignment = assignment.copy()

            # Update assignment
            temp_assignment[abs(terminal)] = 1 if terminal > 0 else 0

            # consider a potential solution
            potential = solve(instance[1:], n, temp_assignment)
            
            # If potential is a complete solution, return potential
            if len(potential) > 0:
                return potential
            
            # otherwise, reset assignment and try the next terminal
            # assignment[abs(terminal)] = 'X'

        # If neither assignment returns a solution, this clause cannot be
        # satisfied, so return "" to represent unsatisfiability
        return ""

        # If all terminals have been attempted and none provide a complete clause
        # Either a) both result in ""
        # Or b) both result in a clause like ['Y', 1, 0, 1, 'X', 1, 1]
        # Want to return a partial solution iff it's the last terminal

    # Process three terminal clauses
    elif len(clause) == 3:

        # Iterate terminals
        for terminal in clause:

            # Check if the clause contains the same terminal in both forms
            if -1 * terminal in clause:

                # Extract the other terminal
                other_term = [x for x in clause if x != terminal and x != -1 * terminal]

                # Add the other terminal if it does not exist in the list
                if other_term not in instance:
                    instance.append(other_term)

                # Recursively return - since it's forced
                return solve(instance[1:], n, assignment)

            # If the terminal is consistent, just call the function
            if terminal < 0 and assignment[abs(terminal)] == 0 \
            or terminal > 0 and assignment[terminal] == 1:
                return solve(instance[1:], n, assignment)
            
            # If the terminal is inconsistent, make a new clause
            # with the other terminal(s) and recursively return
            elif terminal < 0 and assignment[abs(terminal)] == 1 \
              or terminal > 0 and assignment[abs(terminal)] == 0:
                
                # Get the other terminal
                other_terminal = [x for x in clause if x != terminal]

                # Add it to the instance and return
                instance.append(other_terminal)

                # Recursively call - since the current terminal failed
                # We know one of the other two have to be true, so we make
                # a knew two terminal clause then continue the recursion
                # ie the two clause is forced, so just return
                return solve(instance[1:], n, assignment)
            
        # After checking each terminal, if nothing can be determined,
        # there is no poly-time solution (with the current method)
        # So return something signifying a solution
        # return assignment

        # After checking each terminal, try each possible assignment
        for idx, terminal in enumerate(clause):
            
            # copy assignment object
            temp_assignment = assignment.copy()

            # Update assignment
            temp_assignment[abs(terminal)] = 1 if terminal > 0 else 0

            # Consider a potential solution
            potential = solve(instance[1:], n, temp_assignment)

            # If the potential led to a complete solution, return solution
            if len(potential) > 0: 
                return potential
            
            # otherwise, reset the assignment
            # assignment[abs(terminal)] = 'X'

    # print('After processing clause, nothing returned')
    # print(f'assignment: {assignment}')
    # print(f'instance: {instance}')

    # After processing clauses, if nothing is returned, then no assignments
    # worked and the clause cannot be satisfied
    return ""

# second attempt at solve() utilizing expand()
# See Plan Expansion in thoughts.md
# given an instance, return the satisfying assignment
# or "" if unsatisfiable
# O(n^11)
def solve_expand(instance, n, assignment=[], processed=[]):

    # Update assignment if it's the first call
    if len(assignment) == 0:
        assignment = ['Y']
        assignment.extend(['X' for _ in range(n)])

    # If instance is empty, return assignment
    if not len(instance):
        return assignment

    # Bool to remember if anything's been changed
    changed = True

    # 5 Repeat until no new implications are added
    while changed:

        # Changed is False until proven True
        changed = False

        # 1.1 Get all three-terminal implications
        implications = get_implications([x for x in instance if len(x) == 4], 3)

        # Add implications to instance, not adding duplicates
        for implication in implications:
            if implication not in instance:
                instance.append(implication)
                changed = True

        # 1 Get all two-terminal implications
        implications = get_implications([x for x in instance if len(x) == 3], 2)

        # Add implications to instance, not adding duplicates
        for implication in implications:
            if implication not in instance:
                instance.append(implication)
                changed = True

        # 2 Get all one-terminal implications
        implications = get_implications([x for x in instance if len(x) == 2], 1)

        # Add implications to instance, not adding duplicates
        for implication in implications:
            if implication not in instance:
                instance.append(implication)
                changed = True

        # 3 Expand all one-terminal expansions
        expansions = expand([x for x in instance if len(x) == 1], n)

        # Add expansions to instance, not adding duplicates
        for expansion in expansions:
            if expansion not in instance:
                instance.append(expansion)
                changed = True

        # 4 Expand all two-terminal expansions
        expansions = expand([x for x in instance if len(x) == 2], n)

        # Add expansions to instance, not adding duplicates
        for expansion in expansions:
            if expansion not in instance:
                instance.append(expansion)
                changed = True

        # 4.3 Expand all three-terminal expansions
        expansions = expand([x for x in instance if len(x) == 3], n)

        # Add expansions to instance, not adding duplicates
        for expansion in expansions:
            if expansion not in instance:
                instance.append(expansion)
                changed = True

    # print('finished round of adding implications and expansions')
    # print(f'one term clauses: {[x for x in instance if len(x) == 1]}')
    # print(f'two term clauses: {[x for x in instance if len(x) == 2]}')
    # print(f'three term clauses: {[x for x in instance if len(x) == 3]}')
    # print(f'four term clauses: {[x for x in instance if len(x) == 4]}')

        # Get list of one terminal clauses
        one_term_clauses = [x for x in instance if len(x) == 1]
        
        # Add check to see if there are contradictions between the one-term clauses
        for clause in one_term_clauses:
            
            # clause containing the negated instance
            negated_clause = [-1 * clause[0]]

            # if the negation of the current clause is also implied
            if negated_clause in one_term_clauses:
                
                # all assignments are blocked
                return ""
            
    print(f'instance from solve_expand: {instance}')
        
    # Ideally an unsat instance will always boil down to a one-terminal clause contradiction
    # So if it gets here, we can just return assignment to signify a satisfiable
    # assignment does exist, but it'll take longer to figure it out
    return assignment

# Solve using Stronger Lemma I
def solve_gen(instance, n, assignment=[]):

    # Update assignment if it's the first call
    if len(assignment) == 0:
        assignment = ['Y']
        assignment.extend(['X' for _ in range(n)])

    # If instance is empty, return assignment
    if not len(instance):
        return assignment

    # Bool to remember if anything's been changed
    changed = True

    # 5 Repeat until no new implications are added
    while changed:

        # Changed is False until proven True
        changed = False

        # get implications
        implications = process_clauses(instance, n)

        # add implications to instance, not adding duplicates
        for implication in implications:
            if implication not in instance:
                instance.append(implication)
                changed = True
                
        # Get list of one terminal clauses
        one_term_clauses = [x for x in instance if len(x) == 1]
        
        # Add check to see if there are contradictions between the one-term clauses
        for clause in one_term_clauses:
            
            # clause containing the negated instance
            negated_clause = [-1 * clause[0]]

            # if the negation of the current clause is also implied
            if negated_clause in one_term_clauses:
                
                # all assignments are blocked
                return ""
            
    # print(f'instance from solve_gen: {instance}')
        
    return assignment

def generate_all_clauses(n):
    terminals = [x for x in range(1,n+1)]
    terminals.extend([-x for x in range(1,n+1)])
    perms = itertools.combinations(terminals, 3)
    clauses = []
    for clause in list(perms):
        clauses.append(list(clause))
    return clauses

# Generate all instances of length m
def generate_instances(m, clauses):
    perms = itertools.combinations(clauses, m)
    instance = []
    for clause in list(perms):
        instance.append(list(clause))
    return instance

# Generate instance_count random instance of length instance_length
# with n terminals
def gen_random_instance(n, instance_count, instance_length):

    # Array to hold the instances
    instances = []

    # Repeat instance_count times
    for _ in range(instance_count):

        # Hold the instance
        instance = []

        # Repeat new clause instance_length times
        while len(instance) < instance_length:

            # Select three random numbers in range(n)
            clause = []

            while len(clause) < 3:
                terminal = random.randrange(1,n+1)
                neg = random.randrange(2)
                if neg == 0:
                    terminal *= -1
                if terminal not in clause:
                    clause.append(terminal)

            clause.sort(key=lambda x: abs(x))

            if clause not in instance:

                instance.append(clause)

        instances.append(instance)

    return instances

instance_length = 60
instance_count = 2
n = 11

instances = gen_random_instance(n, instance_count, instance_length)

sat_count = 0
unsat_count = 0

for instance in tqdm(instances):

    print(f'testing instance: {instance}')

    instance_copy = copy.deepcopy(instance)

    sat_blockages = write_blockages(instance_copy, n, False)

    instance_copy = copy.deepcopy(instance)

    sat_check = process(instance_copy)
    
    # relies on returning bool
    if (not sat_check) and sat_blockages:
        print(f'False negative on instance {instance}')
    elif sat_check and (not sat_blockages):
        print(f'False positive on instance {instance}')


# for instance in tqdm(instances):

#     # instance = instance.copy()

#     start = time.time()
#     satisfiable = write_blockages(instance.copy(), n, False)
#     end = time.time()
#     # print(f'exponential solution: {end - start}')

#     start = time.time()
#     proc_ins = [x for x in instance if frozenset(x) not in get_bad_clauses(instance)]
#     rope = todict(proc_ins)
#     satbycheck = check_sat(rope)
#     # assignment_str = solve_gen(instance.copy(), n)
#     # assignment_str = optim_solve(instance.copy(), n)
#     # assignment_str = solve_expand(instance.copy(), n)
#     # assignment_str = solve(instance.copy(), n)
#     end = time.time()
#     # print(f'polytime solution: {end - start}')

#     # relies on returning str
#     # if len(assignment_str) == 0 and satisfiable:
#     #     print(f'False negative on instance {instance}')
#     # elif len(assignment_str) > 0 and not satisfiable:
#     #     print(f'False positive on instance {instance}')

#     # relies on returning bool
#     print(f"is it satisfiable by satcheck? {satbycheck}")
#     if (not satbycheck) and satisfiable:
#         print(f'False negative on instance {instance}')
#         print(f'Proc instance: {proc_ins}')
#     elif satbycheck and (not satisfiable):
#         print(f'False positive on instance {instance}')

#     if satisfiable:
#         sat_count += 1
#     else:
#         unsat_count += 1

print(f'unsat count: {unsat_count}')
print(f'sat count: {sat_count}')