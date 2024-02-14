from tqdm import tqdm

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
def search_clauses(rope: dict, found:set[frozenset] = set(), clause=None):

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
            search_clauses(rope[key], found) # check that items get appended to list in place
            
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

instance1 = [[-4, 8, 9], [1, -2, -10], [1, 10, -10], [1, -8, 11], [2, 8, -9], [-1, -3, -7], [8, 9, 10], [-5, 8, -10], [-2, 5, 9], [3, -3, -6], [1, -5, 5], [2, -6, 9], [-3, -4, 10], [1, -1, 2], [6, -9, -11], [-1, -4, 7], [6, -7, 11], [1, 5, -9], [2, -3, 9], [2, -4, 4], [-3, -5, -9], [4, -9, -11], [-3, -4, -6], [1, -1, 5], [-4, 6, 10], [3, 4, -9], [-6, -10, -11], [-2, -4, -10], [-2, 5, -9], [-3, -8, -9], [4, 5, 11], [2, 7, -10], [-1, 2, -4], [3, -5, 8], [6, -7, -11], [-3, 4, 11], [4, -5, 7], [-1, -10, 11], [5, -6, 11], [-2, -8, -9], [4, 7, -8], [5, -5, 7], [-1, 9, -10], [-2, 3, 5], [-1, 3, -9], [-4, -7, -11], [-5, 11, -11], [-3, -6, -7], [-2, -4, 9], [-7, 9, 10], [-3, 7, 11], [2, -3, 3], [-1, 9, -11], [4, -6, 11], [-2, -6, 8], [1, -2, 6], [-7, -10, -11], [-7, 7, 10], [-1, -7, 10], [4, -7, 9]]

instance1 = [x for x in instance1.copy() if frozenset(x) not in get_bad_clauses(instance1.copy())]

rope = todict(instance1)

# print(f"Rope: {rope}")

sat = check_sat(rope)

print(f'is it satisfiable? {sat}')