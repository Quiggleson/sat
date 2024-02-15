# Usage

## Benchmarks

A list of benchmark problems can be found [here](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html)

Currently, it only supports satisfiable instances but you could probably modify ``readcnf.py`` to read both kinds of instances

Download the .tar.gz file from the list of benchmark problems and unpack them into a directory called /inputs in the /Scripts directory

Then run ``python3 readcnf.py`` to test all the instances

It takes around 60 seconds to process a 20-terminal instance

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