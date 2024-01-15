import re

# Input LaTeX type string to represent an instance of 3SAT
# Output list of terminals and pos/neg for each clause
def parse_input(input_string):
    # Extract content within each pair of parentheses
    expressions = re.findall(r'\((.*?)\)', input_string)

    print(f'expressions:\n{expressions}')

    # Initialize a dictionary to store the terminals for each expression
    clauses = []

    # Parse each expression
    for expression in expressions:
        # Extract the subscript value
        match = re.match(r'(?:\\neg\s*)?x_(\d+)', expression)
        if not match:
            raise ValueError(f"Invalid expression: {expression}")

        subscript = int(match.group(1))

        # Check if subscript is greater than the first input value
        if subscript > input_number:
            raise ValueError(f"Subscript value {subscript} is greater than the input value {input_number}")

        # Extract terminals (preceded by \neg or not)
        terminals = re.findall(r'(\\neg\s*)?(x_\d+)', expression)

        # Convert string to int representation like in main.py
        int_rep = []

        for terminal in terminals:

            # Convert terminal to terminal_int
            terminal_str = terminal[1]
            terminal_int = int(terminal_str[terminal_str.index('_')+1:])

            # Negative int to represent negation
            if terminal[0] == '\\neg ':
                int_rep.append(-1*terminal_int)
            else:
                int_rep.append(terminal_int)

        # print(f'terminals:\n{terminals}')

        clauses.append(int_rep)

    return clauses

def generate_binary_table(input_number, clauses):

    # String format of binary numbers
    binary_numbers = [format(i, f'0{input_number}b') for i in range(2**input_number)]

    print(f'binary numbers:\n{binary_numbers}')

    # Create the markdown table
    table_header = "| Blocked | " + " | ".join([f"$x_{i}$" for i in range(1, input_number + 1)]) + " |"
    table_line = "|---|" + "|---" * input_number + "|"

    # Print the markdown table
    print(table_header)
    print(table_line)

    # Generate the table rows
    for row in binary_numbers:
        
        # Check if the row satisfies the instance
        blocked = '' if check_expression(row, clauses) else 'X'

        # Check if the row satisfies all expressions
        #blocked = "X" if all(check_expression(row, terminals, expression) for terminals, expression in expression_terminals.values()) else ""

        # Print the row with the blocked indicator
        print(f"| {blocked} | {' | '.join(list(row))} |")


# Given a string form of a binary number and a list of clauses
# Return true if the row (assignment) satisfies all the clauses
def check_expression(row, clauses):
    
    # Check each clause
    for clause in clauses:
        
        # Var to store if the clause is passing
        satisfiable = False

        # Check each terminal in the clause
        for terminal in clause:

            # Get int value from terminal
            terminal_index = int(terminal[1][terminal[1].index('_')+1:])

            # If a terminal is negated and the value is 0
            # or the terminal is positive and the value is 1 set passing to True
            if terminal[0] == '-' and row[terminal_index-1] == '0' \
            or terminal[0] == '+' and row[terminal_index-1] == '1':
                satisfiable = True

            # print(f'Terminal: {terminal}')
            # print(f'Terminal index: {terminal_index}')
            # print(f'Row: {row}')
            # print(f'Satisfiable: {satisfiable}')
            # print(f'First check: {terminal[0] == "-" and row[terminal_index-1] == "0"}')
            # print(f'First check: {terminal[0] == "+" and row[terminal_index-1] == "1"}')
            # print(f'Terminal[0]: {terminal[0]}')
            # print(f'row[terminal_idx]: {row[terminal_index-1]}')

        # If a clause fails, return false
        if not satisfiable:
            # print(f'Row {row} blocked by clause {clause}')
            return False
    
    # If it makes it through all the clauses, return True
    return True
        

# Get user input for the length of the binary numbers
input_number = int(input("Enter the length of the binary numbers: "))

# Input expression
# input_expression = """
#     $(x_1 \lor x_2 \lor x_3) \land$ <br>
#     $(x_1 \lor x_2 \lor \\neg x_3) \land$ <br>
#     $(x_1 \lor \\neg x_2 \lor x_3) \land$ <br>
#     $(x_1 \lor \\neg x_2 \lor \\neg x_3) \land$ <br>
#     $(\\neg x_1 \lor x_2 \lor x_3) \land$ <br>
#     $(\\neg x_1 \lor x_2 \lor \\neg x_3) \land$ <br>
#     $(\\neg x_1 \lor \\neg x_2 \lor x_3)$ <br>
#     $(\\neg x_1 \lor \\neg x_2 \lor \\neg x_3)$
# """

input_expression = """
$(x_1 \lor x_2 \lor x_4) \land$ <br>
$(x_1 \lor x_2 \lor \\neg x_4) \land$ <br>
$(x_1 \lor \\neg x_2 \lor x_5) \land$ <br>
$(x_1 \lor \\neg x_2 \lor \\neg x_5) \land$ <br>
$(\\neg x_1 \lor x_3 \lor x_6) \land$ <br>
$(\\neg x_1 \lor x_3 \lor \\neg x_6) \land$ <br>
$(\\neg x_1 \lor \\neg x_3 \lor x_7) \land$ <br>
$(\\neg x_1 \lor \\neg x_3 \lor \\neg x_7)$ <br>
"""

# Parse the input expression
clauses = parse_input(input_expression)

print(f'Instance:')
for clause in clauses:
    print(f'{clause}\n')

# TODO: update generate_binary_table to use new format for clauses
    
# Generate and print the binary table
# generate_binary_table(input_number, clauses)

