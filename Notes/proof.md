WTS this algorithm works for all cases
algo 2:
```
(0) Get all three-terminal implications
(1) Get all two-terminal implications
(2) Get all one-terminal implications
(3) Expand all one terminal implications
(4) Expand all two terminal implications
(TODO) expand all three terminal implications
(5) Repeat 1-4 until you have no more implications
(6) If there exists contradicting one-terminal implications, 
    it is not satisfiable
    Otherwise, it is satisfiable
~~(6)~~ Solve like before, assigning values where they are forced from one-term
    clauses, or trying both values from two-term clauses

```

We have to go to 4-t clauses because there is information between 
existing 3-t clauses and new 3-t clauses that can only be 
extracted by expanding to 4-t clauses then reducing to 3-t again

Lemma -_-: if you want to add an additional clause of length k, you
need to expand the current clauses of length k to clauses of 
length k + 1 and then reduce to k

Proof for Lemma -_-: idk about this yet

Lemma A: given an instance of 3SAT, you can expand all of the 
given clauses to the point where you are considering clauses
of length n. Iff you have 2^n unique n-terminal clauses, it 
will be unsatisfiable

WTS
2^n unique n-terminal clauses -> unsat instance
clearly true
if you have 2^n unique n-terminal clauses, each clause blocks one
assignment and since they are unique, each clause blocks a unique
assignment.
Therefore, 2^n assignments will be blocked and the instance is 
unsatisfiable

unsat instance -> 2^n unique n-terminal clauses can be derived
Suppose not. 
Then we have an unsatisfiable instance in which 2^n unique
n-terminal clauses cannot be derived
This means there is at least one n-terminal clause which cannot
be reduced to a given 3-t clause.
Since each n-terminal clause represents an assignment, this is
saying there exists an assignment which is not blocked by a 
given 3-t clause
If there exists an assignment which is not blocked, then that
assignment satisfies the instance.
This means the instance is satisfiable, however it was given
that we have an unsatisfiable instance #

Lemma A is true

Lemma B: given two clauses of length k, if they are identical
except for one negated terminal, this implies a (k-1)-t clause as
well as additional k-t clauses

Proof for B:
Given 
C_1 = [a, b, c, ..., w]
C_2 = [-a, b, c, ..., w]
where C_1 and C_2 only differ by the negated a, 
this implies the clause
C_3 = [b, c, ..., w]
where C_3 is identical to C_1 and C_2 without the a terminal
since half of the assignments blocked by C_3 have a = 1 and half
of the assignments blocked by c_3 have a = 0, if we know from
C_1 and C_2 that both of these types of assignments are blocked, 
then we know that all assignments blocked by C_3 are blocked

Then in assignments blocked by C_2, you can select
a terminal and exactly half will assign that terminal the 
value 0 and the other half will assign that terminal 1.
This is true for all terminals that are not in the clause by Lemma E.
This allows you to create clauses from C_2 that are identical to
C_2, but there is an additional terminal, say y st y and -y is
not in C_2, that is added to C_2 (in both positive and negative
forms)
For example, 
[1, 2, 3] implies
[1, 2, 3, x]
[1, 2, 3, -x]
for all 1 <= x <= n and x =/= 1, 2, 3

Lemma B is true

Main goal: WTS reducing/expanding between k = 1, 2, 3, 4 is just 
as powerful as expanding k up to n

Claim: an instance is unsatisfiable iff contradicting 1-t clauses
can be derived (in poly time - via reduction/expansion)

contradicting 1-t clauses -> unsatisfiability
clearly true
a 1-t clause forces a value for one terminal.
If two 1-t clauses force different values for the same terminal, 
a satisfying assignment could not have any value for that terminal
and since every possible assignment has a value for that terminal,
the instance is unsatisfiable

unsatisfiability -> contradicting 1-t clauses can be derived via
reduction/expansion within k = 1, 2, 3, 4

Suppose not. Then we have an unsatisfiable instance in which we
reduce/expand all clauses between lengths 1 and 4 and it does not
produce contradicting 1-t clauses

We know if we expand to k = n, we will eventually come across a
clause of length w (where w is fixed but arbitrary k <= w <= n)
which can directly expand to n

WTS that if we use reduction and expansion, the highest w that
will expand to block all instances iff it's unsatisfiable is 
w = 4

