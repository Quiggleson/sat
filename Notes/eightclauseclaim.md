Given some axioms
...

Proven by lemma: In any instance of 3SAT with more than eight clauses, 
there will be assignments blocked by more than one clause
and we can expand the instance by adding ghost clauses
which are implied by the given clauses 

Claim: And if the expanded instance is not satisfiable, it will
contain a pattern of eight clauses in which all assignments are
blocked by exactly one of these clauses

Consider the eleven clause instance: 
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

Here are the assignments blocked by more than one clause:

| Blocked | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| 2 | 0 | 0 | 0 | 0 | 1 | 1 |
| 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 | 0 | 1 | 0 |
| 2 | 0 | 0 | 1 | 0 | 1 | 1 |
| 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 | 0 | 1 | 0 |
| 2 | 0 | 1 | 0 | 0 | 1 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 1 | 0 |
| 2 | 1 | 0 | 0 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 0 | 1 | 0 |
| 2 | 1 | 0 | 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 0 | 0 | 1 |
| 2 | 1 | 1 | 0 | 0 | 1 | 0 |
| 2 | 1 | 1 | 0 | 0 | 1 | 1 |

There are 24 assignments here, meaning it will take three clauses to block each
of these assignments exactly once

Idea 2 - check the remaining 40 assignments, do the clauses that block those 
assignments even make it possible for the eight clause pattern to exist
that blocks each assignment exactly once?

Idea 2 is irrelevant, this is the simplest form of the instance, meaning each clause is required for it to be unsatisfiable, therefore each of the eleven clauses blocks
at least one of the remaining 40 assignments

Hmmm we've got 24 assignments and three ideal clauses that could exist
hold I'm gonna code something to 1) check if an instance contains the eight
clause pattern and 2) make a program to iterate through all eight clause
instances of 3sat for up to 48 (or prove a lower number?) terminals.

Thoughts on 2) - we know of a single eight clause pattern that blocks all
assignments, but there may be more instances or a more general pattern
If an eight clause pattern exists, it will be discovered if we search all
eight clause instances with n = 48 because
 - the eight clause pattern that uses seven terminals will be discovered
because 48 > 7
 - The most general pattern has 24 terminals, but some could be negated so 
we double it

Proving it's less than 48:
Without repeating variables, we can make a pattern:
[1, 2, 3], 
[4, 5, 6],
[7, 8, 9],
[10, 11, 12],
[13, 14, 15],
[16, 17, 18],
[19, 20, 21],
[22, 23, 24]

If we were to negate one terminal, it would be logically equivalent because
we never see the same terminal twice

If we were to see the same terminal twice, negation would not add any 
additional terminals to consider since we can only negate variables we 
are already considering

Therefore the most general pattern of eight clauses that block all assignments
uses at most 24 terminals

Less than 24:
WTS negation of existing terminals is required
Idea: [22, 23, 24] can be replaced by negating existing terminals
Consider the assignment $x_1 = x_2 = ... = x_n = 1$
This can only be blocked... idk

Let's approach this by building it up.
The first clause is chosen as an arbitrary starting point
[1, 2, 3]
The next clause exists based on the following rules:
 - It must block $2^{n-3}$ assignments new
 - It cannot contain the same terminal twice (no [1, -1, 2])
 - When introducing a new terminal, use its positive form

Next clauses cannot:
 - contain only new terminals since any clause with only new terminals
would block an already blocked assignment

This implies at least one terminal has to exist from clause to clause
[1, 2, 3]
[-3, 4, 5]
[-5, 6, 7]
[-7, 8, 9]
[-9, 10, 11]
[-11, 12, 13]
[-13, 14, 15]
[-16, 17, 18]

New max number of terminals is 18

New clauses can:
 - Contain two new terminals iff it contains the negated form of an existing 
terminal
 - Contain one new terminal iff it contains the negated form of an existing
terminal
 - Be identical to an existing clause differing by at least one negation

Take [-3, 4, 5] as the next clause, then [-5, 6, 7] IS NOT VALID

Given the first two clauses
[1, 2, 3]
[-3, 4, 5]
The next clauses

can:


cannot:
 - what attribute does [-5, 6, 7] break?

** new clauses must always contain a negated terminal from the first clause **

[1, 2, 3]
[X, 5, 6]
[X, 7, 8]
[X, 9, 10]
[X, 11, 12]
[X, 13, 14]
[X, 15, 16]
[X, 17, 18]

where X is -1, -2, or -3

But if the first two clauses are
[1, 2, 3]
[-3, 4, 5]

then the clause [-3, 6, 7] is not a valid clause because it violates
"new clauses must always contain a negated terminal from the first clause"
where "first clause" is more generalized to "every other clause"

# The Rule: each clause must always contain a negated termianl from every other clause

Try to get more than 7 terminals:

[1, 2, 3],
[-1, 4, 5],
[-1, -4, 6],
[-1, -5, 4],
[-1, -4, -6],
[-2, 1, 7],
[-2, 1, -7],
[-3, 1, 2]

It is impossible to get more than 7 terminals, each decision is forced

The eleven clause instance:
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

Which clauses break the rules?
[4, 5, 6] - this blocks assignments already blocked by [1, 2, 3]
what does this imply?

