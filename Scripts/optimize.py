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

# given a clause an existing rope dict, ``
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
def imply(rope: dict, clause: frozenset, max_clause=3):

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
                if len(implied_clause) < max_clause + 1:

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
# max_clause - the largest clause that will be processed
def check_sat(rope: dict, max_clause=3):

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

            # if clause has 2 or fewer terms, expand it
            # TODO: control this w/ param, separate from max_clause
            if len(clause) < 3:

                # expand clauses
                new_clause = expand(rope, clause)

                # update new_flag
                new_flag = new_clause or new_flag

            if frozenset([-40, 17, 8]) in search_clauses(rope):
                print(f'i have found it! {search_clauses(rope)}')
                return

        print(f'current len: {len(search_clauses(rope))}')

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

    # print(f'{[x for x in search_clauses(rope) if len(x) < 3]}')

    return sat

# expand clause to all clauses of length 1 greater in place, return true iff it's a new clause
def expand(rope: dict, clause: frozenset, n=None):

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

# return satisfying instance or empty set if none exist
def find_sat_assign(instance: list[list], test_assign=None):

    # track assignment
    assign = set()

    # if test assign is not none, process the instance accordingly
    if test_assign is not None:

        # check assignment is valid
        for terminal in test_assign:
            if -1 * terminal in test_assign and terminal != 0:
                print(f'oi! you have contradicting terminal assignments {terminal} and {-1 * terminal}')
                return False

        for term in test_assign:

            # remove all terms with positive version of the terminal
            instance = [[t for t in c if t != -1 * term] for c in instance]

            # remove all clauses w/ negated version of the terminal
            instance = [x for x in instance if term not in x]

            assign = set(test_assign)

    # sort shortest to longest
    instance.sort(key=lambda x: len(x))

    # if nothing exists in len, return a set with 0 to indicate success
    if len(instance) == 0:
        return set([0])

    # process the first term in the first clause and call recursively to iterate clauses
    clause = instance[0]

    # if it's empty, return empty set to indicate failure
    if len(clause) == 0:
        return set()
    
    # get term
    term = clause[0]

    # try setting term to false

    # remove all terms with positive version of the terminal
    new_instance = [[t for t in c if t != term] for c in instance]

    # remove all clauses w/ negated version of the terminal
    new_instance = [x for x in new_instance if -1 * term not in x]

    # recursively call w/ new instance
    new_assignment = find_sat_assign(new_instance)

    # if successful, add the term to assignment and return
    if len(new_assignment) > 0:
        assign.add(-1 * term)
        assign = assign.union(new_assignment)
        return assign
    
    # if not successful, try w/ positive form of term

    # remove all terms w/ negated version of terminal
    new_instance = [[t for t in c if t != -1 * term] for c in instance]

    # remove clauses w/ positive form of terminal
    new_instance = [x for x in new_instance if term not in x]

    new_assignment = find_sat_assign(new_instance)

    # if successful, add the term to assignment and return
    if len(new_assignment) > 0:
        assign.add(term)
        assign = assign.union(new_assignment)
        return assign
    
    # if both unsucessful, return empty set
    return set()

# given an assignment and an instance, return true iff it's the satisfying assignment
def test_assignment(instance: list[list], assignment):

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

# given an unsatisfiable instance, return an instance st all clauses are necessary to make it unsat
def shorten_instance(instance: list[list]):

    # check if instance is unsat
    assignment = find_sat_assign(instance)

    if len(assignment) > 0:
        print("oi the instance is satisfiable! it should be unsatisfiable!")
        return
    
    # make it a frozenset
    instance = [frozenset(x) for x in instance]

    # clauses to discard
    discard = set()

    # iterate clauses
    for clause in tqdm(instance):

        # try discarding
        try_instance = [list(x) for x in instance if x not in discard and x != clause]

        # get the satisfying assignment
        try_assignment = find_sat_assign(try_instance)

        # if satisfying assignment does not exist, discard clause
        if len(try_assignment) == 0:
            discard.add(clause)

    return [list(x) for x in instance if x not in discard]

# given an instance, return an instance remapping the terminals to avoid wasted terminals
def remap(instance: list[list]):

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

# given an instance an an assignment, get a list of clauses required to block the entirity of that assignment
def get_blockers(instance: list[list], assignment):

    # if assignment is already allowed, return empty list
    if len(find_sat_assign(instance, assignment)) > 0:
        print('warning: the assignment already works')
        return []

    # remember clauses not needed to block the assignment
    discard = set()

    # make instance a list of frozensets
    instance = [frozenset(x) for x in instance]

    # iterate clauses
    for clause in instance:

        # try removing a clause
        try_instance = [list(x) for x in instance if (x not in discard) and (x != clause)]

        # see if it works
        satisfying = find_sat_assign(try_instance, assignment)

        # if we remove a clause and it's still not the satisfying assignment (it's still blocked) then that clause did not block it
        if len(satisfying) == 0:
            discard.add(clause)

    return [list(x) for x in instance if x not in discard]

