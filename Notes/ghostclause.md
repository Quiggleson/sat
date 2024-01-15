Consider once again the 11 clause unsatisfiable instance <br>
Clauses:
[1, 2, 3]
[1, 2, -3]
[1, -2, 3]
[-1, 2, 3]
[-1, 2, -3]
[-1, -2, 3]
[4, 5, 6]
[4, 5, -6]
[4, -5, 6]
[4, -5, -6]
[-2, -3, -4]

Algo: 
Look for four clause patterns and make note of required values
Make ghost clauses if possible
Look for three/two clause patterns that require a value for two terminals
Make ghost clauses based on this info (two assigned + one assigned = 1 clause)
Keep repeating until no ghost clauses are made or the eight clause all blocking
pattern is known

Four clause pattern: <br>
check term 1 - no pos, no neg <br>
check term 2 - yes pos, no neg <br>
check term 3 - yes pos, no neg <br>
check term 4 - yes pos, no neg <br>
check term 5 - no pos, no neg <br>
check term 6 -  no pos, no neg <br>

The following are blocked: <br>
$x_2 = 0$ <br>
$x_3 = 0$ <br>
$x_4 = 0$ <br>

clearly adds the ghost clause [2, 3, 4], new instance becomes
[1, 2, 3]
[1, 2, -3]
[1, -2, 3]
[-1, 2, 3]
[-1, 2, -3]
[-1, -2, 3]
[4, 5, 6]
[4, 5, -6]
[4, -5, 6]
[4, -5, -6]
[-2, -3, -4]
[2, 3, 4]

This does not allow for any new four clause patterns since pos 2, 3, 4
were already discovered

Two clause patterns - any assignment with two terminals constant and the 
other flipping signs: <br>
term 1 - [1, 2], [1, 3], [-1, 2], [-1, 3] <br>
term 2 - [2, 3], [2, -3], [-2, 3] <br>
term 3 - <br>
term 4 - [4, 5], [4, -5], [4, 6], [4, -6] <br>
term 5 - <br>
term 6 - <br>

hmm no new blockages

but we know [2], [3], [4] cannot exist so we can make more ghost clauses <br>
This makes three clauses per two terminal block, 33 "new" clauses - invalid clauses <br>

new instance: 
does this have the eight clause pattern?


[1, 2, 3] 
[1, 2, 4] 
[1, 3, 4] 
[-1, 2, 3] 
[-1, 2, 4] 
[-1, 3, 4] 
[2, 3, 4] 
[2, -3, 4] 
[-2, 3, 4] 
[2, 4, 5] 
[3, 4, 5] 
[2, 4, -5] 
[3, 4, -5] 
[2, 4, 6] 
[3, 4, 6] 
[2, 4, -6] 
[3, 4, -6] 

[1, 2, 3]
[1, 2, -3]
[1, -2, 3]
[-1, 2, 3]
[-1, 2, -3]
[-1, -2, 3]
[4, 5, 6]
[4, 5, -6]
[4, -5, 6]
[4, -5, -6]
[-2, -3, -4]

combined:

[1, 2, 3],
[1, 2, 4], 
[1, 3, 4], 
[-1, 2, 3], 
[-1, 2, 4], 
[-1, 3, 4], 
[2, 3, 4], 
[2, -3, 4], 
[-2, 3, 4], 
[2, 4, 5], 
[3, 4, 5], 
[2, 4, -5], 
[3, 4, -5], 
[2, 4, 6], 
[3, 4, 6], 
[2, 4, -6], 
[3, 4, -6], 
[1, 2, -3],
[1, -2, 3],
[-1, 2, -3],
[-1, -2, 3],
[4, 5, 6],
[4, 5, -6],
[4, -5, 6],
[4, -5, -6],
[-2, -3, -4]

Search for the pattern
Try each terminal as $x_1$ - does it appear as 4 pos and 4 neg?:
term 1 - yes
term 2 - yes pos, no neg
term 3 - yes pos, no neg
term 4 - yes pos, 
term 5
term 6

dang, doesn't matter - yes it does you dum dum, [-2, -3, -4] is part of the 8 clause pattern <br>
the clause [-2, -3, -4] is critical - removing it makes it satisfiable <br>
Therefore, a pattern that blocks everything must include that clause <br>
And since

unless there's another two clause pattern <br>
Consider the clauses <br>
[-2, -3, -4] <br>
[2, -3, 4]

What can we gather from this? <br>
Replace it with [-1, -2, -3], [1, -2, 3] <br>
This blocks assignments with
$x_1 = x_2 = x_3 = 1$ and
$x_1 = x_3 = 1; x_2 = 0$
This blocks all $x_2$'s where $x_1 == x_3$

Meaning... what pattern do we care about or ghost clause can we make?

If we see this two clause pattern, we know assignments where $x_2 == 1$ and 
$x_1 == x_3$ are blocked

What was the original goal again?
Find the simplest pattern that blocks all assignments - a pattern that exists
in all unsatisfiable instances
OR
Prove that no such pattern exists

Forget like everything from the past 30 lines, <br>
Since [-2, -3, -4] is a critical clause, the pattern must contain that
so try three instances: 1) remove all clauses without 2, 2) remove all
clauses without 3, 3) remove all clauses without 4

keep 2:

[1, 2, 3],
[1, 2, 4], 
[-1, 2, 3], 
[-1, 2, 4], 
[2, 3, 4], 
[2, -3, 4], 
[-2, 3, 4],
[2, 4, 5], 
[2, 4, -5],  
[2, 4, 6], 
[2, 4, -6],  
[1, 2, -3],
[1, -2, 3],
[-1, 2, -3],
[-1, -2, 3],
[-2, -3, -4]

keep3:

[1, 2, 3], 
[1, 3, 4],
[-1, 2, 3], 
[-1, 3, 4], 
[2, 3, 4], 
[2, -3, 4], 
[-2, 3, 4], 
[3, 4, 5], 
[3, 4, -5], 
[3, 4, 6], 
[3, 4, -6], 
[1, 2, -3],
[1, -2, 3],
[-1, 2, -3],
[-1, -2, 3],
[-2, -3, -4]

keep 4:

[1, 2, 4], 
[1, 3, 4], 
[-1, 2, 4], 
[-1, 3, 4], 
[2, 3, 4], 
[2, -3, 4], 
[-2, 3, 4], 
[2, 4, 5], 
[3, 4, 5], 
[2, 4, -5], 
[3, 4, -5], 
[2, 4, 6], 
[3, 4, 6], 
[2, 4, -6], 
[3, 4, -6], 
[4, 5, 6],
[4, 5, -6],
[4, -5, 6],
[4, -5, -6],
[-2, -3, -4]

All of those instances are satisfiable, meaning the eight clause pattern
does not apply to all unsatisfiable instances 
OR
The 11-clause instance can be expanded more