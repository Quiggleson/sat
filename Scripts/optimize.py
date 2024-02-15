from tqdm import tqdm
import copy

# use frozen sets and rope sorting to get O(n^6)

# given list of lists, return instance as rope sorted dict
def todict(instance: list[list[int]]):

    # rope dict
    rope = {}

    # iterate clauses
    for clause in instance:

        set_clause = frozenset(clause)

        # add clause to rope sort
        rope = add_clause(rope, set_clause)[0]

    # print(f'from todict, rope len: {len(search_clauses(rope))}')

    # return processed rope dict
    return rope

# given a clause an existing rope dict, 
# return updated rope dict and True if new clause, False otherwise
def add_clause(rope: dict, clause: frozenset, remaining=None):

    # flag for new clause
    new_flag = False

    # initial case - populate remaining
    if remaining is None:
        remaining = clause.copy()

    # base case - add end of path
    if len(remaining) == 0:
        # if rope["0"] exists, it's not a new clause
        if "0" in rope:
            return rope, False
        rope["0"] = clause
        return rope, True

    # iterate terms in remaining
    for term in remaining:

        # use existing subdict if able
        if str(term) in rope:
            subdict = rope[str(term)]
        else:
            subdict = {}

        # update remaining
        r = [x for x in remaining if x != term]

        # try adding new clause
        try_clause = add_clause(subdict, clause, r)

        # update the subdict
        subdict = try_clause[0]

        # add subdict to current
        rope[str(term)] = subdict

        # update flag
        new_flag = new_flag or try_clause[1]

    # return ans
    return rope, new_flag

# given rope dict and clause, add all clauses implied by lemma 5.9
def imply(rope: dict, clause: frozenset):

    # flag to indicate if a new clause is added
    clause_flag = False

    # iterate terms
    for term in clause:

        # search for a clause with the opposite term
        if str(-1 * term) in rope:

            # make a new clause removing the term
            # note: a clause will never have the same term twice
            partial = set([x for x in clause if x is not term])

            # populate found with clauses with at most one opposite form term from clause
            found = search_clauses(rope[str(-1 * term)], clause=clause)

            # print(f"using clause {clause} found the clauses: {found}")

            # no longer required, all clauses in found contain at most one opposite form term
            # # iterate terms in partial
            # for partial_term in partial:

            # # remove found clauses with an opposite form term in partial
            #     found = [x for x in found if (-1 * partial_term) not in found]

            # iterate found, adding new clauses to rope
            for found_clause in found:

                # make implied clause out of partial and found w/o opposite form terms
                implied_clause = frozenset(partial.union([x for x in found_clause if x != -1 * term]))

                # if the new clause is of length 3 or less, add it
                if len(implied_clause) <= 3:

                    # try adding new clause
                    try_clause = add_clause(rope, implied_clause)

                    # add clause to rope dict
                    rope = try_clause[0]

                    # update the new_clause flag 
                    if try_clause[1]:
                        clause_flag = True

    # return updated rope and flag if new clause is added
    return rope, clause_flag

# get all clauses in section of rope dict, valid compared to search clause
def search_clauses(rope: dict, found:set[frozenset]=None, clause=None):

    if found is None:
        found = set()

    # iterate keys in rope
    for key in rope:

        # if key is 0 and clause is none and clause does not exist in found
        if key == "0" and clause is None and rope[key] not in found:

            # add clause to found
            # found.append(rope[key])
            found.add(rope[key])

        # if key is 0 and search clause is given and the new clause is not in found
        elif key == "0" and clause is not None and rope[key] not in found:

            # count opposite form terms
            opp_term_count = 0

            # iterate terms in clause
            for term in clause:

                # if the new clause contains an opposite form term
                if -1 * term in rope[key]:

                    # update opp term count
                    opp_term_count += 1

            # if no more than one opp form term exists, add it to found
            if opp_term_count <= 1:

                # append new clause to found
                found.add(rope[key])

        # else if the key is not 0, a subdictionary exists
        elif key != "0":

            # search for clauses in child
            found = search_clauses(rope[key], found, clause) # check that items get appended to list in place
            
    # return found clauses
    return found

