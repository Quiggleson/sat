from tqdm import tqdm

# given list of lists, return instance as rope sorted dict
def todict(instance: list[list[int]]):

    # rope dict
    rope = {}

    # iterate clauses
    for clause in instance:

        # add clause to rope sort
        add_clause(rope, frozenset(clause))

    # return processed rope dict
    return rope

# given a clause an existing rope dict, 
# update rope dict in place and return True if new clause, False otherwise
def add_clause(rope: dict, clause: frozenset, remaining=None):

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

# given rope dict and clause, add all clauses implied by lemma 5.9
# modify rope in place, return true if new clauses are added
def imply(rope: dict, clause: frozenset):

    # flag to indicate if a new clause is added
    clause_flag = False

    # iterate terms in clause
    for term in clause:

        # search for a clause with the opposite term
        if str(-1 * term) in rope:

            # make a new clause removing the term
            # note: a clause will never have the same term twice
            partial = set([x for x in clause if x is not term])

            # populate found with clauses with at most one opposite form term from clause
            found_clauses = search_clauses(rope[str(-1 * term)], clause=clause)

            # print(f"using clause {clause} found the clauses: {found}")

            # no longer required, all clauses in found contain at most one opposite form term
            # iterate terms in partial
            # for partial_term in partial:

            # # remove found clauses with an opposite form term in partial
            #     found_clauses = [x for x in found_clauses if (-1 * partial_term) not in x]

            # iterate found, adding new clauses to rope
            for found_clause in found_clauses:

                # make implied clause out of partial and found w/o opposite form terms
                implied_clause = frozenset(partial.union([x for x in found_clause if x != (-1 * term)]))

                # if the new clause is of length 3 or less, add it
                if len(implied_clause) < 4:

                    # add the implied clause, remember if it's really new or old
                    new_clause = add_clause(rope, implied_clause)

                    # update the new_clause flag 
                    clause_flag = new_clause or clause_flag

    # return true iff new clauses were added
    return clause_flag

# get all clauses in section of rope dict, valid compared to search clause
def search_clauses(rope: dict, found:set[frozenset]=None, clause=None):

    if found is None:
        found = set()

    # iterate keys in rope
    for key in rope:

        # if key is 0 and clause is none and clause does not exist in found
        if (key == "0") and (clause is None) and (rope[key] not in found):

            # add clause to found
            found.add(rope[key])

        # if key is 0 and search clause is given and the new clause is not in found
        elif (key == "0") and (clause is not None) and (rope[key] not in found):

            # count opposite form terms
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

        # else if the key is not 0, a subdictionary exists
        elif key != "0":

            # search for clauses in child - found gets modified in place
            search_clauses(rope[key], found, clause)
            
    # return found clauses
    return found

# count the total number of "0" keys in rope - should be 6 * len(instance) for debugging
def count_rope(rope: dict, length=-1):

    # track count
    count = 0

    # iterate keys in rope
    for key in rope:

        # if key is 0 
        if key == "0":

            # if counting the current length
            if length == -1 or len(rope[key]) == length:
                # count clause as found
                count += 1

        # else if the key is not 0, a subdictionary exists
        elif key != "0":

            # search for clauses in child - found gets modified in place
            count += count_rope(rope[key], length)
            
    # return found clauses
    return count

# keep getting implications until no new clauses or contra 1-t clauses
# return true iff satisfiable
def check_sat(rope: dict):

    # flag to control looping
    new_flag = True

    # loop until no new clauses
    while new_flag:

        # new flag is false until proven otherwise
        new_flag = False

        # get clauses in the instance
        instance = search_clauses(rope)

        # iterate clauses in instance
        for clause in instance:

            # if clause is of length 1, look for contra 1-t clause
            if len(clause) == 1:

                # get term
                term, = clause

                # see if contra 1-t clause exists
                if (str(-1 * term) in rope) and ("0" in rope[str(-1 * term)]):

                    # return unsatisfiable
                    return False

            # imply new clauses
            clause_flag = imply(rope, clause)

            # update new_flag
            new_flag = clause_flag or new_flag

            # if clause has 2 or fewer terms, expand it
            if len(clause) < 3:

                # expand clauses
                new_clause = expand(rope, clause)

                # update new_flag
                new_flag = new_clause or new_flag

        # print(f'current len: {len(search_clauses(rope))}')

        # print(f'total entries: {count_rope(rope, 3)}')

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
            if (set_clause not in bad_clauses) and ((-1 * term) in set_clause):

                # append to bad_clauses
                bad_clauses.add(set_clause)

    # return bad clauses
    return bad_clauses

# input list of list, preprocess and call all functions
def process(instance: list[list[int]]):

    # print(f'input instance: {instance}')
    
    instance = [x for x in instance if frozenset(x) not in get_bad_clauses(instance)]

    # print(f'processed instance: {instance}')

    rope = todict(instance)

    # print(f'rope len: {len(search_clauses(rope))}')

    sat = check_sat(rope)

    return sat

# expand clause to all clauses of length 1 greater in place, return true iff it's a new clause
def expand(rope: dict, clause: frozenset):

    # flag for new clauses
    new_flag = False

    # get keys before modification - dict could change
    keys = list(rope.keys())

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