I think the idea has to come from the fact that there will
be information between given 3-t clauses and derived 3-t clauses
that can only be extracted from using 4-t clauses...
and this is not applicable for 4-t clauses because there are no
4-t clauses- they are all derived!

Lemma  C: 

WTS the information between existing 3-t clauses and derived
3-t clauses... nah hold up, prove the inverse

WTS information between two derived clauses will never be 
able to create a new clause of the same length. You must use
an existing clause to create a new clause

Suppose not. Then there exists two derived clauses of length k
that imply a new clause of length k
... what is meant by 'new clause'?
CONTINUE THIS PROOF

recall every clause of length >= 4 must be derived

For every derived clause, you can trace back the implications
to existing clause(s)

So if you were to expand these derived clauses, you would get
to the point where k = n

If at this point there is a clause of length n (equivalent to 
an assignment) that can be traced back to the "new clause" from
the derived clause and those derived clauses can be traced back
to the given 3-t clauses

Cleanup and redo:

Suppose not. Then there exists two derived clauses of length
k >= 4 that imply a new clause, C st the assignments blocked by C
are only blocked by clauses based on C.

...---

WTS you can use given 3-t clauses in addition to derived 3-t 
clauses to derive new 3-t clauses that block an assignment ?

Lemma D: an instance of 1SAT is unsatisfiable iff it contains two clauses
where the same terminal is positive in one and negated in the other.

Proof:
WTS  unsatisfiable -> the same terminal exists like [-x], [+x]
suppose not. Then the instance is unsatisfiable, but does not contain two
clauses like described. This means a terminal may appear exactly once, 
regardless of positive or negative.
Now, each terminal may appear at most once and the instance is unsat
Note that each clause blocks at most half of the possible assignments
and after the first clause, every additional clause will block at least one
assignment that has already been blocked by the first clause.
Stronger: use Lemma E
The first clause blocks 2^{n-1} assignments.
Aside: there are now n-1 terminals whose values could be 0 or 1 as the terminal
in the clause has its value set.
2^{n-1} = 2^n/2^1 = 2^n/2
so the first clause blocks half of the assignments
the second clause also blocks (2^n)/2 assignments, but there is some overlap.
By Lemma E, since we have a set value for the second clause's terminal, we 
know that half of those assignments overlap with the assignments blocked
by the first clause
So the second clause only blocks an additional (2^n)/2 - 2^{n-2}
(2^n)/2 - 2^{n-2} = (2^n)/2 - (2^n)/2^2 = (2^n)/2 - (2^n)/4 = (2^n)/4
The second clause blocks an additional 1/4 of the possible assignments.
The third clause blocks the initial 2^n/2 assignments, but subtract out overlap
between the first two clauses
The pattern is seen:
2^n/4 of the assignments are repeated by the first clause and
of the 2^n/4 new assignments blocked by the second clause, half of those are 
blocked by the third clause. So the formula is 
total blocked - shared with first clause - shared with second clause
= 2^n/2 - 2^n/4 - 2^n/8
= 1/8 of the assignments are now blocked by this clause

The pattern is seen that for each new clause, q, there are 
1/2^q new assignments blocked

(maybe unnecessary) Recall we know at most there are n assignments if we use each terminal the maximum number of times. 

Since each new clause blocks half of the assignment before it and we have a 
natural number of terminals, it will never block all 2^n assignments

WTS the same terminal existing like [-x], [+x] -> unsat
clearly true, these clauses block every possible assignment

Lemma D has been proven correct

Lemma E: Given a clause, C, then for every terminal not in C, half of the 
assignments blocked by C have that terminal's value set to 0 and the other
half have that terminal's value set to 1.

Proof:
We have 2^n possible assignments, one for each possible combinations of values
for each terminal.
If a clause blocks an assignment, then it blocks all assignments where all
of the terminals in the clause have their value set such that the term evaluates
to false in the clause. Meaning if a term is negated in a clause, it is assigned
a value of 1 and vice versa if a term is positive in a clause, it is assigned a
value of 0. This is true because if each term in the clause evaluates to false
and you combine multiple "falses" with an or operator, it will evaluate to false.
However, there are more terminals in the assignments.
Recall the clauses block EVERY assignment where the terminals in the clause
are assigned values st the clause has to evaluate to true.
This implies all possible values can exist for the other terminals in the
assignments that are blocked. 
Now pick a terminal not in the clause. WTS half of the blocked assignments
have that terminal's value set to 1 and the other half have that terminal's
value set to 0.
We can represent the assignments as binary numbers where each digit corresponds
to a terminal (keeping the digits corresponding to the terminals fixed as we increment). Now we can increment the binary number until we have all possible
assignments.
Based on how binary numbers work, you can select any terminal and exactly half
of the binary numbers will have that value set to 0 and the other half will
have that value set to 1.