# given an instance, 
# remove redundant clauses
# convert to rope + process the new instance
# return the list of clauses in the original instance that are not in the new rope
def get_hidden_clauses(instance: list[list]):

    # get new_instance w/o all the clauses
    new_instance = shorten_instance(instance)

    # convert instances to frozensets
    instance = [frozenset(x) for x in instance]
    
    # get rope
    rope = todict(new_instance)

    # remember if it's satisfiable
    satisfiable = check_sat(rope)

    # get clauses from the processed rope
    clauses = search_clauses(rope)

    # get clauses in instance not in processed rope
    hidden = [list(x) for x in instance if x not in clauses]

    # return clauses in original instance not in the processed rope
    return new_instance, hidden

# given an instance and a target clause, expand all clauses to contain all terms in the target clause (resulting in 6-t clauses)
def expand_target(rope: dict, target: list[int]):

    # get clauses
    clauses = search_clauses(rope)

    # iterate clauses
    for clause in clauses:

        # make new clause
        new_clause = clause.union(target)

        # check if it's a valid clause
        valid = any([-1 * x in new_clause for x in new_clause])

        # if it is valid, add it
        if valid:
            add_clause(rope, new_clause)

instance = [[17, -40, 8], [-47, -45, -31], [4, -49, 44], [-7, 36, 6], [-34, -47, 1], [-14, 31, -28], [28, -8, -23], [-16, 49, 41], [-37, -11, 12], [-16, -9, -14], [-30, 12, -9], [-50, 26, 48], [47, 15, -44], [-33, -13, -15], [3, -44, 45], [32, -41, 30], [24, -19, -14], [-20, 7, 41], [10, -13, 38], [7, 35, -13], [41, -3, -15], [39, 16, 44], [31, -14, -40], [-45, 1, -3], [1, 12, -29], [49, -12, -45], [-44, -16, 6], [-7, 27, -46], [22, 18, -38], [5, 34, 10], [-17, -16, -45], [23, -8, 41], [15, 41, -30], [-46, -41, -15], [15, 49, 21], [26, 34, -41], [-6, -35, 41], [-1, 9, -16], [-27, -15, 25], [-28, -14, -18], [23, -13, -19], [-45, -39, 16], [10, 36, -18], [-9, -43, 2], [2, 11, 14], [5, -31, -14], [4, 38, 36], [-29, 32, 7], [-35, -15, -36], [49, 9, -50], [-23, -47, 14], [49, -26, 47], [-47, -31, -25], [28, -2, 11], [-50, 48, -17], [49, -38, 29], [23, -31, -44], [36, -45, 23], [7, -17, 11], [-26, -30, 7], [26, -27, -9], [22, -11, 21], [-8, 15, 14], [-39, -32, -19], [9, 25, 29], [-37, -43, 34], [36, -19, 33], [-26, 41, 27], [41, 10, -33], [-8, -17, 6], [-43, 18, 15], [-47, 48, 29], [41, 30, 3], [-18, 9, -33], [-31, 26, -7], [8, -4, 5], [32, 26, 16], [22, 44, 50], [-47, -28, -27], [-20, -7, 26], [49, 35, -19], [2, -38, 1], [34, -36, -20], [-5, -23, 13], [-3, -6, 27], [42, 46, 43], [-46, -18, -44], [-17, 12, 21], [24, -39, -36], [-9, -44, -20], [-28, 36, -21], [-34, 19, -30], [-10, -24, 34], [2, 30, -43], [16, 11, -6], [30, -36, -4], [-1, 6, -47], [28, -12, 24], [17, -41, 44], [-45, 14, 21], [-33, 45, -7], [15, -12, 49], [-11, -20, 13], [-49, 47, -44], [3, -1, 6], [45, 33, -16], [-46, -34, -40], [46, -6, -1], [11, -39, -27], [46, 34, -33], [-22, 2, -16], [15, -49, 17], [-36, -38, 16], [-17, 7, -45], [26, 5, 10], [40, 27, 18], [39, -29, 19], [-17, 19, -49], [-39, 21, 2], [9, -39, 16], [34, -36, 49], [-22, -29, 42], [-1, -44, -49], [21, -19, 45], [12, -22, 29], [-4, 42, -14], [23, 45, 24], [-7, 13, 23], [9, 29, 11], [24, -33, -38], [-15, -3, 22], [-12, 19, -20], [-10, 31, 2], [49, -29, 40], [26, 14, -34], [44, 31, -36], [41, 20, -1], [50, -15, -7], [12, 46, -5], [-3, -31, -10], [19, 38, 6], [-37, 44, -34], [13, 3, 5], [-45, 15, 48], [44, 20, -33], [-28, -24, 14], [-48, 14, 10], [-22, -13, 16], [28, 26, 35], [27, 18, 20], [-35, -49, -48], [15, 30, -39], [37, 33, -2], [23, 36, -8], [-7, -36, 50], [-2, -29, 19], [24, 40, -31], [2, 1, -25], [-36, -26, -18], [-26, 39, 12], [46, 17, 34], [-16, 39, 50], [38, 3, 14], [45, -42, 43], [39, -11, -13], [-6, -32, 45], [-50, 12, -48], [12, 45, 1], [-42, 2, -48], [9, 2, -43], [-50, -8, 11], [3, -47, -19], [-50, -7, -22], [6, 23, -30], [-35, -15, -45], [7, -35, 5], [-25, -32, -49], [-20, -31, -50], [-19, -37, 3], [-42, 25, 23], [-33, -9, 43], [-39, -1, -3], [-30, 14, -16], [10, 23, 33], [-20, -13, -47], [-1, 31, -7], [15, -5, -34], [2, -21, -41], [-13, 9, -19], [17, -40, 3], [11, 32, -31], [-1, 40, -2], [11, 8, 13], [47, -38, -21], [5, 49, 30], [-7, -23, 42], [-34, 40, 6], [-27, -34, -20], [1, -33, 31], [-11, 2, 12], [-50, 16, -45], [8, 36, -24], [-25, -48, 31], [38, 37, -48], [-32, 18, 46], [16, -8, 20], [45, 7, -8], [-15, -45, 25], [11, -28, 48], [-2, 27, -22], [2, -36, -37], [-43, 40, 42], [28, 24, -7], [14, -29, 23], [-16, -38, 46], [17, 38, -50], [-38, 2, -36], [-40, -29, -17]]

