import os
from optimize import process
from tqdm import tqdm
import copy

def parse_cnf_file(file_path):
    clauses = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('p cnf'):
                # Extract the number of variables and clauses
                _, _, num_vars, num_clauses = line.split()
                num_vars, num_clauses = int(num_vars), int(num_clauses)
            elif line.startswith('c') or line.startswith('%'):
                # Skip comment lines
                continue
            else:
                # Parse the clause and add it to the list
                clause = list(map(int, line.split()[:-1]))
                clauses.append(clause)

    return clauses

def process_directory(directory_path):

    instances = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".cnf"):
            file_path = os.path.join(directory_path, filename)
            cnf_clauses = parse_cnf_file(file_path)

            instance = [x for x in cnf_clauses if len(x) > 0]

            instances.append(instance)

    return instances

def process_unsats():

    instances = process_directory('./UUF50.218.1000')[:10]

    for instance in tqdm(instances):

        print(f'testing instance of len {len(instance)}')

        instance_copy = copy.deepcopy(instance)

        sat = process(instance_copy)

        if sat:
            print(f'False positive on instance {instance}')

def process_sat():
    # Parse the .cnf file
    instances = process_directory('./inputs/uf20-91/')[516:]

    # iterate instances
    for instance in tqdm(instances):

        instance_copy = copy.deepcopy(instance)

        # check satisfiability 
        sat = process(instance_copy)

        # all instances in this collection are satisfiable
        if not sat:
            print(f"False negative on instance {instance}")

process_unsats()