Done Lemma E

Lemma F: Suppose we have an instance of 2-t and 1-t clauses st a contradiction
cannot be made using only reduction. WTS that the 1-t clauses can be expanded
and the resulting 2-t clauses (with the existing 2-t clauses) can be reduced in 
such a way as to create contradicting 1-t clauses iff the instance is 
unsatisfiable.

Proof:

WTS the instance is unsat -> the clauses can be expanded/reduced to create
contradicting 1-t clauses

Suppose not. Then the instance is unsat and it is impossible to derive
2-t and 1-t clauses in this manner.

Since contradicting 1-t clauses cannot be created, then clauses of the form
[y]
[-y,x]
where x, y are terminals, cannot exist

WTS that clause pattern not existing implies satisfiability.

Suppose not. Then the clause pattern does not exist and it is unsat.
Since it's unsat, all of the assignments are blocked. What does this imply
about the given clauses?
Maybe since that pattern does not exist, there must be overlap which always
prevents all of the assignments from getting blocked

Recall 
each 1-t clause blocks 2^{n-1} assignments and 
each 2-t clause blocks 2^{n-2} assignments and 
for each group of assignments (blocked by a clause), 
    for each of the terminals which are not in that clause, 
        exactly half of the assignments are blocked by that terminal's value equal to 0 and the other half are blocked by that terminal's value equal to 1
The pattern does not exist
the instance is unsatisfiable

For each 1-t clause, it's negated terminal cannot appear in a 2-t clause

WTS the clauses exist in some pattern and that pattern is satisfiable

We already saw in Lemma D that if we had every possible 1-t clause (with the 
given restrictions), it has to be satisfiable

Let's try adding 2-t clauses.
We know we cannot add any clauses that include a negated term that exists in
a 1-t clause

[1]
[2]
[-3]
[-4]

[1, 2]
[1, -3]
[1, -4]
[2, -3]
[2, -4]
[-3, -4]

Adding all possible 2-t clauses will never be able to imply a contradicting
1-t clause since it will never have one terminal constand while the other
terminal is negated and positive since (for any given terminal) only one of 
these forms is allowed in all of the 2-t clauses

Stronger now:

For any instance of 2SAT an unsatisfiable instance implies contradicting
1-t clauses can be derived

Given: an unsatisfiable instance of 2SAT
We know 
 - all assignments are blocked
 - if we expand each clause to all possible n-term clauses, it will block each assignment
 - if two clauses share one terminal while the other is negated, it implies a 1-t clause

WTS a 1-t clause 





WTS the clauses can be expanded/reduced to create contradicting 1-t clauses
-> the instance is unsat

Clearly true based on the idea of contradicting 1-t clauses (it was in another
proof, idk where)

Lemma G: An unsatisfiable instance of 2SAT -> a 1-t clause is implied
Suppose not, then a given instance of 2SAT is unsatisfiable and a 1-t clause
cannot be derived.
Further, no two clause patterns exist like this:
[x, y]
[x, -y]
where one terminal is constant and the other is negated

So we know either [x, y] or [x, -y] doesn't exist. Since they are generic
enough, let's say [x, y] does not exist

This means that all assignments blocked by [x, y] are blocked by some other
clauses, all while ensuring this pattern does not emerge

There are 2^{n-2} assignments that need to be blocked

Consider a terminal, z, that is not in the clause [x, y]

Half of the assignments that need to be blocked are blocked by z = 1 and the
other half are blocked by z = 0

We cannot directly block this without violating the restriction

If we wanted to block all assignments where z = 0, we would need the clause
[z] which has to be implied from something like [z, w], [z, -w], which violates
the restriction

Recall a 1-t clause implication is not allowed, so we have to block the 
assignments where z = 0 using more terminals.

Clearly if we keep going to the next terminal, we would run out of terminals
and only be halfway (from the last step) to the final assignment blockage
(similar to the 1/2, 1/4, 1/8, ... pattern in Lemma D)

So we have to overlap.