# hidden_tuple = get_hidden_clauses(instance)

# print(f'new instance: {hidden_tuple[0]}\nhidden: {hidden_tuple[1]}')

new_instance = [[-47, -34, 1], [32, 30, -41], [10, -13, 38], [-13, 35, 7], [41, -3, -15], [16, 44, 39], [34, 10, 5], [-16, -45, -17], [-15, -46, -41], [41, -6, -35], [-14, -28, -18], [4, 38, 36], [-15, -36, -35], [49, -26, 47], [-47, -31, -25], [48, -50, -17], [49, -38, 29], [-31, -44, 23], [-45, 36, 23], [-30, -26, 7], [26, -27, -9], [21, -11, 22], [9, 29, 25], [34, -37, -43], [33, 36, -19], [18, -43, 15], [48, -47, 29], [41, 3, 30], [50, 44, 22], [-47, -28, -27], [49, 35, -19], [-23, -5, 13], [42, 43, 46], [-46, -44, -18], [-44, -20, -9], [-21, -28, 36], [-30, 19, -34], [-24, 34, -10], [24, 28, -12], [-45, 21, 14], [-7, 45, -33], [49, -12, 15], [13, -20, -11], [-44, 47, -49], [-16, 33, 45], [-39, 11, -27], [34, 46, -33], [17, -49, 15], [16, -38, -36], [-45, 7, -17], [26, 10, 5], [19, -29, 39], [-49, 19, -17], [-39, 2, 21], [49, 34, -36], [-22, -29, 42], [-44, -1, -49], [-22, 12, 29], [42, -14, -4], [24, 45, 23], [9, 11, 29], [24, -38, -33], [-15, -3, 22], [2, -10, 31], [26, -34, 14], [-36, 44, 31], [41, 20, -1], [-15, 50, -7], [-5, 12, 46], [-31, -3, -10], [19, 38, 6], [-37, 44, -34], [5, 3, 13], [48, -45, 15], [44, 20, -33], [16, -22, -13], [26, 35, 28], [18, 27, 20], [-48, -35, -49], [-39, 30, 15], [33, 37, -2], [-7, 50, -36], [19, -29, -2], [24, -31, 40], [1, 2, -25], [12, -26, 39], [17, 34, 46], [-16, 50, 39], [3, 38, 14], [43, 45, -42], [-13, -11, 39], [-32, -6, 45], [-48, 12, -50], [1, 12, 45], [-48, 2, -42], [-8, 11, -50], [-7, -22, -50], [-15, -45, -35], [5, -35, 7], [-32, -49, -25], [3, -37, -19], [25, -42, 23], [43, -9, -33], [-39, -3, -1], [33, 10, 23], [-47, -13, -20], [-7, -1, 31], [-5, -34, 15], [2, -21, -41], [9, -13, -19], [-40, 17, 3], [32, -31, 11], [40, -1, -2], [8, 11, 13], [-38, -21, 47], [-7, 42, -23], [1, 31, -33], [2, 12, -11], [16, -45, -50], [8, -24, 36], [-48, 31, -25], [-48, 37, 38], [-32, 18, 46], [16, -8, 20], [-8, 45, 7], [-15, -45, 25], [48, 11, -28], [-22, 27, -2], [24, -7, 28], [-16, -38, 46], [17, -50, 38], [-40, -29, -17]]

