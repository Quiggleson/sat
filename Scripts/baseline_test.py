from baseline_solver import is_satisfiable
import pytest

def test_zero_indexed_clauses():
    clauses = [[0, 1, 2], [3, 4, 5], [-2, 4, 5]]
    n = 5
    with pytest.raises(TypeError):
        is_satisfiable(clauses, n)

def test_satisfiable_instance():
    clauses = [[1, 2, 3], [1, 2, -3], [-1, 2, -3], [-1, -2, -3]]
    n = 3
    assert is_satisfiable(clauses, n) == True, "a satisfiable instance was returned as unsatisfiable"

def test_unsat_instance():
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
    assert is_satisfiable(clauses, n) == False, "an unsatisfiable instance was returned as satisfiable"