The only legal clauses we can use containing x or y are
[x, -y]
[-x, y]
[-x, -y]
[x, z] or [-x, z]
[y, z] or [-y, z]
also [x, w...]

we can discard [-x, -y], [x, -y], [-x, y] since it does not block any 
assignments blocked by [x, y]
We can also discard [-x, z] and [-y, z] because they do not block
any assignments blocked by [x, y]

Consider adding [x, z] and [y, z].
Each of these blocks the same assignments since x and y are already set
and z remains constant between the two. And since a single value for z
blocks only half of the assignments, this cannot block all of the assignments.

Consider adding [x, w_1], [x, w_2], [x, w_3]... where w_i is another terminal
in the instance.
Again, each of these only blocks half of what it needs to. See Lemma D for a 
similar style:
We need to block 2^{n-2} assignments without using [x, y]
The first clause blocks 2^{n-3} assignments, which is half of what we need
2^{n-2}/2^{n-3} = 1/2
The second clause blocks 2^{n-3} assignments as well, but half of these
overlap with the first clause, so it only blocks 2^{n-4} additional
assignments
Similarly the third clause only blocks 2^{n-5} assignments.

The pattern continues, blocking half of the required assignments each time, 
and since the number of terminals is finite, we never block all of the
assignments

Therefore any instance without a two clause pattern in this manner:
[x, y]
[x, -y]

is satisfiable

And since our given instance is unsatisfiable, it must contain that pattern
and must imply a 1-t clause

ehh prove that [x, w_1], [w_1, w_2], ... does not imply unsat


Lemma H: You need both reduction and expansion
Expanding to 4 then reducing to 1 is incomplete
But what about
Reduce to 1, expand to 4, then reduce to 1?
Also incomplete
... Look into the stopping case to get a better sense of where the data
is going
It will also help with knowing when certain clauses don't have to be considered
anymore



Lemma I: In order to imply an additional clause of length k by expanding then
reducing, two clauses must share at least one negated terminal (and have at least k - 2 constant terms ?)

Aside (with k = 3):
share one constant term -> get new clause from expand + reduce
and the new clause is whatever the non-shared term/terminal is
there is still data left in 2(n-1) (k+1)-terminal clauses
share two constant terms -> get hecka new clauses from reduce + expand

Proof
Let n = 5
Consider the clause
[1 2 3]
which implies 4-t clauses
[1 2 3 4]
[1 2 3 -4]
[1 2 3 5]
[1 2 3 -5]

In order to imply a new 3-t clause, another existing 3t clause must exist
st it can imply a 4-t differing from the existing 4-t clauses by exactly
one negated terminal

Pick any of the existing 4-t clauses to match to, it does not matter which one
since 4, -4, 5, -5 all fill the role of "a terminal that is not in the original
clause"

Let's say we want data from the clause [1 2 3 4] then we need another 4-t
clause that differs by exactly one negated terminal. The cases are either
(1) the terminal is in the original clause or
(2) the terminal is not in the original clause

consider (1) the negated terminal in the 4-t clause is in the original 3-t 
clause

They are all equivalent so let's pick x_1
Now we want a 4-t clause [-1 2 3 4]

The possible 3-t clauses that expand to this are
[-1 2 3]
[-1 2 4]
[-1 3 4]
[2 3 4]

The first three all contain a negated terminal from the original clause so
we just have to disprove the last clause:

Suppose we pick [2 3 4]
then we have
[1 2 3 4]
[-1 2 3 4]
[2 3 4 5]
[2 3 4 -5]

Recall the 4-t clauses from the original 3-t clause:
[1 2 3 4]
[1 2 3 -4]
[1 2 3 5]
[1 2 3 -5]

We can discard the clauses with x_5 because they clearly cannot reduce to any
3-t clauses

Looking now at 
[1 2 3 4]
[1 2 3 -4]
[1 2 3 4]
[-1 2 3 4]

We can see that the 3-t clauses that are implied are
[1 2 3]
[2 3 4]

Which are just the given 3-t clauses so no new data is found

consider (2) the negated terminal is not in the original clause
Recall the scenario
Let n = 5
Consider the clause
[1 2 3]
which implies 4-t clauses
[1 2 3 4]
[1 2 3 -4]
[1 2 3 5]
[1 2 3 -5]

Now we want a 4-t clause st when matched with one of the existing 4-t clauses, 
the negated terminal is not in the original 3-t clause
Since 4, -4, 5, and -5 are equivalent, let's pick 4

