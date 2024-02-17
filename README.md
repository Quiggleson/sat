# Usage

## Benchmarks

A list of benchmark problems can be found [here](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html)

Run ``readcnf.py`` to iterate through the files in ``/inputs`` or ``/UUF50.218.1000`` (you have to unzip satisfiable instances into ``/inputs`` or unsatisfiable instances into ``/UUF50.218.1000`` and call the function at the bottom of the file)

Currently there's a bug with the unsatisfiable benchmark problems with the ``optimize.py`` solution, but it's being looked into

## Script Usage

``checkimplications.py`` is the main script to check if algorithms work
 
 - the bottom is hecka messy right now, but ``gen_random_instance()`` will generate a list of random instances of 3SAT and you can try different functions using that list
 - ``solve_gen()`` and ``solve_expand()`` are old solve functions that use lists of lists, they should be accurate, but slow (8 hours for 1000 10-terminal instances iirc?)
 
``optimize.py`` is the newest script to attempt a O(n^6) runtime
 - pass the instance as a list of lists into ``process()`` and it will return a bool: False for unsatisfiable, True for satisfiable

``main.py``
 - ``write_blockages()`` will write a md file of the assignment table and instance as well as return True (satisfiable) or False (unsatisfiable) for the input instance
   - it will overwrite existing files, it was not made for robustness in that regard

most other functions are depracated, I haven't had the chance to clean it up yet