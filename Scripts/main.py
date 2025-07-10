from tqdm import tqdm
import copy
from baseline_solver import write_blockages, is_satisfiable
from v2_utils import process

def bulk_test_template(instances: list[list[list[int]]], n: int) -> bool:
    """
    Template for testing instances

    Returns whether any false positives or false negatives exist
    """
    sat_count = 0
    unsat_count = 0
    false_positives = 0
    false_negatives = 0

    for instance in tqdm(instances):

        instance_copy = copy.deepcopy(instance)

        is_sat_from_baseline = is_satisfiable(instance_copy, n)

        is_sat_from_algo = process(instance_copy)
        
        if not is_sat_from_algo and is_sat_from_baseline:
            print(f'False negative on instance {instance}')
            false_negatives += 1
        elif is_sat_from_algo and not is_sat_from_baseline:
            print(f'False positive on instance {instance}')
            false_positives += 1

        if is_sat_from_baseline:
            sat_count += 1
        else:
            unsat_count += 1

    print(f"Total of {sat_count} satisfiable instances")
    print(f"Total of {unsat_count} unsatisfiable instances")

    return bool(false_positives or false_negatives)

def large_instance_demo():
    """
    Tests an example instance with 50 terminals using the process() function from optimize.py
    """
    instance = [[-47, -34, 1], [32, 30, -41], [10, -13, 38], [-13, 35, 7], [41, -3, -15], [16, 44, 39], [34, 10, 5], [-16, -45, -17], [-15, -46, -41], [41, -6, -35], [-14, -28, -18], [4, 38, 36], [-15, -36, -35], [49, -26, 47], [-47, -31, -25], [48, -50, -17], [49, -38, 29], [-31, -44, 23], [-45, 36, 23], [-30, -26, 7], [26, -27, -9], [21, -11, 22], [9, 29, 25], [34, -37, -43], [33, 36, -19], [18, -43, 15], [48, -47, 29], [41, 3, 30], [50, 44, 22], [-47, -28, -27], [49, 35, -19], [-23, -5, 13], [42, 43, 46], [-46, -44, -18], [-44, -20, -9], [-21, -28, 36], [-30, 19, -34], [-24, 34, -10], [24, 28, -12], [-45, 21, 14], [-7, 45, -33], [49, -12, 15], [13, -20, -11], [-44, 47, -49], [-16, 33, 45], [-39, 11, -27], [34, 46, -33], [17, -49, 15], [16, -38, -36], [-45, 7, -17], [26, 10, 5], [19, -29, 39], [-49, 19, -17], [-39, 2, 21], [49, 34, -36], [-22, -29, 42], [-44, -1, -49], [-22, 12, 29], [42, -14, -4], [24, 45, 23], [9, 11, 29], [24, -38, -33], [-15, -3, 22], [2, -10, 31], [26, -34, 14], [-36, 44, 31], [41, 20, -1], [-15, 50, -7], [-5, 12, 46], [-31, -3, -10], [19, 38, 6], [-37, 44, -34], [5, 3, 13], [48, -45, 15], [44, 20, -33], [16, -22, -13], [26, 35, 28], [18, 27, 20], [-48, -35, -49], [-39, 30, 15], [33, 37, -2], [-7, 50, -36], [19, -29, -2], [24, -31, 40], [1, 2, -25], [12, -26, 39], [17, 34, 46], [-16, 50, 39], [3, 38, 14], [43, 45, -42], [-13, -11, 39], [-32, -6, 45], [-48, 12, -50], [1, 12, 45], [-48, 2, -42], [-8, 11, -50], [-7, -22, -50], [-15, -45, -35], [5, -35, 7], [-32, -49, -25], [3, -37, -19], [25, -42, 23], [43, -9, -33], [-39, -3, -1], [33, 10, 23], [-47, -13, -20], [-7, -1, 31], [-5, -34, 15], [2, -21, -41], [9, -13, -19], [-40, 17, 3], [32, -31, 11], [40, -1, -2], [8, 11, 13], [-38, -21, 47], [-7, 42, -23], [1, 31, -33], [2, 12, -11], [16, -45, -50], [8, -24, 36], [-48, 31, -25], [-48, 37, 38], [-32, 18, 46], [16, -8, 20], [-8, 45, 7], [-15, -45, 25], [48, 11, -28], [-22, 27, -2], [24, -7, 28], [-16, -38, 46], [17, -50, 38], [-40, -29, -17]]
    n = 50

    bulk_test_template([instance], n)

def write_blockages_demo():
    clauses = [
        [1, 2, 3],
        [1, 2, -3],
        [1, -2, 3],
        [1, -2, -3],
        [-1, 2, 3],
        [-1, 2, -3],
        [-1, -2, 3],
        [-1, -2, -3],
    ]
    write_blockages(clauses, 3)

def small_unsat_demo():
    clauses = [
        [1, 2, 3],
        [1, 2, -3],
        [1, -2, 3],
        [1, -2, -3],
        [-1, 2, 3],
        [-1, 2, -3],
        [-1, -2, 3],
        [-1, -2, -3],
    ]
    n = 3
    is_sat_from_baseline = is_satisfiable(clauses, n)
    is_sat_from_algo = process(clauses, n)

    print("[DEMO] Unsatisfiable instance")
    print("Does the (exponential) baseline say it's satisfiable?")
    print(is_sat_from_baseline)
    print("Does the algorithm say it's satisfiable?")
    print(is_sat_from_algo)

def small_sat_demo():
    clauses = [
        [1, 2, 3],
        [1, 2, -3],
        [1, -2, 3],
        [-1, 2, 3],
        [-1, 2, -3],
        [-1, -2, -3],
    ]
    n = 3
    is_sat_from_baseline = is_satisfiable(clauses, n)
    is_sat_from_algo = process(clauses, n)

    print("[DEMO] Satisfiable instance")
    print("Does the (exponential) baseline say it's satisfiable?")
    print(is_sat_from_baseline)
    print("Does the algorithm say it's satisfiable?")
    print(is_sat_from_algo)

# Note: this takes far too long to run
# large_instance_demo()

small_unsat_demo()

small_sat_demo()

write_blockages_demo()