Want [1 2 3 -4]
which can be expanded from
[1 2 3]
[1 2 -4]
[1 3 -4]
[2 3 -4]

We already have [1 2 3] so discard it
All the other clauses fall into the trap of only implying the two given
3-t clauses

Now we have shown you cannot get data if another 3-t clause does not share
a negated terminal, but consider the case where it does:

Recall you must share at least one term otherwise more than one terminal
will be different and you will not be able to reduce

Given:
n = 5
[1 2 3]
->
[1 2 3 4]
[1 2 3 -4]
[1 2 3 5]
[1 2 3 -5]

[-1 2 4]
->
[-1 2 3 4]
[-1 2 -3 4]
[-1 2 4 5]
[-1 2 4 -5]

all possible reductions to 3-t include:
->
[2 3 4]

Bam, new 3-t terminal from expanding then reducing


Proof/Lemma/etc Number Next: The Final:

WTS if we cannot derive contradicting 1-t clauses from 3SAT then it 
is satisfiable.

Proof:

Suppose not.
Then we cannot derive contradicting 1-t clauses from 3SAT and
it is unsatisfiable

Stronger Lemma I:
Given two clauses of length k that share a negated term, this implies a new
clause wherein it includes all of the other terms.
Ex/
[1, 2, 3, ..., i]
[a, b, c, ..., -i]
implies
[1, 2, 3, ..., a, b, c]
but if a bunch are the same, we can remove duplicates.
For all practical purposes, this limits 3-t clauses to imply clauses of length
2, 3, or 4. But does this solve the problem of needing a 5-t clause? yes

Proof for Stronger Lemma I:
Given two clauses of length k that share a negated term, this implies a new
clause of at least length k-1 and at most length 2*(k-1) which is composed
of all the terminals that are not the negated terminal.

Suppose we have the clauses
[1, 2, 3, ..., i]
[a, b, c, ..., -i]
where 1, 2, 3, ... i are any number of terminals in the instance
and a, b, c are any number of terminals in the instance.
Note that there could be overlap between the 1, 2, 3 ... and the a, b, c, ...
but according to Lemma (the one where if a clause contains the same terminal
twice but negated, it will always be satisfiable) the same terminal cannot 
appear in either form more than twice in the same clause
WTS it implies a clause like [1, 2, 3, ..., a, b, c, ...]

What do we know about the clauses of length k?
- they do not overlap
- there is some subset action happening...

assume for a moment the combined clause is larger than k
we know we can expand [a, b, c, ...] (without i) to [a, b, c, ..., q, r, s...]
because adding specifity (more terminals -> fewer blocked assignments) to a
clause is always allowed as long as the larger clause contains all terminals
in the smaller clause, the larger clause does not block any more assignments
than the smaller clause
but we cannot assume we have [a, b, c, ...] as we only have [a, b, c, ..., -i]
so we can imply
[a, b, c, ..., -i, q, r, s, ...] is blocked
now replace q, r, s, ... with 1, 2, 3 ...
[a, b, c, ..., -i, 1, 2, 3, ...]
Similarly, expand [1, 2, 3, ... i] to 
[1, 2, 3, ... i, a, b, c, ...]
Now since we have two clauses of the same length sharing all terminals except
for one negated terminl, we can make a new clause with just the shared terminals
therefore, 
[1, 2, 3, ..., a, b, c, ...] is implied by 
[1, 2, 3, ..., i]
[a, b, c, ..., -i]


now consider where the combined clause is less than or equal to k
the combined clause is less than k iff there is some overlap between
1, 2, 3, ... and a, b, c, ...
In this case, are all of the steps still valid?
assume that 1, 2, 3, ... == a, b, c, ...
then step 1, we expand
[1, 2, 3, ..., -i, 1, 2, 3, ...]
clearly this doesn't block any more assignments than the unexpanded version

what about the lengths of the implied clause?
Consider: all non-negated terms overlap
then there are (k-1) overlapping terminals and there are (k-1) terminals
in the new clause
Consider: no non-negated terms overlap
then there are (k-1) unique terminals in each clause so there are (k-1)*2
terminals in the new clause 

Since all steps are valid in both cases, we can say for certainty that if two
clauses of length k have the same terminal, t,  where t is positive in one clause and negated in the other, then we can make a new clause between length 
(k-1) and 2*(k-1) containing all the terminals that are not t

