# Overview

## Current Status

This repo has a bunch of neat ideas, but does not have a proven working polynomial time solution to solve 3SAT. 

It attempts to process an instance and keep implying new clauses until it either 1) derives a set of clauses which imply the instance is unsatisfiable or 2) run out of new clauses to imply.

As described below, `v2_utils.process(instance, max_length)` aims to return a bool indicating if the instance is satisfiable. When tested with `max_length == 3`, this returns false positives. If it can be shown that there exists a fixed value for `max_length` that is independent of the number of terminals, then P = NP.

## Requirements

1. Navigate to the `Scripts` directory

  ```
  cd Scripts
  ```

2. Create a virtual environment

  ```
  python3 -m venv .venv
  ```

3. Install the requirements

  ```
  pip install -r requirements.txt
  ```

## Benchmarks

A list of benchmark problems can be found [here](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html)

Run ``readcnf.py`` to iterate through the files in ``/inputs`` or ``/UUF50.218.1000`` (you have to unzip satisfiable instances into ``/inputs`` or unsatisfiable instances into ``/UUF50.218.1000`` and call the function at the bottom of the file)

## Script Usage

`baseline_solver.py`
 - `write_blockages(instance)`
   - writes a file, `blockages.md` with information about the given instance
   - Displays the following:
     - instance size
     - instance clauses
     - blocked assignments (and how many times each one is blocked)
     - whether it's satisfiable
 - `is_satisfiable(instance)`
   - simply returns a bool indicating whether the given instance is satisfiable
   - This is a baseline check done in exponential time

`v2_utils.py`
 - `process(instance (as list of lists), max_length)`
   - This is the only function you have to directly call
   - This processes an instance according to the ideas outlined below
   - It returns a bool indicating whether `instance` is satisfiable
     - Note: currently throws out false positives if `max_length == 3`
 - `todict(instance (as list of lists))`
   - Converts the given list of lists into an object similar to a [Trie](https://en.wikipedia.org/wiki/Trie) fine tuned to support sets
   - See [Rope Example](<Dev Notes/ropeexample.txt>) for an example and explanation
 - `check_sat(instance (as Trie-esque data structure))`
   - Keep adding implied clauses to the instance until you either
      a. derive contradicting 1-terminal clauses or
      b. can't imply any new clauses
   - Return a bool indicating whether `instance` is satisfiable
     - Note: currently throws out false positives if `max_length == 3`
   - Read the section Important Ideas below

`main.py`
 - Has a few demo functions, showcasing `write_blockages()` and `process()`

## Important Ideas

This section has a quick overview of the ideas used in this repo. If you want a highly detailed explanation, read the [paper](Documents/quigley_main.pdf) in Documents.

1. An instance of 3SAT can be blocked (from being the satisfying assignment) by a clause
2. Clauses in the instance can imply new clauses in the following ways:
   1. Implication: if two clauses contain the same term which is positive in one clause and negated in the other, then they imply a new clause which contains all the remaining terms in either clause (excluding the opposite form terms)
      1. ex, `[-1, 2, 3]` and `[1, 4, 5]` imply `[2, 3, 4, 5]`
   2. Reduction: if two clauses in an implication are identical except for the opposite form term, the implied clause's length will be one less than the input clauses
      1. ex, `[-1, 2, 3]` and `[1, 2, 3]` imply `[2, 3]`
   3. Expansion: given a clause and a term not in that clause, you can append that term to the clause without blocking any additional assignments
      1. ex `[1, 2, 3]` implies `[1, 2, 3, 4]`
3. Using the different types of implications, we can keep adding clauses to the instance without changing whether it's satisfiable
4. If we derive two clauses which contain a single term each and that term is positive in one clause and negated in the other, the instance is unsatisfiable. Call these contradicting 1-terminal clauses.
   1. In other words, `[a], [-a]` is in the instance for some `a` in the set of terminals
5. Ideally, we'd find a way to continually process all the clauses until we either 1) derive the contradicting 1-terminal clauses or 2) know that there is no way to derive these clauses (as such, the instance would be satisfiable)

## Tests

Run `pytest` to run tests