# instance = [[-5, -2, 28], [-22, 26, -9], [7, 32, -24], [23, -43, 39], [47, 27, 15], [30, 21, -7], [-29, 37, -23], [28, -20, -29], [36, 7, 42], [36, 8, 48], [6, 50, -34], [10, -36, -33], [1, 18, 8], [37, 9, 49], [-47, -28, -19], [2, 47, 16], [23, 40, -50], [-35, 13, 16], [50, -27, 49], [7, 24, 38], [5, 18, -34], [-41, 11, -48], [31, -36, -12], [23, 49, 6], [-40, 16, -26], [-46, -24, -14], [28, -33, 46], [-20, -9, 4], [10, -5, 2], [-18, -16, -27], [39, 38, 19], [-38, 44, 42], [1, 38, 30], [8, -29, -16], [-20, 12, -7], [41, -43, 36], [19, 32, 46], [31, 16, 2], [-21, -28, -49], [-28, 6, 5], [33, 43, -1], [20, -21, -27], [-29, 12, -7], [-50, -43, -4], [-42, -7, -45], [4, -23, -39], [-50, 9, -11], [18, -2, 4], [1, -32, -17], [-44, 22, -2], [35, 20, 14], [14, -23, -12], [-16, 37, -19], [-41, -50, 10], [-38, 50, -6], [-11, 37, 10], [47, -33, 24], [36, -47, 46], [48, 27, -13], [12, -8, 42], [-14, 44, -24], [-23, 36, 11], [-29, -13, -15], [-31, -26, -41], [49, -5, -23], [30, 31, -24], [-40, 30, -12], [-20, -2, -41], [12, 15, 16], [34, 1, 17], [37, -45, -35], [-36, -38, -21], [25, -7, -45], [6, 2, -44], [-34, -38, 47], [-4, -31, 7], [-29, 26, -43], [-42, 47, -37], [15, -18, -28], [5, 22, 20], [13, 26, -44], [25, -42, -9], [-47, 32, -28], [-9, -32, -7], [-19, -45, -17], [-1, -8, -14], [-27, 2, 18], [-16, -15, 39], [-32, -6, -37], [-34, -11, 22], [39, -50, 25], [-28, 21, 3], [-2, 21, -35], [-46, -45, -37], [-9, 17, -40], [48, 6, -37], [-25, -35, 50], [-48, 32, -26], [-14, -17, 34], [29, -8, 34], [6, 37, 42], [34, -47, -22], [-9, -8, -2], [4, -46, -24], [-33, -2, 25], [-5, -27, -31], [18, 40, -29], [24, 18, -28], [-49, 32, 35], [-45, 46, 17], [-11, -1, -18], [-14, -33, -25], [29, 22, 9], [36, 23, 48], [38, -10, -16], [-25, -5, -37], [28, 13, 12], [44, -32, 31], [18, -23, -27], [-35, -31, -1], [36, -8, -48], [1, -28, 10], [22, 24, -46], [-6, 43, -5], [23, -43, 29], [17, -28, 20], [12, 49, -47], [-34, -32, 50], [11, 39, 17], [-14, 44, 18], [4, -33, -38], [-42, -8, -35], [15, -12, 27], [39, 2, 49], [-30, 31, -13], [-7, -26, 11], [30, -40, -15], [-9, 43, -5], [-44, 47, 42], [-29, 45, 23], [-33, -42, 12], [7, 29, -34], [29, 49, -31], [-7, -49, -22], [-9, 26, -30], [-32, 35, -38], [-12, -18, 6], [21, -16, 12], [-27, -35, 14], [35, 41, -38], [-10, -4, -24], [-25, 8, -4], [43, 24, -7], [20, 2, -34], [-35, 43, 32], [8, 17, -45], [30, 21, 33], [3, 47, 31], [26, 23, -35], [-3, 8, -29], [-5, 14, 10], [30, 48, 43], [36, 10, -12], [32, -41, -5], [-3, -1, -35], [-24, -40, 4], [-5, -19, -20], [13, -17, 37], [7, -14, -42], [39, 32, -42], [13, 37, 16], [38, 24, 23], [35, 33, 19], [23, 14, -15], [-5, -14, -27], [-22, 50, -26], [42, 4, -17], [-18, 46, -20], [38, 39, 41], [48, 9, 29], [-14, 27, -15], [33, -6, -50], [38, 39, -7], [12, -44, -25], [-11, 6, -19], [-48, -36, 37], [5, 10, 19], [-12, -42, -36], [-40, 20, 10], [42, 28, 5], [-37, -9, 39], [40, -45, -26], [25, -39, -43], [6, 25, 8], [-36, 4, 44], [-43, -41, -13], [39, -15, -42], [-46, 3, 28], [-26, -18, -37], [-50, 20, 1], [47, -3, 46], [-7, -23, 36], [37, 33, -16], [-26, -46, 13], [28, 49, 11], [-17, -11, -26], [18, -17, 31], [37, 46, 31], [-3, -19, 31], [47, 39, -28], [16, -14, 20], [-29, -12, -32], [-20, 36, -30], [29, 28, -6], [-17, 22, -45], [41, -39, 9], [30, -44, -43], [-32, 21, -9]]
# ans = process(instance)

# print(f'instance is satisfiable? {ans}')