Proof done for Stronger Lemma I

Lemma J:
Given an **implied** clause of length k, say C, any clause that C implies can
be directly implied by the clauses that imply C

Example with k = 4, n = 7.
Given a 4-t clause, 
C := [1, 2, 3, 4]
WTS any 5-t clause that can be derived will already be derived by a 3-t clause
To derive a new clause from C, we need something like
[5, 6, 7, -4] or
[1, 5, 6, -4] or
[1, 2, 5, -4] or
[1, 2, 3, -4]

Consider D := [5, 6, 7, -4]

Then these clauses imply a clause
E := [1 2 3 5 6 7]

The 3-t clauses implying C are:
Below, parentheses mean everything in the () must exist and outside the 
parentheses, at least one must exist
a: ( 
  [1 2 i],
  [3 4 -i] 
  where i is any number 5 to n
)
b: [1 2 3]
c: [1 2 4]
d: [1 3 4]
e: [2 3 4]

The 3-t clauses implying D are:
f: (
  [5 6 i]
  [7 -4 -i]
  where i is any number 1 <= i <=n that's not 5, 6, 7, 4 
)
g: [5 6 7]
h: [5 7 -4]
i: [5 6 -4]
j: [6 7 -4]

WTS all combinations of (a, ..., e) and (f, ..., j) already imply E.
Welp clauses of length 3 can only imply clauses of length 4 so it doesn't work
:(
Clearly [1, 2, 3] [5, 6, 8], [-4, 7, -8] won't imply [1 2 3 4 5 6 7] immediately
but what if it's just that it will imply it without expanding above a certain k?

ie
3-t clauses can directly imply all clauses of len (3-1)*2
4-t clauses directly imply all clauses of len (4-1)*2

not good enough. We have to prove the more general form:
any two clauses that contain the same terminal, t, negated in one and positive in the other, will imply a new clause containing all terminals that are not t

Then... we still need to derive [1 2 3 4] from [1 2 3] before [1 2 3 4 5 6 7]
but maybe that's alright?

shut up. It doesn't matter that we have to expand all the way up to k = 7, it
matters that we have all possible combinations of 3-t clauses that imply
C and D and there is no combination of these clauses that do not imply E.

But what about the search time? To expand to k = 7?

For a moment let's say we proved that all possible 3-t clauses that imply
C and D also imply E without the need of directly making C and D, then what?

I guess the plan was to say that n-t clauses are implied by n-1-t clauses
are implied by ... are implied by 3-t clauses, but if you have to expand up to n-1 it defeats the purpose.

UGH. MOST BASIC: wts that the clauses implied by Stronger Lemma I include
all of the clauses that could possibly be implied.
WTS the given clauses of length 3 can be processed to gain all of the possible
clauses of length 3 that are implied.

Hmm maybe: is there any clause of length 4/5 or more that can imply a clause of
length 3 that cannot be directly implied by the given clauses? WTS there is 
no such clause

Suppose not. Then there is a clause of length 4, say D, that implies a clause
of length 3, say C, that cannot be implied by the given clauses of length 3.

We know by Stronger Lemma I that clauses of length 3 can only be implied by
clauses of length 3 or 4. (or 1 or 2 by expansion).

WTS that if a 4-t clause that would imply a new 3-t clause then the existing
3-t clauses that imply that 4-t clause also imply the new 3-t clause

WTS an unsatisfiable instance implies contradicting 1-t clauses. 
Unsatisfiable -> all assignments are blocked
Contradicting 1-t clauses -> 2-t clauses
2-t clauses -> 2-t or 3-t clauses
3-t clauses -> 3-t clauses or 4-t clauses, but all my homies hate 4-t clauses

Intuitively, the final proof will be of the form:
We can imply clauses according to Stronger Lemma I and
all clauses of length 5 that are implied by clause(s) of length 4 are directly
implied by clause(s) of length 3.
Expand on this to say all clauses of length n that are implied by clauses
of length n-1 are directly implied by clauses of length n-2. Continue until
you are considering clauses of length 3.
Another useful lemma: you can add whatever terminals you want to a clause, 
except for terminals already in the clause, and it will not block any
assignments that are not already blocked
Note that you actually can add terminals that are already in the clause
because if a clause contains two terminals and one is negated and one is 
positive, it will always be true and it will block 0 assignments which clearly
shows it will not block more assignments than the original clause