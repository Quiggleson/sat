from tqdm import tqdm

def write_blockages(clauses: list[list[int]], n: int) -> None:
    """
    Write information about the instance to `blockages.md`

    1. Write the assignment table

    2. Write how many clauses block each assignment

    3. Write whether the instance is unsatisfiable
    """

    output_file = open('blockages.md', 'w+')

    # Write data about the instance
    output_file.write('Instance:\n')
    output_file.write(f'n: {n}\n')
    output_file.write(f'clauses:\n({len(clauses)})\n')
    
    for clause in clauses:
        output_file.writelines(f'{clause},\n')

    # Headers for table in markdown format
    table_header = "| Blocked | " + " | ".join([f"$x_{i}$" for i in range(1, n + 1)]) + " |"
    table_line = "|---" + "|---" * n + "|"

    # Write table headers
    output_file.write(f'{table_header}\n')
    output_file.write(f'{table_line}\n')

    # Count how many assignments are blocked
    blocked_assignments = 0

    # Iterate assignments
    for i in tqdm(range(2**n)):

        # Assignment in string format
        assignment_str = str(format(i,f'#0{n+2}b'))[2:]

        # Store how many clauses block that assignment
        blocking = 0

        # Loop through clauses
        for clause in clauses:
            
            # Current is blocked - True until one terminal unblocks it
            cur_blocked = True

            for terminal in clause:
                
                # If the terminal is pos and the assignment's value is 1, or
                # if the terminal is neg and the assignment's value is 0, 
                # the assignment is not blocked by the clause
                if terminal > 0 and assignment_str[terminal - 1] == '1' or \
                    terminal < 0 and assignment_str[-1*terminal - 1] == '0':
                        cur_blocked = False

            if cur_blocked:
                blocking += 1

        # Increment the blocked assignment count
        if blocking:
            blocked_assignments += 1

        # Print the row with the blocked indicator
        output_file.write(f"| b: {blocking} | {' | '.join(list(assignment_str))} |\n")

    # Report satisfiability
    if blocked_assignments == 2**n:
        output_file.write('Unsatisfiable!')
    else:
        output_file.write('Satisfiable!')
 
    # Close the output file
    output_file.close()

def is_satisfiable(clauses, n) -> bool:
    """
    Return whether a given instance of 3SAT is satisfiable.

    Note: clauses should be 1-indexed

    This function works in exponential time.
    """
    if 0 in set([term for clause in clauses for term in clause]):
       print("[ERROR] Clause contains 0. Terminals should be 1-indexed.")
       raise TypeError

    assignment = [False] * (n + 1)

    def iterate_assignments(idx: int) -> bool:
        if idx == n + 1:
            return check_assignment()
        
        assignment[idx] = True
        try_true = iterate_assignments(idx + 1)
        if try_true:
            return True

        assignment[idx] = False
        try_false = iterate_assignments(idx + 1)
        return try_false

    def check_assignment() -> bool:
        for clause in clauses:
            satisfied = False
            for term in clause:
                if term > 0 and assignment[abs(term)]:
                    satisfied = True
                    break
                if term < 0 and not assignment[abs(term)]:
                    satisfied = True
                    break
            if not satisfied:
               return False
        return True
  
    return iterate_assignments(1)