All blocked assignments:
| Blocked | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|
| 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

More rules:
If we have two clauses
[1, 2, 3]
[4, 5, 6]

what additional requirements are needed to make it unsatisfiable?
We need at least seven more clauses, clearly this can be done by
making the eight clause pattern around [1, 2, 3] in which case [4, 5, 6]
would be made redundant, shoot.

How can we expand the instance based on implications of ghost clauses?
Let's go back to the implications

The eleven clause instance does not follow the rules, but there are two
sets of clauses which do follow the rules and they share a clause that
follows the rules for both sets

Perhaps it's as simple as eight sets of clauses that follow the rules and
each set has to be connected to each other set?
Each of the eleven clauses is critical, how can we show that removing one
makes the instance invalid? (invalid meaning does not contain the eight 
clause pattern and is thus satisfiable)

Remove [1, 2, 3]
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

We now have 6 clauses in the set around x_2 and the 4-clause set around x_4
is attached via [-2, -3, -4]

You take one clause out [-2, -3, 4] and have to replace it with all of the
clauses that block instances based on that third terminal (here it's x_4), but
since there are four clauses that are required to block all cases where
x_4 = 0, there will be overlap
But we know [-2, -3, 4] blocks at minimum what the four clauses containing x_4
block
Therefore we can add [-2, 3, 4] as a ghost clause and the four clause pattern
can be seen
The four clauses with x_4 are actually much stronger, we can block any clause
containing x_4. In essence we can assign x_4 = 1 and remove that terminal
from the instance

Then we're left with list(n) = 1, 2, 3, 5, 6
and 
[1, 2, 3]
[1, 2, -3]
[1, -2, 3]
[-1, 2, 3]
[-1, 2, -3]
[-1, 2, 3]
[-2, -3, X]
[-2, -3, -X]

Based on the pattern, X can be any terminal in the instance and since
we have the clause [-2, -3], this blocks any assignment where 
$x_2 = x_3 = 0$ which includes the clauses [-2, -3, X] where X is not 
only any terminal, but can validly be replaced by each and every
terminal

So now we know of this eight clause pattern and we know how to deal
with sets of four clauses that 1) follow The Rule and 

If a set of clauses does not follow the rule then there will be overlap
and four clauses will not force a value assignment to a single terminal
Or in a two clause set, it will not force the 

What about an instance where there are 8 sets of two clauses and each
follows the rule within it's set and among every other set?

[1, 2, 3],
[-1, 4, 5],
[-2, -4, 6],
[-1, -4, -6],
[-1, -5, 4],
[-2, 1, 4],
[-3, 1, 2]

well crap

We have an instance with seven clauses and each
assignment is blocked exactly once, however there
are eight clauses left and the only constant
terminal between all eight is x_4

1) How can we tell from the instance that
x_4 would only have the possible value of 1?

2) Unless we added two clauses that implied the
eighth clause

3) Welp there is no eight clause solution

| Blocked | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 | 1 | 0 |

What if we added
[1, -2, -4]
[-1, 2, -4]

Then we have a nine clause solution 
[1, 2, 3],
[-1, 4, 5],
[-2, -4, 6],
[-1, -4, -6],
[-1, -5, 4],
[-2, 1, 4],
[-3, 1, 2],
[1, -2, -4],
[-1, 2, -4]

How can we find the eight clause pattern?
Looks like [4, 1, 2] or the pattern is different
in the clauses with -4, is it enough to limit it?
These four clauses do not follow the rules, there is overlap
How many clauses follow the rules?


Sort:
0  [-4, -2, 6],
1'  [-4, -1, -6],
2' [4, 1, -2],
2  [-4, 1, -2]
3  [-4, -1, 2]
2  [4, -1, 5],
4  [4, -1, -5],
1  [1, 2, 3],
1  [-3, 1, 2]

There are four sets of clauses st within each sets the rules are followed
and there is at least one clause in each set that follows the rules with
at least one clause from every other set

clauses with 4:

[-1, 4, 5]
[-2, -4, 6]
[-1, -4, -6]
[-1, -5, 4]
[-2, 1, 4]
[1, -2, -4]
[-1, 2, -4]

what clauses imply x_4 cannot be 0?
what clauses block assignments with x_4 = 0?

These clauses are required to force a value
for x_4

[1, 2, 3],
[1, 2, -3]
[-1, 4, 5],
[-1, 4, -5],
[-2, 1, 4],

[1, 2]
[-1, 4]

Why do they force a value for x_4?
The implication [-1, 4] blocks assignments
where x_4 = 0, x_1 = 1
The implication [1, 2] blocks assignments
where x_2 == x_1 = 0
Therefore the clause [-2, 1, 4] cannot be assigned
x_4 = 0 and x_1 = 1 or x_2 = 0 and x_1 = 0

Interesting, it seems that the implications of 
values for two terminals may be such that it 
implies if the terminals are the same or different
as opposed to hardcoded "x_1 = 0; x_2 = 1"
Clearly not

Does [1, 2] [-1, 4] really imply [2, 4]? yes

Ah, [2, 4] means at least one has to be true and in order to satisfy [-2, 1, 4]