# keep getting implications until no new clauses or contra 1-t clauses
# return true iff satisfiable
def check_sat(rope: dict):

    # flag to control looping
    new_flag = True

    # count how many new clauses are added
    new_clause_count = 0

    # loop until no new clauses
    while new_flag:

        # new flag is false until proven otherwise
        new_flag = False

        # get clauses in the instance
        instance = search_clauses(rope)

        # iterate clauses in instance
        for clause in instance.copy():

            # if clause is of length 1, look for contra 1-t clause
            if len(clause) == 1:

                # get term
                term, = clause

                # see if contra 1-t clause exists
                if str(-1 * term) in rope and "0" in rope[str(-1 * term)]:

                    # print(f'contradicting terms: {clause} and {rope[str(-1 * term)]["0"]}')
                    # print([list(x) for x in search_clauses(rope)])
                    # return unsatisfiable
                    return False

            # imply new clauses
            imply_tuple = imply(rope, clause)

            # update new_flag
            new_flag = imply_tuple[1] or new_flag

            if new_flag:
                new_clause_count += 1

            # update rope dict
            rope = imply_tuple[0]

        # get clauses in the instance
        instance = search_clauses(rope)

        # print(f'current len: {len(instance)}')

    # no new clauses and no contra 1-t clauses, return satisfiable
    return True

# given a list of clauses, return the clauses that block no assignments
def get_bad_clauses(clauses: list[list[int]] | list[frozenset]): 

    # list of bad clauses
    bad_clauses = set()

    # iterate clauses
    for clause in clauses:

        # convert to frozenset
        set_clause = frozenset(clause)

        # iterate terms in clause
        for term in set_clause:

            # if opposite form term is in clause, add it to bad clauses
            if set_clause not in bad_clauses and -1 * term in set_clause:

                # append to bad_clauses
                bad_clauses.add(set_clause)

    # return bad clauses
    return bad_clauses

# input list of list, preprocess and call all functions
def process(instance: list[list[int]]):

    # print(f'input instance: {instance}')
    
    instance = copy.deepcopy(instance)

    instance = [x for x in instance if frozenset(x) not in get_bad_clauses(instance)]

    # print(f'processed instance: {instance}')

    rope = todict(instance)

    # print(f'rope len: {len(search_clauses(rope))}')

    # print(f"Rope: {rope}")

    sat = check_sat(rope)

    return sat

# instance = [[-4, -7, -9], [-7, 7, 9], [3, 7, 10], [4, 11, -11], [7, -8, -9], [-5, -10, 10], [1, -3, 9], [-6, 7, 10], [-2, 9, -9], [-1, 3, -11], [-2, 7, 10], [-2, -3, -5], [-1, -9, 10], [1, -3, 4], [-2, -3, -11], [1, -1, 4], [-8, 11, -11], [4, 8, -11], [1, 5, 10], [-5, 7, 8], [4, 5, -5], [2, 3, -9], [-4, -5, 11], [8, -8, 11], [-2, 5, -6], [3, -5, 10], [1, -2, -6], [4, -6, -10], [-10, 10, 11], [5, -5, -10], [-3, 9, 11], [-5, -6, -8], [-1, 2, 5], [-6, 7, 8], [-1, 7, -8], [1, 5, 6], [-5, 9, 11], [2, -5, 8], [1, -10, -11], [-4, -8, 11], [-1, 7, 11], [3, -7, -9], [-6, 9, 10], [4, -8, 10], [4, 5, -10], [-2, 6, -10], [1, 10, -11], [2, -3, -4], [-6, -10, -11], [-5, -7, -9], [2, 6, 10], [8, -9, 10], [3, 4, -8], [1, -8, 8], [-2, -7, -8], [3, -4, -5], [1, 6, 7], [1, -2, 9], [-1, -5, 6], [3, 7, -10]]

# ans = process(instance)

# print(f'instance is satisfiable? {ans}')