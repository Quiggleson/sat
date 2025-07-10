# Notes

## Initial Implication Graph

3-t expands to n-t clauses which reduce to 1-t clauses

Each n-t clause has a corresponding assignment st

- negative terms <-> True assignment
- positive terms <-> False assignment

example

A := [a, -b, c, d, -e, ...]

implies b and e are True and a, c, d are False in the blocked assignment.

Consider the given 3-t clauses, 

- negative terms <-> True assignment
- positive terms <-> False assignment

3-t clauses block all assignments which set the three terms in the clause to False. There are 2^{n-3} assignments blocked by each 3-t clause.

B := [a, b, c]

C := [+- a, +- b, +- c, ...] ?

Therefore we can expand all the given 3-t clauses to all possible n-t clauses.

Now want to show we can reduce to 1-t clauses:

Recall we have every possible n-t clause (all 2^n of them).

A := [a, b, c, ....]

B := [-a, b, c, ...]

C := [b, c, ...]

..

D := [z]

E := [-z]

Known:

- z could either be in a given 3-t clause or not

Consider the 8 clauses which hold all combos of a, b, c and we have the terminal d as well.

The 8 clauses block all assignments, but if we pop a, b, and c from the n-terminal clauses then we will be left with [d] and [-d], but d exists nowhere in the instance.


At this step, we can derive *any* pair of contradicting 1-terminal clauses

[a] [-a]
[b] [-b]
[c] [-c]
[d] [-d]

What are the benefits of one pair over the other?

 - order of popping
   - let's say it takes exponential time to derive the d pair, we may be able to rearrange the graph and pop d first to derive the a pair in poly time

We lose some strength in restricting the graph to exclude expansion as we can no longer derive every pair of contra 1-t clauses. We can only derive contra 1-t clauses containing terms which exist in the given clauses.


Known

 - Every term in the (expansionless) implication graph exists as positive in one clause and negative in the other

It's a matter of rearranging the implication graph to limit the length of the processed clauses

## Expansionless Implication Graph

WTS the initial implication graph can be rearranged as to derive contra 1-t clauses without expansion

NOTE: the initial implication graph can derive all possible contra 1-t clauses, however this graph will be limited. Will this be a problem?

This will only be a problem if all contra 1-t clauses can no longer be derived. As long as this graph allows for the derivation of at least one pair of contra 1-t clauses, then we still have the goal (recall WTS unsat instance -> contra 1-t clauses can be derived in poly time).

1) WTS expansion can be delayed until the last step
2) WTS expansion is unnecessary

Consider the 3-t to n-t expansion and reduction to n-1-t

A (3-t) -> C (n-t)
B (3-t) -> D (n-t)
C and D => E (n-1-t)

where x in C and -x in D

if x not in A, then A can expand to E
if -x not in B, then B can expand to E
if x if A and -x in B, then A and B imply a new clause, F (len 2-4), which expands to E

In the initial implication graph, we are free to pop terms in any order. With the new graph, we are limited to pop terms which exist.

The initial would expand to n then we could pick the term to pop for the n-1, n-2, n-3, ..., 3, 2, 1 clauses

Now to derive the n-1, we either

(1) expand a given 3-t to n-1 or
(2) combine two 3-t's to imply a clause which can expand to n-1

and to derive n-2, we either

(1) expand a given 3-t
(2) combine two given 3-t's and expand to n-2
(3) combine a given 3-t and a derived 2-4-t and expand to n-2
(4) combine two derived 2-4-t and expand to n-2

and to derive n-3, we either

(1) expand a given 3-t
(2) combine two clauses, each of which have been a part of 0, 1, or 2 implications

and to derive a n-k clause, we either

(1) expand a given 3-t
(2) combine two clauses, each of which have been a part of 0 to k-1 implications

What if the implications get longer than an n-k-t clause?

When would that happen?

Consider the 1-terminal clauses. The input clauses are a maximum of n-2 steps away from a given 3-t clause.

Consider the placements of the given 3-t clauses in the implication graph. Would you ever reuse a clause?

The clause

A := [a, b, c]

can be used to derive

B := [a, c, d, ....] (n-2)

and

C := [b, e, f, ...] (n-3)

what if it's used to derive

[a, b] which derives [a]

and

[b, c] which goes on to derive [c] which pops -c from [-a, -c] and

it looks like yes clauses can be reused