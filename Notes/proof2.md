extra space for proof notes

WTS unsatisfiability -> contradicting 1-t clauses can be derived via
reduction/expansion using only reduction/expansion to clauses of length
k = 1, 2, 3, 4

We know from Lemma A that an unsatisfiable instance can be expanded to
2^n unique n-terminal clauses.

Lemma B: given two clauses of length k, if they are identical
except for one negated terminal, this implies a (k-1)-t clause as
well as additional k-t clauses. Deriving the (k-1)-t clause is known
as reduction and deriving the additional k-t clauses is known as expansion.

WTS we cannot get more data from reducing/expanding derived clauses

Consider a satisfiable instance
WTS reducing two derived clauses never results in more info
Suppose not. Then there exists two derived clauses whose reduction will
result in more info
Consider the following derived clauses
[1, 2, 3, ...]
[-1, 2, 3, ...]
these reduce to 
[2, 3, ...]
which can be expanded to
[2, 3, ..., i]
[2, 3, ..., -i]
for all i that's not in the clause and 1 <= i <= n
but since these are derived clauses, there exist given clauses of length
(k-1) that imply the two derived clauses


Consider an unsatisfiable instance
