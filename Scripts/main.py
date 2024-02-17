import sys
import itertools
from tqdm import tqdm

# Given an instance of 3SAT
# Write to output file how many times each assignment is blocked
# Return True if satisfiable, false otherwise
def write_blockages(clauses, n, write=True):
  
  # Only write if write is True
  if write:
      
    # Open output file
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

  # Count how many assignments are blocked by just one clause
  fragile_assignments = 0

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
    if write:
      output_file.write(f"| b: {blocking} | {' | '.join(list(assignment_str))} |\n")
    
  # Report satisfiability
  if blocked_assignments == 2**n:
    # print('Unsatisfiable!')
    return False
    if write:
      output_file.write('Unsatisfiable!')
  else:
    # print('Satisfiable!')
    return True
    if write:
      output_file.write('Satisfiable!')

  if write:

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
# clauses = [
#   [1, 2, 3],
#   [1, 2, -3],
#   [1, -2, 3],
#   [-1, 2, 3],
#   [-1, 2, -3],
#   [-1, -2, 3],
#   [4, 5, 6],
#   [4, 5, -6],
#   [4, -5, 6],
#   [4, -5, -6],
#   [-2, -3, -4]
# ] 


# n = 50
# clauses = [[-5, -2, 28], [-22, 26, -9], [7, 32, -24], [23, -43, 39], [47, 27, 15], [30, 21, -7], [-29, 37, -23], [28, -20, -29], [36, 7, 42], [36, 8, 48], [6, 50, -34], [10, -36, -33], [1, 18, 8], [37, 9, 49], [-47, -28, -19], [2, 47, 16], [23, 40, -50], [-35, 13, 16], [50, -27, 49], [7, 24, 38], [5, 18, -34], [-41, 11, -48], [31, -36, -12], [23, 49, 6], [-40, 16, -26], [-46, -24, -14], [28, -33, 46], [-20, -9, 4], [10, -5, 2], [-18, -16, -27], [39, 38, 19], [-38, 44, 42], [1, 38, 30], [8, -29, -16], [-20, 12, -7], [41, -43, 36], [19, 32, 46], [31, 16, 2], [-21, -28, -49], [-28, 6, 5], [33, 43, -1], [20, -21, -27], [-29, 12, -7], [-50, -43, -4], [-42, -7, -45], [4, -23, -39], [-50, 9, -11], [18, -2, 4], [1, -32, -17], [-44, 22, -2], [35, 20, 14], [14, -23, -12], [-16, 37, -19], [-41, -50, 10], [-38, 50, -6], [-11, 37, 10], [47, -33, 24], [36, -47, 46], [48, 27, -13], [12, -8, 42], [-14, 44, -24], [-23, 36, 11], [-29, -13, -15], [-31, -26, -41], [49, -5, -23], [30, 31, -24], [-40, 30, -12], [-20, -2, -41], [12, 15, 16], [34, 1, 17], [37, -45, -35], [-36, -38, -21], [25, -7, -45], [6, 2, -44], [-34, -38, 47], [-4, -31, 7], [-29, 26, -43], [-42, 47, -37], [15, -18, -28], [5, 22, 20], [13, 26, -44], [25, -42, -9], [-47, 32, -28], [-9, -32, -7], [-19, -45, -17], [-1, -8, -14], [-27, 2, 18], [-16, -15, 39], [-32, -6, -37], [-34, -11, 22], [39, -50, 25], [-28, 21, 3], [-2, 21, -35], [-46, -45, -37], [-9, 17, -40], [48, 6, -37], [-25, -35, 50], [-48, 32, -26], [-14, -17, 34], [29, -8, 34], [6, 37, 42], [34, -47, -22], [-9, -8, -2], [4, -46, -24], [-33, -2, 25], [-5, -27, -31], [18, 40, -29], [24, 18, -28], [-49, 32, 35], [-45, 46, 17], [-11, -1, -18], [-14, -33, -25], [29, 22, 9], [36, 23, 48], [38, -10, -16], [-25, -5, -37], [28, 13, 12], [44, -32, 31], [18, -23, -27], [-35, -31, -1], [36, -8, -48], [1, -28, 10], [22, 24, -46], [-6, 43, -5], [23, -43, 29], [17, -28, 20], [12, 49, -47], [-34, -32, 50], [11, 39, 17], [-14, 44, 18], [4, -33, -38], [-42, -8, -35], [15, -12, 27], [39, 2, 49], [-30, 31, -13], [-7, -26, 11], [30, -40, -15], [-9, 43, -5], [-44, 47, 42], [-29, 45, 23], [-33, -42, 12], [7, 29, -34], [29, 49, -31], [-7, -49, -22], [-9, 26, -30], [-32, 35, -38], [-12, -18, 6], [21, -16, 12], [-27, -35, 14], [35, 41, -38], [-10, -4, -24], [-25, 8, -4], [43, 24, -7], [20, 2, -34], [-35, 43, 32], [8, 17, -45], [30, 21, 33], [3, 47, 31], [26, 23, -35], [-3, 8, -29], [-5, 14, 10], [30, 48, 43], [36, 10, -12], [32, -41, -5], [-3, -1, -35], [-24, -40, 4], [-5, -19, -20], [13, -17, 37], [7, -14, -42], [39, 32, -42], [13, 37, 16], [38, 24, 23], [35, 33, 19], [23, 14, -15], [-5, -14, -27], [-22, 50, -26], [42, 4, -17], [-18, 46, -20], [38, 39, 41], [48, 9, 29], [-14, 27, -15], [33, -6, -50], [38, 39, -7], [12, -44, -25], [-11, 6, -19], [-48, -36, 37], [5, 10, 19], [-12, -42, -36], [-40, 20, 10], [42, 28, 5], [-37, -9, 39], [40, -45, -26], [25, -39, -43], [6, 25, 8], [-36, 4, 44], [-43, -41, -13], [39, -15, -42], [-46, 3, 28], [-26, -18, -37], [-50, 20, 1], [47, -3, 46], [-7, -23, 36], [37, 33, -16], [-26, -46, 13], [28, 49, 11], [-17, -11, -26], [18, -17, 31], [37, 46, 31], [-3, -19, 31], [47, 39, -28], [16, -14, 20], [-29, -12, -32], [-20, 36, -30], [29, 28, -6], [-17, 22, -45], [41, -39, 9], [30, -44, -43], [-32, 21, -9]]
# for clause in clauses:
#   clause.sort()

# clauses.sort()

# ans = write_blockages(clauses, n, False)

# print(f'is it satisfiable? {ans}')

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