import sys
import itertools
from tqdm import tqdm

# Given an instance of 3SAT
# Write to output file how many times each assignment is blocked
def write_blockages(clauses, n):
    
  # Open output file
  output_file = open('blockages.txt', 'w+')

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

  # Count how many assignments are blocked by just one clause
  fragile_assignments = 0

  # Fragile assignment importance:
  # Recall each clause blocks at most 2^{n-3} assignments
  # Wait a moment, though, there can be unsatisfiable instances
  # that require some overlap
  # WTS they can be mapped to a simpler instance ?????

  # Iterate assignments
  for i in range(2**n):
    
    # Assignment in string format
    assignment_str = str(format(i,f'#0{n+2}b'))[2:]
    
    # Store how many clauses block that assignment
    blocking = 0

    # Loop through clauses
    for clause in clauses:
        
      # Current is blocked - True until one terminal unblocks it
      cur_blocked = True

      # Check each terminal
      for terminal in clause:
        
        # If the terminal is pos and the assignment's value is 1, or
        # if the terminal is neg and the assignment's value is 0, 
        # the assignment is not blocked by the clause
        if terminal > 0 and assignment_str[terminal - 1] == '1' or \
        terminal < 0 and assignment_str[-1*terminal - 1] == '0':
          cur_blocked = False
          # print(f'Assignment: {assignment_str}')
          # print(f'Not blocked by clause: {clause}')

      # If the clause blocks the assignment, increment blocking
      if cur_blocked:
        blocking += 1

    # Incremenet the blocked assignment count
    if blocking > 0:
      blocked_assignments += 1

    # If assignment is blocked by a single clause,
    # that clause is required - store a count of assignments blocked by 1 clause
    if blocking == 1:
      fragile_assignments += 1

    # Print the row with the blocked indicator
    output_file.write(f"| {blocking} | {' | '.join(list(assignment_str))} |\n")
    
  # Report satisfiability
  if blocked_assignments == 2**n:
    print('Unsatisfiable!')
    output_file.write('Unsatisfiable!')
  else:
    print('Satisfiable!')
    output_file.write('Satisfiable!')

  # Write how many assignments are blocked by a single clause
  output_file.write(f'There are {fragile_assignments} assignment(s) blocked by one clause')
    
  # Close the output file
  output_file.close()

# Given a map of assign_str : blockage count
  # clauses and n
# Return a list of clauses that are redundant
def check_redun(assignments, clauses, n):
  # TODO: implement me
  return

n = 6

# clauses = [
#   [1,2,3],
#   # [1,2,-3],
#   [1,-2,3],
#   # [1,-2,-3],
#   [-1,2,3],
#   [-1,2,-3],
#   [-1,-2,3],
#   [4,5,6],
#   [4,5,-6],
#   [4,-5,6],
#   [4,-5,-6],
#   # [-4,5,6],
#   # [-4,5,-6],
#   # [-4,-5,6],
#   [-2,-3,-4]
# ]

# clauses = [
#   [1, 2, 3],
#   [1, 2, -3],
#   [1, -2, 3],
#   [1, -2, -3],
#   [-1, 2, 3],
#   [-1,2,-3],
#   [-1,-2,3]
# ]

# With ghost clauses minus one req clause:
# clauses = [
#   [1, 2, 3], 
#   [1, 2, 4], 
#   [1, 3, 4], 
#   [-1, 2, 3], 
#   [-1, 2, 4], 
#   [-1, 3, 4], 
#   [2, 3, 4],
#   [2, -3, 4],
#   [-2, 3, 4], 
#   [2, 4, 5],
#   [3, 4, 5],
#   [2, 4, -5],
#   [3, 4, -5],
#   [2, 4, 6],
#   [3, 4, 6],
#   [2, 4, -6],
#   [3, 4, -6],
#   [1, 2, -3],
#   [1, -2, 3],
#   [-1, 2, -3],
#   [-1, -2, 3],
#   [4, 5, 6],
#   [4, 5, -6],
#   [4, -5, 6],
#   [4, -5, -6],
#   # [-2, -3, -4] # <- CRITICAL clause
# ]

# Eleven clause unsatisfiable instance
clauses = [
  [1, 2, 3],
  [1, 2, -3],
  [1, -2, 3],
  [-1, 2, 3],
  [-1, 2, -3],
  [-1, -2, 3],
  [4, 5, 6],
  [4, 5, -6],
  [4, -5, 6],
  [4, -5, -6],
  [-2, -3, -4]
]

write_blockages(clauses, n)

'''
Notes

 - 1 based because -0 == +0 == 0
 - Each clause removes a maximum of 2^{n-3} clauses, so if there are fewer than 8 clauses, 
   it will always be satisfiable
 - Each clause blocks 0 to 2^{n-3} clauses
 - We want to iterate through clauses without marking each blocked assignemtn, yet we want
   to know how many blocked assignments there are


Trials

 - With n = 6, x_0...x_4
 - Consider c_1 = (1 v 2 v 3) where i in c_1 represents the 1-indexed index of the assignment
 - This blocks 2^{n-3} assignments, specifically every assignment with x_0 = x_1 = x_2 = 0
 - c_2 = (-1, 2, 3) blocks another 2^{n-3} clauses
 - try all 6 combinations of +-1, +-2, +-3
 - c_3 = (1, -2, 3) blocks 2^{n-3} more
 - c_4 = (1, 2, -3) blocks 2^{n-3} more
 ...
 - c_8 = (-1, -2, -3) blocks 2^{n-3} more

 With n = 6, an instance with each combination of +-1, +-2, +-3 will result in an answer: no satisfying assignment

 This holds true for all n >= 4

  After c_1 = (1 2 3), c_2 could be

 - any number of complements
 (-1 2 3) -> 2^{n-3} new
 
 - has two overlap, one new var
 (1 2 4) == (1 2 -4) -> 2^{n-3} - 2^{n-4} more
 - has one overlap, two new vars
 (1 4 5) == (1 -4 -5) -> 2^{n-3} - 2^{n-5} more
 - has no overlaps, three new vars
 (4 5 6) -> 2^{n-3} - 2^{n-5}

'''