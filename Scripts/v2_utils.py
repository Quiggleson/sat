from tqdm import tqdm

def todict(instance: list[list[int]]):
    """
    Given a list of lists, return a rope sorted dict

    See Dev Notes/ropeexample.txt for an example of what this means
    """

    # rope dict
    rope = {}

    # iterate clauses
    for clause in instance:

        # add clause to rope sort
        add_clause(rope, frozenset(clause))

    # return processed rope dict
    return rope

def add_clause(rope: dict, clause: frozenset, remaining=None):
    """
    Add a clause to existing rope dict object

    Return true if `clause` is a new clause

    Return false if `clause` already existed in `rope`
    """

    # flag for new clause
    new_flag = False

    # initial case - populate remaining
    if remaining is None:
        remaining = clause

    # base case - at end of path
    if len(remaining) == 0:
        # if rope["0"] exists, it's not a new clause
        if "0" in rope:
            return False
        rope["0"] = clause
        return True

    # iterate terms in remaining
    for term in remaining:

        # add term to rope if not present
        if str(term) not in rope:
            rope[str(term)] = {}

        # update remaining
        r = frozenset([x for x in remaining if x != term])

        # add clause to rope[str(term)] in place with updated remaining
        new_clause = add_clause(rope[str(term)], clause, r)

        # update flag
        new_flag = new_flag or new_clause

    # return ans
    return new_flag

def imply(rope: dict, clause: frozenset, max_clause=3):
    """
    Given a rope dict and a clause, add all new clauses implied by Lemma 5.9

    See Documents/quigley_main.pdf#Lemma5.9 for an explanation of its behavior

    Return True if new clause(s) are added
    """

    # flag to indicate if a new clause is added
    clauses_added = False

    for term in clause:

        # search for a clause with the opposite term
        if str(-1 * term) in rope:

            # make a new clause removing the term
            partial = set([x for x in clause if x is not term])

            # populate found_clauses with clauses with exactly one opposite form term from clause
            found_clauses = search_clauses(rope[str(-1 * term)], clause=clause)

            # iterate found, adding new clauses to rope
            for found_clause in found_clauses:

                # make implied clause out of partial and found w/o opposite form terms
                implied_clause = frozenset(partial.union([x for x in found_clause if x != (-1 * term)]))

                # if the new clause is of length max_clause or less, add it
                if len(implied_clause) < max_clause + 1:

                    # add the implied clause, remember if it's really new or old
                    new_clause = add_clause(rope, implied_clause)

                    # update the new_clause flag 
                    clauses_added = new_clause or clauses_added

    return clauses_added

def search_clauses(rope: dict, found:set[frozenset]|None=None, clause=None):
    """
    Given a rope dict, an optional set of found clauses, and an optional clause,

    if `clause` is ommitted, return all clauses in `rope`

    if `clause` is given, return all clauses in `rope` with at most one opposite form term shared with `clause`
    """

    if found is None:
        found = set()

    # iterate keys in rope
    for key in rope:

        # if key is 0 and the given clause is none and newly found clause does not exist in found
        if (key == "0") and (clause is None) and (rope[key] not in found):

            # add clause to found
            found.add(rope[key])

        # if key is 0 and search clause is given and the new clause is not in found
        elif (key == "0") and (clause is not None) and (rope[key] not in found):

            opp_term_count = 0

            # iterate terms in clause
            for term in clause:

                # if the new clause contains an opposite form term
                if (-1 * term) in rope[key]:

                    # update opp term count
                    opp_term_count += 1

            # if no more than one opp form term exists, add it to found
            if opp_term_count <= 1:

                # append new clause to found
                found.add(rope[key])

        # else if the key is not 0, search the subdictionary
        elif key != "0":

            search_clauses(rope[key], found, clause)
            
    return found

def check_sat(rope: dict, max_clause=3):
    """
    Given a rope sorted instance and the maximum length of clauses to process, 

    Add implied clauses to the instance until you derive contra 1-t clauses or no new clauses are added

    Return False if contra 1-t clauses are added and True otherwise
    """

    # flag to control looping
    new_flag = True

    # loop until no new clauses
    while new_flag:

        # new flag is false until proven otherwise
        new_flag = False

        # get clauses in the instance
        instance = search_clauses(rope)

        # iterate clauses in instance
        for clause in tqdm(instance):

            # if clause is of length 1, look for contra 1-t clause
            if len(clause) == 1:

                # get term
                term, = clause

                # see if contra 1-t clause exists
                if (str(-1 * term) in rope) and ("0" in rope[str(-1 * term)]):

                    # return unsatisfiable
                    return False

            # imply new clauses
            clause_flag = imply(rope, clause, max_clause)

            # update new_flag
            new_flag = clause_flag or new_flag

            # expand clauses shorter than max_clause
            if len(clause) < max_clause:
                
                # expand clauses
                new_clause = expand(rope, clause)

                # update new_flag
                new_flag = new_clause or new_flag

    # no new clauses and no contra 1-t clauses, return satisfiable
    return True