hidden = [[-40, 17, 8], [-47, -45, -31], [4, 44, -49], [-7, 36, 6], [-14, -28, 31], [-8, -23, 28], [-16, 49, 41], [-37, 12, -11], [-16, -14, -9], [-30, 12, -9], [48, 26, -50], [-44, 15, 47], [-15, -13, -33], [3, -44, 45], [24, -14, -19], [41, -20, 7], [-40, -14, 31], [1, -45, -3], [1, -29, 12], [49, -45, -12], [-16, -44, 6], [-7, -46, 27], [-38, 18, 22], [-8, 41, 23], [41, -30, 15], [49, 21, 15], [26, 34, -41], [-16, 9, -1], [-15, -27, 25], [-13, -19, 23], [16, -39, -45], [10, 36, -18], [2, -43, -9], [2, 11, 14], [-31, -14, 5], [32, -29, 7], [49, -50, 9], [-23, -47, 14], [11, 28, -2], [11, -17, 7], [-8, 14, 15], [-32, -39, -19], [41, 27, -26], [41, 10, -33], [-8, 6, -17], [9, -18, -33], [-31, 26, -7], [8, -4, 5], [32, 16, 26], [-7, 26, -20], [-38, 2, 1], [34, -36, -20], [-6, 27, -3], [12, 21, -17], [24, -39, -36], [2, -43, 30], [16, -6, 11], [-36, -4, 30], [-47, -1, 6], [17, 44, -41], [3, -1, 6], [-40, -46, -34], [-6, 46, -1], [-16, -22, 2], [40, 18, 27], [16, 9, -39], [-19, 45, 21], [-7, 13, 23], [19, -12, -20], [40, 49, -29], [-24, -28, 14], [-48, 10, 14], [-8, 36, 23], [-36, -26, -18], [9, 2, -43], [-47, 3, -19], [-30, 6, 23], [-31, -20, -50], [-16, -30, 14], [49, 5, 30], [40, -34, 6], [-20, -27, -34], [2, -37, -36], [40, 42, -43], [-29, 14, 23], [-38, 2, -36]]

# how on earth can we see if an instance implies a hidden clause? 
# we can expand everything to contain [-40, 17, 8] and see if there's a way to reduce them to [-40, 17, 8]?

# new attempt:
# get rope from new_instance
# process w/ check_sat
# expand_target with target = [-40, 17, 8]
# process w/ check_sat again
# and see if [-40, 17, 8] is in rope

rope = todict(new_instance)

print('check sat round 1')

check_sat(rope)

expand_target(rope, [-40, 17, 8])

print('check sat round 2')

sat = check_sat(rope, 5)

clauses = [list(x) for x in search_clauses(rope) if len(x) <= 3]

print(f'clauses: {clauses}')

print(f'satisfiable (broken maybe)? {sat}')

print(f'satisfying assignment: {find_sat_assign(new_instance)}')

# new_instance = shorten_instance(instance)

# print(f'shortened instance: {new_instance}')

# blocking_clauses = get_blockers(instance, pot_assign)

# print(f'the clauses required to block {pot_assign} are\n{blocking_clauses}')

# print(find_sat_assign(new_instance, pot_assign))

# # instance = remap(instance)

# # print(f'instance: {instance}')

# assignment = find_sat_assign(instance,pot_assign)

# print(f'full assignment: {list(assignment)}')

# # instance = [[3],[1,2],[-1,2]]

# rope = todict(instance)

# ans = check_sat(rope)

# clauses = search_clauses(rope)

# print(f'clauses: {[list(x) for x in clauses]}')

# assignment = find_sat_assign(instance)

# # print('the follow clauses exist in old_instance and not the implied one:')

# # print([list(x) for x in old_instance if frozenset(x) not in clauses])

# print('new instance:')

# print([list(x) for x in clauses])

# # print(list(assignment))

# print('new clauses shorter than 3:')

# print([list(x) for x in clauses if len(x) < 3])

# print(f'instance is satisfiable? {ans}')