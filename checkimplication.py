# Given an instance and a (2 clause) implication, 
# return whether or not the instance implies the implication

import itertools
from tqdm import tqdm
import random
from main import write_blockages

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

# Return the satisfying assignment
# Or "" if none exists
def solve(instance, n, assignment=[]):

    # print(f'instance: {[x for x in instance if len(x) < 3]}')
    # print(f'assignment: {assignment}')
    
    # Update assignment if it's the first call
    if len(assignment) == 0:
        assignment = ['Y']
        assignment.extend(['X' for _ in range(n)])

    # If the instance is empty, return assignment
    if len(instance) == 0:
        return assignment

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
            
            # Update assignment
            assignment[abs(terminal)] = 1 if terminal > 0 else 0

            # Consider a potential solution
            potential = solve(instance[1:], n, assignment)

            # If the potential led to a complete solution, return solution
            if len(potential) > 0: 
                return potential
            
            # otherwise, reset the assignment
            assignment[abs(terminal)] = 'X'

    # print('After processing clause, nothing returned')
    # print(f'assignment: {assignment}')
    # print(f'instance: {instance}')

    # After processing clauses, if nothing is returned, then no assignments
    # worked and the clause cannot be satisfied
    return ""

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

            clause.sort()

            if clause not in instance:

                instance.append(clause)

        instances.append(instance)

    return instances

# n = 6
# clauses = [[-6, -2, 6], [-3, -2, 1], [-6, -3, 6], [-6, -3, 5], [-2, 4, 5], [-3, 2, 3], [-6, -2, 1], [-4, -2, 3], [-6, -2, 4], [-1, 2, 6], [-4, 3, 5], [-1, 2, 5], [2, 3, 6], [-3, -1, 5], [-6, -3, 2], [-5, -3, -1], [-3, -2, 4], [-6, -3, -1], [-4, -2, 2], [-5, -4, 5], [-6, -4, 1], [-5, -1, 1], [-1, 1, 2], [-6, 1, 2], [-3, 5, 6], [-2, -1, 1], [-5, 4, 6], [-5, -2, 3], [-1, 5, 6], [-6, 3, 4], [-5, -3, 3], [-6, 2, 6], [-5, 2, 5], [1, 4, 6], [-6, -2, 2], [-4, 4, 5], [-6, -1, 4], [-1, 2, 3], [-5, 3, 5], [-4, 1, 2]]
# ans = solve(clauses, n)
# if len(ans) == 0:
#     print('unsatisfiable')
# else:
#     print(ans)

instance_length = 40
instance_count = 10
n = 6

instances = gen_random_instance(n, instance_count, instance_length)

# print(instances)

for instance in instances:

    satisfiable = write_blockages(instance, n, False)

    assignment_str = solve(instance, n)

    if len(assignment_str) == 0 and satisfiable:
        print(f'False negative on instance {instance}')
    elif len(assignment_str) > 0 and not satisfiable:
        print(f'False positive on instance {instance}')