def get_bad_clauses(clauses: list[list[int]] | list[frozenset]):
    """
    given a list of clauses, return the clauses that block no assignments
    """

    # list of bad clauses
    bad_clauses = set()

    # iterate clauses
    for clause in clauses:

        # convert to frozenset
        set_clause = frozenset(clause)

        # iterate terms in clause
        for term in set_clause:

            # if opposite form term is in clause, add it to bad clauses
            if (set_clause not in bad_clauses) and ((-1 * term) in set_clause):

                # append to bad_clauses
                bad_clauses.add(set_clause)

    # return bad clauses
    return bad_clauses

def process(instance: list[list[int]], max_clauses=3):
    """
    Given a list of lists representing an instance and a maximum length of clauses to process, 

    Filter out clauses that contain the same terminal in both forms, 
    
    Sort the instance into a rope dict,

    Check satisfiability using check_sat() and return the outcome
    """

    instance = [x for x in instance if frozenset(x) not in get_bad_clauses(instance)]

    rope = todict(instance)

    sat = check_sat(rope, max_clauses)

    return sat

def expand(rope: dict, clause: frozenset, n=None) -> bool:
    """
    Given a rope dict and a clause, 

    Expand `clause` by one terminal to all possible implied clauses

    Return True if the implied clause is a new clause
    """

    # flag for new clauses
    new_flag = False

    # get keys before modification - dict could change
    keys = list(rope.keys())

    # if n is set, use it
    if n is not None:
        keys = range(1,n+1)
        print(f'keys: {len(keys)}')

    # iterate keys
    for key in keys:

        # get int version
        term = int(key)

        # only add valid clauses
        if (term not in clause) and ((-1 * term) not in clause):

            # add clause w/ positive version of term
            new_clause = add_clause(rope, frozenset(clause.union([term])))

            # update flag
            new_flag = new_clause or new_flag

            # add clause w/ positive version of term
            new_clause = add_clause(rope, frozenset(clause.union([-1 * term])))

            # update flag
            new_flag = new_clause or new_flag

    return new_flag

def test_assignment(instance: list[list[int]], assignment):
    """
    Given an instance and an assignment, return True if it's the satisfying assignment and False otherwise
    """

    # check assignment is valid
    for terminal in assignment:
        if -1 * terminal in assignment and terminal != 0:
            print(f'oi! you have contradicting terminal assignments {terminal} and {-1 * terminal}')
            return False

    # iterate clauses
    for clause in instance:

        # track if the clause is satisfied
        satisfied = False

        # iterate terms
        for term in clause:

            # update satisfied
            # to allow partial assignments, it's not satisfied iff the negation exists in assignment
            satisfied = satisfied or -1 * term not in assignment

        # if none of the terms are in assignment, the clause is false
        if not satisfied:
            return False
        
    # if all clauses are satisfied, return True
    return True

def remap(instance: list[list]):
    """
    given an instance, return an instance remapping the terminals to avoid wasted terminals
    """

    # get the largest terminal in the instance
    largest = 0

    for clause in instance:

        for term in clause:

            largest = max(abs(term), largest)

    # list - index represents old value, value represents new value
    remap = [-1] * (largest + 1)

    # store the next lowest terminal
    next = 1

    # new instance
    new_instance = []

    # iterate clauses
    for clause in instance:

        # create new_clause
        new_clause = []

        # iterate terms
        for term in clause:

            # store positive term in remap
            pos_val = abs(term)

            # if map has not been assigned
            if remap[pos_val] == -1:
                
                # assign it
                remap[pos_val] = next

                # increment next
                next += 1

            # append appropriate form of the terminal
            if term < 0:
                new_clause.append(-1 * remap[pos_val])
            else:
                new_clause.append(remap[pos_val])

        # append clause to new instance
        new_instance.append(new_clause)

    # return new instance
    return new_instance