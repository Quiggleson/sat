# Given an instance and a (2 clause) implication, 
# return whether or not the instance implies the implication

# Return a list of all two terminal implications
def get_two_term_implications(instance):
    
    # Set of two terminal implications
    implications = []

    # Idea: compare each clause to the clauses that come after
    # and if they differ by a single terminal being negated, 
    for idx, clause1 in enumerate(instance[:-1]):
        for clause2 in instance[idx+1:]:

            print(f'Comparing {clause1} and {clause2}')

            # the implication holds if two terminals are constant
            # between the clauses and the last term is negated

            # 0 if the clauses do not share a negated terminal
            negated_term = 0

            # Array of shared terminals
            common_terms = []
            
            # Iterate through the terminals in clause1 and check for negation
            for term1 in clause1:
                if term1 in clause2:
                    common_terms.append(term1)
                if -1 * term1 in clause2:
                    negated_term = term1

            if negated_term and len(common_terms) == 2:
                implications.append(common_terms)
    
    return implications

# Return clauses not contributing to implications
def get_complete_data(instance, implications):
    
    # Clauses that contribute to the implication
    contributing_clauses = []

    # Iterate clauses
    for clause in instance:
        print(f'checking clause {clause}')

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

                    
# Return true iff the implication can be implied by the instance
# Note: current algo is bad
def check_implication(instance, implication):
    implications = get_two_term_implications(instance)
    if implication in implications:
        return True
    return False

# return the satisfying assignment or empty string if one doesn't exist
def get_assignment(clauses, n):
    
    # Get implications
    implications = get_two_term_implications(clauses)

    # Get clauses that do not contribute to implications
    uncontributing_clauses = get_complete_data(clauses, implications)

    # A single list of all the implications
    shortest_form = implications

    # A single list of all the implications
    shortest_form.extend(uncontributing_clauses)
    
    # sort by length of implication
    shortest_form.sort(key=lambda x: len(x))

    # If there are no two clause implications, it is just as hard 
    # as the beginning, print a warning
    if len(shortest_form[0]):
        print(f'WARNING: there are no two clause implications in instance {clauses}')

    # Assignment where values are guaranteed
    known_assignment = ['X' for _ in range(n)]

    return try_assignment(shortest_form, known_assignment)

# Get implications of length k
# assume instance is already pruned to only contain clauses of length
# k + 1
def get_implications(instance, k):
    
    implications = []
    
    # Loop through all clauses excecpt the last one where len(clause) == k + 1
    for idx, clause1 in enumerate([instance][:-1]):

        # Loop through the remaining clauses
        for clause2 in instance[idx+1:]:

            shared = []

            negated = []

            for terminal in clause1:

                if terminal in clause2:

                    shared.append(terminal)

                if -1 * terminal in clause2:

                    negated.append(terminal)

            if len(shared) == k and len(negated) == 1:

                implications.append(shared)

    print(f'adding implications {implications}')
    return implications

# Return the satisfying assignment
# Or "" if none exists
def solve(instance, n, assignment=[]):

    print(f'instance: {instance}')
    print(f'assignment: {assignment}')
    
    # Update assignment if it's the first call
    if len(assignment) == 0:
        assignment = ['Y']
        assignment.extend(['X' for _ in range(n)])

    # If the instance is empty, return assignment
    if len(instance) == 0:
        return assignment
    
    # Get implications of length 2
    implications = get_implications([x for x in instance if len(x) == 3], 2)

    for implication in implications:
        if implication not in instance:
            instance.append(implication)
        
    # Get implications of length 1
    implications = get_implications([x for x in instance if len(x) == 2], 1)

    for implication in implications:
        if implication not in instance:
            instance.append(implication)

    # Sort the implications
    instance.sort(key=lambda x: len(x))

    # Process the first clause
    clause = instance[0]

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

        # Recursively return with new assignment and removing this clause
        return solve(instance[1:], n, assignment)

    # Process two terminal implications
    elif len(clause) == 2:

        # Iterate terminals
        for terminal in clause:

            # If the terminal is consistent, just call the function
            if terminal < 0 and assignment[abs(terminal)] == 0 \
            or terminal > 0 and assignment[terminal] == 1:
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
            
            # If the value is unknown, update assignment
            assignment[abs(terminal)] = 1 if terminal > 0 else 0

            # Recursively return
            return solve(instance[1:], n, assignment)

    elif len(clause) == 3:

        # Iterate terminals
        for terminal in clause:

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

                # Recursively call
                return solve(instance[1:], n, assignment)
            
            # If the value is unknown, update assignment
            assignment[abs(terminal)] = 1 if terminal > 0 else 0

            # Recursively return
            return solve(instance[1:], n, assignment)


# Eight clause pattern
# clauses = [
#     [1, 2, 3],
#     [1, 2, -3],
#     [1, -2, 3],
#     [1, -2, -3],
#     [-1, 2, 3],
#     [-1, 2, -3],
#     [-1, -2, 3],
#     [-1, -2, -3]
# ]

n = 6

clauses = [
    [1, 2, 3],
    [-1, 4, 5],
    [-2, -4, 6],
    [-1, -4, -6],
    [-1, -5, 4],
    [-2, 1, 4],
    [-3, 1, 2],
    [1, -2, -4],
    # [-1, 2, -4]
]

# implications = get_two_term_implications(clauses)

# uncontributing_clauses = get_complete_data(clauses, implications)

# print(f'implications:\n{implications}\n')
# print(f'uncontributing clauses:\n{uncontributing_clauses}\n')

# get_assignment(clauses,n)

assignment = solve(clauses, n)
if len(assignment) == 0:
    print('Unsatisfiable!')
else:
    print(str(assignment[1:]))