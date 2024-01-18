# Introduction
This is an exploration of 3SAT. Note that this version assumes no clauses contain a variable and its complement.

# Definitions
#### Variables
A variable is of the form $x_i$ where $1 \le i \le n$ where $n$ is the number of variables in the instance and each variable can be assigned a value $0$ or $1$

#### Clause
A clause is a set of 3 variables and/or their complements combined with a logical or operator. It is of the form: <br>
$(x_i \lor x_j \lor x_k)$ where $i \ne j \ne k$ <br> or
$(x_i \lor \neg x_j \lor x_k)$ <br>
Note that in the case of a complement, a variable and its complement may exist within the same clause, but the same variable cannot exist twice in the same clause unless one of the instances of the variable is negated

#### Instance
An instance of the 3SAT problem is comprised of a series of clauses in which each clause is combined with a logical and operator. It is of the form: <br>
$(x_i \lor x_j \lor x_k) \land (x_l \lor x_o \lor x_p) ...$

#### Assignments
An assignment is a set of variables and their values for a given instance. It is of the form: <br>
$A := x_1 = i, x_2 = j, x_3 = k, ..., x_n = l$ where there are $n$ variables in the given instance and $i, j, k, l \in \{0,1\}$

#### Satisfiable
An instance is satisfiable iff there exists an assignment such that the expression evaluates to true

#### Blocking an assignment
An assignemt is considered blocked if it is impossible to satisfy the given instance using that assignment. <br>
For example, the assignment $A := x_1 = x_2 = x_3 = 0$ can never satisfy the given instance: $(x_1 \lor x_2 \lor x_3)$

# Assumptions/Quick Derivations
#### For a given instance with $n$ variables, there are $2^n$ possible assignments
An assignment assigns either a $0$ or a $1$ to each variable (2 options) and there are $n$ variables so $2^n$ possible assignments exist.

#### For a given instance with $n$ variables, $(n C 3)*8$ possible clauses exist
Note that this excludes clauses that include a variable and its complement. <br>
$(n C 3)$: Choose 3 variables out of the $n$ possible to make a clause <br>
$8$: Each variable can either be natural or its complement, ie, each variable can have one of two values. <br>
$3^2$ possible clauses given 3 variables were selected <br>
$(n C 3)*8$ unique clauses exist given an instance of 3SAT with $n$ variables

#### TODO: Move the idea of worthless clauses up here

#### Including clauses with only two unique variables, there are $(n C 2)*4$ possible assignments
$(n C 2)$: Choose 2 variables out of the $n$ possible variables <br>
$2$: 2 ways to selcet a single variable that appears twice <br>
$2$: the other variable is either complemented or not

#### Total of $(n C 3)*8 + (n C 2)*4$ possible clauses
#### = $\dfrac{4n^3}{3} - 2n^2 + \dfrac{2n}{3}$ clauses
#### = $\dfrac{2}{3} (n -1 ) n (2n - 1)$ clauses
See previous two derivations

#### Each assignment can be blocked by at most $(n C 3)$ clauses
Consider an assignment. This assignment can be blocked by choosing 3 literals
and if that literal is 1 in the assignment, use the negative literal, and if
that literal is 0 in the assignment, use the positive literal. <br>
Use the three chosen literals to create a clause. <br>
Since you choose three literals out of n, there are $(n C 3)$ ways to create a
unique clause <br>
In other words there are $(n C 3)$ clauses that can block that assignment

# Lemmas
### Lemma :) - Assignments can be blocked
WTS that for a given instance, an assignment can be blocked after a single clause. <br>
Consider an instance of 3SAT with <br>
- $n$ variables <br>
- containing the clause $(x_i \lor x_j \lor x_k)$ 
where $i \ne j \ne k$ and $i, j, k \le n$

Consider the assignment $A := x_1 = x_2 = x_3 = ... = x_n = 0$, ie, an assignment where all variables are set to 0. <br>
Since each clause is bounded by a logical and, each clause has to evaluate to true in order for the entire instance to evaluate to true <br>
Note that the clause $(x_i \lor x_j \lor x_k)$ will evaluate to true iff at least one of the three variables are true, ie, they cannot all be set to 0. <br>
Since the assignment $A$ sets all variables to 0, the clause cannot evaluate to true with the given assignment. <br>
Therefore the entire instance cannot evalute to true with assignment $A$. <br>
Since it is impossible to satisfy the instance with assignment $A$, assignment $A$ is blocked by the given clause. $\square$
### Lemma 2N - Each clause blocks $2^{n-3}$ assignments
Consider the instance of 3SAT as defined in Lemma :). Let the specified clause
be clause $C$. <br>
Idea: show the general form of the assignments blocked by $C$ and show how many
such clauses exist <br>
Using similar logic as Lemma :), any assignment in which $x_i = x_j = x_k = 0$
will be blocked. <br>
Since there are 3 variables whose values are known, there are $n-3$ variables 
whose values could be 0 or 1 <br>
Since there are $n-3$ variables and $2$ possibilities for the variables, there 
are $2^{n-3}$ assignments in which $x_i = x_j = x_k = 0$, ie, there are 
$2^{n-3}$ assignments that are blocked by each clause <br>
#### Special case: consider the clause $(x_i \lor \neg x_i \lor x_j)$
Bloody bloody this doesn't block anything because $(x_i \lor \neg x_i)$ will be
true if $x_i = 0$ or $x_i = 1$ <br>
Alright these types of clauses are absolutely worthless since they are 
vacuously true <br>
Do not consider clauses that contain a positive and negative version
of the same literal

### Lemma Clause and Effect -
### adding clauses to an instance will make it more likely to be unsatisfiable
### removing clauses from an instance will make it more likely to be satisfiable

### Lemma Bounds - 
### An instance with fewer than 8 clauses will always be satisfiable
### An instance with more than $(n C 3)*7$ will never be satisfiable
# Exploration
### Idea: WTS there's a maximum number of clauses and in order to reach it, you have to pass through some pattern that can be pre-measured
Two ways to count patterns:

1. For each clause, consider what possible clauses could be next
2. For each clause, consider the index in which that clause appears, 
ie, what clauses appear before it, 
ie, not only which $2^{n-3}$ assignments are blocked, but also how it affects
redundant blockages (assignments that are blocked by multiple clauses)

#### Plan 1
Recall each assignment can be blocked by a maximum of $(n C 3)$ clauses <br>
What differentiates clauses?
if we take an instance of 3SAT st each clause blocks the same assignment, what
  will happen?

Consider an instance of 3SAT as follows:
 - $n$ variables exist
 - There are $(n C 3)$ clauses st each clause blocks an assignment, $A$
 - $A := x_1 = x_2 = x_3 = ... = x_n = 0$

 The clauses would be of the form

 $(x_1 \lor x_2 \lor x_3) \land$ <br>
 $(x_1 \lor x_2 \lor x_4) \land$ <br>
 ... <br>
 $(x_1 \lor x_2 \lor x_n) \land$ <br>
 $(x_1 \lor x_3 \lor x_4) \land$ <br>
 ... <br>
 $(x_1 \lor x_{n-1} \lor x_n) \land$ <br>
 $(x_2 \lor x_3 \lor x_4) \land$ <br>
 ... <br>
 $(x_{n-2} \lor x_{n-1} \lor x_n)$ <br>

Each clause blocks $A$ <br>
It does not block everything, still clearly satisfiable by the assignment <br>
$A_1 := x_1 = x_2 = x_3 = ... = x_n = 1$ <br>
But what about $A_1 := x_1 = x_2 = x_3 = ... = 1; x_n = 0$ <br>
This still works. Looks like it only blocks assignments with at least 3 0's. <br>

Consider an assignment with two or fewer 0's. <br>
Since each clause has three unique literals, each clause will evaluate to true <br>
Therefore all assignments with two or fewer 0's will satisfy the instance <br>

Consider an assignment with three or more 0's. <br>
Since the $(n C 3)$ clauses include all possible combinations of the positive
literals, there exists at least one clause whose literals are all 0 and would
thus evaluate to false, making the entire instance evaluate to false. <br>
Therefore all assignments with three or more 0's are blocked. <br>

There are a total of $2^n - \dfrac{1}{2}(n-1)(n) - n - 1$ blocked assignments

-- this is me from the future -- <br>
We don't really care about how many assignments are blocked, but rather to what
extent each assignment is blocked

##### Derivation
(number of total clauses) - (number of unblocked clauses) <br>
= (number of total clauses) - ((number of clauses with two 0's) + 
(number of clauses with one 0) + (number of clauses with no 0's)) <br>
= $2^n - ((n C 2) + (n C 1) + (n C 0))$ <br>
= $2^n - \dfrac{1}{2}(n-1)(n) - n - 1$

Alright we've got an exponential number of blocked clauses, which is ...
Shoot I'm not sure. <br>
We have $\dfrac{1}{6}(n-2)(n-1)(n)$ clauses and $2^n - \dfrac{1}{2}(n-1)(n) - n - 1$ 
blocked assignments. <br>
We have on the order of $n^3$ clauses and $2^n$ blocked assignments and each
clause blocks $n^3$ assignments <br>
If each clause blocks $n^3$ assignments and there are $n^3$ clauses then it 
should block on the order of $n^6$ assignments <br>

After a polynomial number of clauses, we have a polynomial number of assignments
remaining. <br>

It's polynomial to check that the instance falls under this case then it's
polynomial time to check the remaining assignments. <br>

The specific case being an instance of 3SAT that is consistent with the 
description in this Plan 1 <br>

It is slightly more general. As long as the instance of 3SAT just *contains* the
given clauses, the brute force approach becomes a polynomial time problem <br>

We have shown that any instance of 3SAT that contains at least (n C 3) clauses
and they all block the same clause, it becomes polynomial time solvable <br>

Is there a way to confirm that an instance fits this metric in polynomial time?

For each clause, ~~(n C 3) assignments are potentially *the* blocked assignment.
So for each clause we need to remember the counts for on the order of $n^3$ 
additional clauses.~~ <br>
correction: $2^{n-3}$ assignments are blocked and are potentially *the* blocked
assignment so we need to remember the counts for $2^{n-3}$ assignments for
each clause we come across <br>
Meaning there are $(n C 3) * 2^{n-3}$ which is still an exponential number of
assignments we need to count before we have a polynomial time solution

Now the idea changes from counting the actual assignments to counting patterns
of assignments

### Cross out nearly everything after this
### Actually Part 2 may still be valid as long as we don't rely on remembering
### The count on each assignment

### The above is still an interesting conclusion, it means we cannot use certain tools
### We cannot rely on counting the number of assignments affected by each clause 
However we do know *how many* assignments may have been blocked by a clause
and so what if we keep counts on the clauses we've seen?


### The below stuff
After $(n C 3)$ clauses we know it becomes a polynomial time solvable problem
and after $(n C 3)$ clauses we have to remember counts for <br>
(number of clauses) * (number of assignments per clause) <br>
= $(n C 3) * (n C 3)$ <br>
which is on the order of $n^3 * n^3$ which is <br>
$n^6$ different assignments we need to count before we have a polynomial time
solution <br>

## Lemma SpecInstance
Idea: we just proved that if an instance has at least $(n C 3)$ clauses that
all block the same assignment, then it is solvable in polynomial time

WTS minimum number of clauses in which there will always be $(n C 3)$ clauses
that block the same assignment and if it is not unreasonably large, it is 
acceptable to brute force everything smaller than that

#### Part 2 - min number of clauses that force the SpecInstance lemma
Outcome of part 2: wait a second... there are only $(n C 3)*8$ unique clauses <br>
And at some point we must cross the threshold in which the special instance is
forced. <br>
So we have at most $(n C 3)*8$ clauses and for each clause we need to remember


Alright so we've got:
 - $(n C 3)*8$ possible clauses
 - Each assignment can be blocked by at most $(n C 3)$ clauses
 - $2^n$ possible assignments
 - By Lemma 2N, each clause blocks at most $2^{n-3}$ assignments

And we want
 - $(n C 3)$ clauses that block the same assignment

 WTS minimum number of clauses before it has to be true that $(n C 3)$ of them
 block the same assignment

 We know at least $(n C 3)$ clauses have to exist and at most $(n C 3)*8$ can
 exist in the instance

Start with all $(n C 3)*8$ clauses in one instance <br>
Then each assignment is blocked by the maximum number of clauses that can block
an assignment, which is $(n C 3)$ clauses <br> 
Remove a single clause, say $c_1 := (x_1 \lor x_2 \lor x_3)$ <br>
There are $2^{n-3}$ assignments that are no longer blocked by $(n C 3)$ clauses, 
but rather $(n C 3) - 1$ clauses. <br>
These are all the assignments that were originally blocked by $c_1$ <br>
In this case, all assignments with $x_1 = x_2 = x_3 = 0$ are now slightly freed <br>
And there are $2^n - 2^{n-3}$ assignments left to free. <br>
The most we can free with a single clause is $2^{n-3}$ <br>
But how many times can we free the maximum number of assignments? <br>
And what does $x$ have to be in $2^n - x*2^{n-3}$ before the expression is.. <br>
Break, hold on this is confusing, let's define some more things <br>

**Safe assignment** - an assignment which is blocked by fewer than $(n C 3)$ clauses <br>
**Fragile assignment** - an assignment which is blocked by $(n C 3)$ clauses <br>

The problem has become: Find the minimum number of clauses in an instance of
3SAT in which at least one assignment must be fragile <br>

So now, after $c_1$ has been removed, there are $2^{n-3}$ safe assignments and
$2^n - 2^{n-3}$ fragile assignments <br>

Do we want to remove clauses in such a way as to maximize or minimize additional
safe assignments?

Recall that we want the smallest number of clauses that will require overlap on
the same assignment $(n C 3)$ times, ie, that will require at least one assignment
to be fragile

If we were adding clauses from 0, we would want to make assignments fragile as
slowly as possible, but since we're removing clauses, we want to make assignments
fragile as quickly as possible, meaning we retain fragile assignments for as long
as possible <br>

Goal: remove clauses in such a way as to make the minimum number of assignments
safe with each removal

Idea 2: Start with one clause and keep adding clauses while evenly distributing 
the blockages across the assignments

Start with one clause - blocks $2^{n-3}$ assignments <br>
Add all clauses from Plan 1 except for the last clause <br>
Now we have a single assignment with $(n C 3) - 1$ clauses blocking it... well
let's play around with what the other assignments look like in Plan 1

#### Part 3 - Restart attempt 1
Idea: if eight unique clauses exist that contain all the combinations of the 
same three literals, the instance is unsatisfiable 

So now we just have to find other cases that force certain conditions?

Consider n = 4

| $x_1$ | $x_2$ | $x_3$| $x_4$ |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 |

with the instance

$(x_1 \lor x_2 \lor x_3) \land$ <br>
$(x_1 \lor x_2 \lor \neg x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor \neg x_3) \land$ <br>
$(\neg x_1 \lor x_2 \lor x_3) \land$ <br>
$(\neg x_1 \lor x_2 \lor \neg x_3) \land$ <br>
$(\neg x_1 \lor \neg x_2 \lor x_3)$ <br>

the possible assignment table becomes

Blocked | $x_1$ | $x_2$ | $x_3$| $x_4$ |
| --- | --- | --- | --- | --- |
| X | 0 | 0 | 0 | 0 |
| X | 0 | 0 | 0 | 1 |
| X | 0 | 0 | 1 | 0 |
| X | 0 | 0 | 1 | 1 |
| X | 0 | 1 | 0 | 0 |
| X | 0 | 1 | 0 | 1 |
| X | 0 | 1 | 1 | 0 |
| X | 0 | 1 | 1 | 1 |
| X | 1 | 0 | 0 | 0 |
| X | 1 | 0 | 0 | 1 |
| X | 1 | 0 | 1 | 0 |
| X | 1 | 0 | 1 | 1 |
| X | 1 | 1 | 0 | 0 |
| X | 1 | 1 | 0 | 1 |
|  | 1 | 1 | 1 | 0 |
|  | 1 | 1 | 1 | 1 |

which is easily proven unsatisfiable by adding the clauses

$(\neg x_1 \lor \neg x_2 \lor x_4) \land$ <br>
$(\neg x_1 \lor \neg x_2 \lor \neg x_4)$

So there exists unsatisfiable instances which do not contain eight unique clauses
that contain all combinations of the same three pos/neg literals

How can we track a vulnerability?

First, note that if n were much larger, it would still only take those nine
clauses to make it unsatisfiable since the additional assignments would all
have the same combinations of $x_1, x_2, x_3, x_4$

It looks like this is a nine clause pattern that will always result in unsatisfiability
And if we remove another clause from the original seven, we may be able to 
"exchange" the missing clauses for two or more new ones

Eventually when we deplete the original seven clauses, we'll have 30 or so patterns
that will guarantee unsatisfiability but then we'll have to consider $x_5$ and
so on

First things first, let's make a chart of known sets of clauses that guarantee
unsatisfiability

#### 9 clause set discussion
Taking the original 8 and removing 1 and adding two different ones, what if
we removed a different clause? <br>
It would result in a similar addition of two more clauses

What if we remove two clauses?

It would open up two more assignments, but suppose we had the 6 remaining clauses:

$(x_1 \lor x_2 \lor x_3) \land$ <br>
$(x_1 \lor x_2 \lor \neg x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor \neg x_3) \land$ <br>
$(\neg x_1 \lor x_2 \lor x_3) \land$ <br>
$(\neg x_1 \lor x_2 \lor \neg x_3) \land$ <br>

Then the open clauses would be

Blocked | $x_1$ | $x_2$ | $x_3$| $x_4$ |
| --- | --- | --- | --- | --- |
|  | 1 | 1 | 0 | 0 |
|  | 1 | 1 | 0 | 1 |
|  | 1 | 1 | 1 | 0 |
|  | 1 | 1 | 1 | 1 |

Which could be blocked by the additional two clauses

$(\neg x_1 \lor \neg x_2 \lor x_4) \land$ <br>
$(\neg x_1 \lor \neg x_2 \lor \neg x_4)$

which means ...
 - there is redundancy in the first example in the 9 clause set section
 - another 8 clause set exists
 - 

Once we remove a clause from a known set and replace it by exchanging one term
with an unseen terminal (or maybe just any different terminal) we can now
completely disregard any changes in the old terminal and only consider assignments
where the remaining two terminals are unchanged. If we then use both the positive
and negated version of the new terminal, we can block all the same assignments
as the previous clauses

in short, replace $(x_1 \lor x_2 \lor x_3) \land (x_1 \lor x_2 \lor \neg x_3)$
with $(x_1 \lor x_2 \lor x_4) \land (x_1 \lor x_2 \lor \neg x_4)$

This makes sense as it just flips the order of when the new terminal ($x_3$ or 
$x_4$) is assigned a 1 or a 0

Blocked | $x_1$ | $x_2$ | $x_3$| $x_4$ |
| --- | --- | --- | --- | --- |
|  | 1 | 1 | 0 | 0 |
|  | 1 | 1 | 0 | 1 |
|  | 1 | 1 | 1 | 0 |
|  | 1 | 1 | 1 | 1 |

So now it no longer becomes all eight forms of three terminals, but rather
all four forms of two terminals with two clauses in which the two
terminals stay constant and the third terminal exists in either form, for each
of the four forms of the first two clauses

Taking things one step further, perhaps we just need to consider a single terminal
that exists in two clauses in either form. <br>
And then for each of those clauses, select another terminal so that two new clauses
are made st the first terminal remains the same and the second changes
And for each of those clauses, select another terminal so that two new clauses
are made st the first two terminals remain the same and the third terminal changes

In this way we should have 8 clauses, but the restriction of terminals is no 
longer limited to 3

Algorithm to make an instance unsatisfiable: <br>

```
Select a terminal, x_i
Create two new clauses that contain the positive and negative forms of x_i
For each of these clauses,
  select a new terminal x_j (note that it does not have to be the same
  terminal for both of the clauses)
  Create two new clauses in which x_i remains the same and x_j is positive
  in one clause and negative in the other
  For each of these clauses,
    select a new terminal x_k (note that it does not have to be the same
    terminal for both of these clauses)
    Create two new clauses in which x_i and x_j remain the same and x_k is
    positive in one and negative in the other
```

Test:

$x_i := x_1$ <br>
$x_{j,1} := x_2$ <br>
$x_{j,2} := x_3$ <br>
$x_{k,1} := x_4$ <br>
$x_{k,2} := x_5$ <br>
$x_{k,3} := x_6$ <br>
$x_{k,4} := x_7$ 

$(x_1 \lor x_2 \lor x_4) \land$ <br>
$(x_1 \lor x_2 \lor \neg x_4) \land$ <br>
$(x_1 \lor \neg x_2 \lor x_5) \land$ <br>
$(x_1 \lor \neg x_2 \lor \neg x_5) \land$ <br>
$(\neg x_1 \lor x_3 \lor x_6) \land$ <br>
$(\neg x_1 \lor x_3 \lor \neg x_6) \land$ <br>
$(\neg x_1 \lor \neg x_3 \lor x_7) \land$ <br>
$(\neg x_1 \lor \neg x_3 \lor \neg x_7)$ <br>

[1, 2, 4]
[1, 2, -4]
[1, -2, 5]
[1, -2, -5]
[-1, 3, 6]
[-1, 3, -6]
[-1, -3, 7]
[-1, -3, -7]

Dang, this is satisfiable by

| Blocked | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ |
|---|---|---|---|---|---|---|---|
|:(|1|1|1|1|1|1|0|

Well hottin hootin hollering maybe I am dumb, that algorithm works!!!

CONTINUE HERE

Two things:
1. Can we confirm that an instance of 3SAT has clauses in this pattern in polynomial time?
of course, $n^7$, just take 7 of the n variables and try them all
or it might be (n P 7)
2. Are there unsatisfiable instances that do not contain this pattern?
Yes, now can we reduce it to a more general 8 clause pattern?
Or can we prove that no such pattern exists?

Test 2:

$(x_1 \lor x_2 \lor x_3) \land$ <br>
$(x_1 \lor x_2 \lor \neg x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor x_3) \land$ <br>
$(x_1 \lor \neg x_2 \lor \neg x_3) \land$ <br>
$(\neg x_1 \lor x_2 \lor x_4) \land$ <br>
$(\neg x_1 \lor x_2 \lor \neg x_4) \land$ <br>
$(\neg x_1 \lor \neg x_2 \lor x_4) \land$ <br>
$(\neg x_1 \lor \neg x_2 \lor \neg x_4)$

### Working with the programs
I noticed this clause
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

has the following assignments blocked twice:
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

Which would also be blocked by [1, 2, 4], but this clause is not 
in the instance

What does this mean?

There is some information here that is at least as valuable as the
presence of [1, 2, 4] and if we knew this information, we could
apply the "ghost" clause of [1, 2, 4] to see if the clause pattern exists

Now what info implies the presence of a redundant [1, 2, 4]?

Look at other clauses blocking these assignments:

[1, 2, -3] <- blocks first four
[1, 2, 3] <- blocks next four
[4, 5, 6]
[4, 5, -6]
[4, -5, 6]
[4, -5, -6]
^ the clauses containg 4 block all eight clauses once

The four clauses containg four matches half of the eight clause
pattern that blocks everything, specifically, the presence of 
these clauses blocks exactly half of the assignments - any assignment
where $x_4$ is assigned the value of 0

It takes four clauses in this pattern and a terminal cannot have a value
of 0. Similarly, if it was -4, the terminal could not have a value of 1

Now how do the first two caluses (1 2 3 and 1 2 -3) affect the scenario?

** Possible Lemma **
** Open the files in the Ghost Clause dir **
If we select a clause and a terminal that's not in the clause, 
exactly half of the assignments that clause blocks will have
that terminal equal to 0 and exactly half will have that terminal equal to 1

Knowing this, if we prove a value cannot exist for a terminal (like
it was shown that $x_4$ cannot be 0) and we have a clause [1, 2, 3]
then what can we say about [1, 2, 4] or [1, 3, 4] or [2, 3, 4]? <br>
Not much I think <br>
If we remove [1, 2, -3] the instance becomes satisfiable and the ghost
clause [1, 2, 4] does not exist


WTS something cool about how [1, 2, 3] and [1, 2, -3] and (not 4 == 0) 
implies the presence of a redundant [1, 2, 4] <br>
[1, 2, 3] and [1, 2, -3] blocks all clauses with $x_1 = x_2 = 0$

It takes at least two clauses to block all assignments that assign a 
certain value to two terminals - a neat thing happens if you find clauses
in this pattern and some in another, you can make ghost clauses

Three clauses? <br>
Maximum amount of info - [1, 2, 3], [1, 2, -3], [1, -2, 3]
Blocks all assignments with 
$x_1 = x_2 = 0$ <br>
$x_1 = x_3 = 0$ <br>
Really just the two clause case, but two valid clauses exist

Five clauses? <br>
Consider the clauses - <br>
[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3] <br>
Four clause info - blocks: <br>
$x_1 = 0$ <br>
One clause info - blocks: <br>
$x_1 = 1; x_2 = x_3 = 0$ 

Six clauses? <br>
[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3], [-1, 2, -3] <br>
Four clause info - blocks: <br>
$x_1 = 0$ <br>
Two clause info - blocks: <br>
$x_1 = 1; x_2 = 0$

Seven clauses? <br>
[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3], [-1, 2, -3],
[-1, -2, 3] <br>
Four clause info - blocks: <br>
$x_1 = 0$ <br>
Two clause info - blocks: <br>
$x_1 = 1; x_2 = 0$
$x_1 = 1; x_3 = 0$

Eight clauses? <br>
Clearly just blocks assignments where $x_1 = 0$ or $x_1 = 1$

Let's see how many clauses it takes to block certain types of assignments

One clause - blocks assignments where a value is assigned for three terminals

Two clauses - blocks assignments where a value is assigned for two terminals

Three clauses - blocks two sets of assignments regarding terminals $x_i$,
$x_j$, and $x_k$ 1) all assignments where a value for $x_i$ and $x_j$ are
assigned and 2) all assignments where a value for $x_i$ and $x_k$ are assigned

Four clauses - blocks assignments where a value is assigned for one terminal

Five clauses - the four clauses block a single terminal's assignment
and the fifth clause blocks a three-terminal assignment

Six clauses - simply four clause info + two clause info

Seven clauses - simply four clause + three clause

Eight clauses - four + four; all assignments are blocked

Using this idea we can make ghost clauses, but first let's continue for 5, 6,
7, and 8 clauses

Alright ghost clause time <br>
Refer to the document ghostclause.md

Idea: show that every redundancy can result in a ghost clause
and that ghost clauses can be added to the instance without
adding any new information, but they can be used to match patterns that
would prove an instance unsatisfiable

Algo: 
Look for four clause patterns and make note of required values
Make ghost clauses if possible
Look for three/two clause patterns that require a value for two terminals
Make ghost clauses based on this info (two assigned + one assigned = 1 clause)
Keep repeating until no ghost clauses are made or the eight clause all blocking
pattern is known

### Idea number next:
We know that if an instance is unsatisfiable, then it implies the existence
of the eight clause pattern
Let's just try all the clauses, see if they're implied and if the eight
clause pattern exists in the new instance, then it's unstatisfiable

Problem: show that the existence of an implied clause is solvable in poly time
Given an instance and a potential implied clause, show whether or not all of
the 2^{n-3} assignments that clause could block are already blocked by the 
instance

Let's say the clause is [1, 2, 3], just an arbitrary starting point,
then in order for it to be implied, we would need 
 - clauses that block all assignments where x_1 = x_2 = x_3 = 0

Note that the clause could be implied without ever using one of its terminals
Let's run through [1, 2, 4] with the nine clause instance:
[1, 2, 3] 
[-1, 4, 5],
[-2, -4, 6],
[-1, -4, -6],
[-1, -5, 4],
[-2, 1, 4],
[-3, 1, 2]
[1, -2, -4]
[-1, 2, -4]

This becomes a similar smaller "3SAT" problem with only 2^n-3 possible
assignments, however there is no guaranteed number of assignments a clause
could block

 - any clause that contains a negated terminal from the potential clause
will block 0 assignments
 - any clause that does not share a terminal blocks at most 2^{n-6}
 - any clause that has one shared terminal blocks at most 2^{n-5}
 - any clause that has two shared terminals blocks at most 2^{n-4}

How many clauses can we have that do not imply [1, 2, 4]?

[3, 5, 6]
[3, 5, -6]
[3, -5, 6]
[3, -5, -6]
[1, 2, 3] <- blocks same ones as [3, 5, 6]'s

How many clauses are there total?
8 * (n C 3)

idk, let's say the minimum number of clauses that force the implication is on
the order of n^3, this doesn't help too much

Work on overlap:
the only clauses that overlap must not share a negated terminal, ie, 
if [1, 2, 3] is a clause, then overlap will occur iff the other clause
does not contain -1, -2, or -3
This is just another search for the eight clause pattern, but we know values for
three of the terminals.
This doesn't matter too much as we can still possible have the clauses like
[3, 5, 6]
[3, 5, -6]
[3, -5, 7]
[3, -5, -7]
[3, 8, 9]
[3, 8, -9]
[3, -8, 10]
[3, -8, -10]

What if we can force some information since we know we're searching all possible
clauses, eventually we will come upon the seven clauses with which one of the 
clauses from the instance would make the eight clause pattern

Given the nine clause instance:
[1, 2, 3] 
[-1, 4, 5],
[-2, -4, 6],
[-1, -4, -6],
[-1, -5, 4],
[-2, 1, 4],
[-3, 1, 2]
[1, -2, -4]
[-1, 2, -4]

[1, 2, 4]
| Blocked | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ |
|---|---|---|---|---|---|---|
| 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 | 0 | 1 |
| 3 | 0 | 0 | 0 | 0 | 1 | 0 |
| 3 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 |

and we know half of the clauses are blocked by [1, 2, 3]
so we only need to find clauses to block 2^{n-4} assignments

Interesting, we only need to block four assignments, but we have eight clauses

We can disregard any clauses with -1, -2, or -4, leaving us with
[-3, 1, 2]

hypothetically, we could've been left with 
[-3, 5, 6]
[-3, 1, -5]
[-3, 2, -6]
[-3, 2, 5]

Since 2 is in the potential clause, [2, X, Y] will block [X, Y, Z] plus more
so we can trim [X, Y, Z] which is [-3, 5, 6]

WTS: you will always be able to trim, or, if you can't trim, then a single value
will be implied

hold on, if we add more terminals, this is still just searching for the eight
clause pattern again, it's still blocking 2^{n-4} assignments which is exponential

So it is just as hard as proving you will always be able to trim as in the
original problem

### Idea number next
Consider an instance with two clauses
[1, 2, 3]
[1, 2, -3]

Will there ever be an instance containing these clauses in which the value of
x_3 determines if the problem is satisfiable or not?

Consider the nine clause instance
[1, 2, 3],
[-1, 4, 5],
[-2, -4, 6],
[-1, -4, -6],
[-1, -5, 4],
[-2, 1, 4],
[-3, 1, 2],
[1, -2, -4],
[-1, 2, -4]

Look for all two terminal implications

hmm... the only direct two terminal implications are
[1, 2]
[1, -2]
[-1, 4]

which come from
[1, 2, 3]
[1, 2, -3]

[1, -2, 4]
[1, -2, -4]

[-1, 4, 5]
[-1, 4, -5]

but we need more information, we cannot imply unsatisfiability by just these
six clauses, what do we get from

[-2, -4, 6]
[-1, -4, -6]
[-1, 2, -4]

[1, 2]
[1, -2]
[-1, 4]

try the poly time 2SAT approach
try x_1 = 0 -> x_2 = 1 -> x_1 = 1 X
try x_2 = 0 -> x_1 = 1 -> x_4 = 1 -> fails on [-1, 2, -4] X
try x_1 = 1 -> x_4 = 1 -> x_2 = 1 -> x_6 = 1 -> fails on [-1, -4, -6] X
try x_2 = 1 -> x_1 = 1 -> x_4 = 1 -> x_6 = 1 -> X

In this instance, it is proven in poly time
[1, 2] implies x_1 == 1 OR x_2 == 1 and both assignments lead to
a contradiction

TODO: Find an algo that tries solutions based on a 2sat instance
something like
1. For each 2 clause implication, say [x_i, x_j]
2. Try the assignment x_i = 1
3. If contradicts, try the assignment x_j = 1
4. If x_j = 1 leads to a contradiction, it is unsat
5. - Do something where if it's not a contra, but there are 2 clause
implications without an assignment, keep checking assignments

  
More low level algorithm:
```
Make an assignment to keep track of forced values, called known_assignments
for each clause in implications (1-term, 2-term, 3-term implications):
  process 1-term
    if the 1-term clause causes a contradiction, return UNSAT
    otherwise, update known_assignments
  process 2-term
    for each terminal in 2-term:
      if the current terminal is forced, update known_assignments with the
        other terminal
      if the clause is True via an existing assignment, no more info can
        be gained from this clause
    if neither terminal's value can be assigned, try both assignments
    ... how? Dangnabbit, recursion, call the function with (implications[cur:], known_assignments)

  process 3-term
```

More more low level, more robust algo:
```
Input: the instance, optionally an assignment
(0) if assignment is null, set X for each terminal to represent unknown
(1) Scan three-terminal clauses for two-terminal implications
(2) Scan two-terminal clauses for one-terminal implications
(3) add the implications to the list and sort by length
(4) Process the first implication
  (4a) If it's a one-term implications
      (1a) if the current assignment does not allow this assignment, return ""
          to show this assignment is unsatisfiable
      (1bi) otherwise, set the value of the terminal in the assignment
      (1bii) call the function with removing the first implication
             and the updated implications and return the output 
  (4b) If it's a two-term implication
    (1) For each terminal, 
      (1a) if the terminal is consistent with the assignment, just call the
          function with the same assignment, but remove the current clause
          save this to a variable, assignment1
      (1b) if the terminal is inconsistent with the assignment, add a new
          one-terminal containing just the other terminal, then call the
          function with the same assignment and updated implications (without
          the current clause)
      (1c) if the terminal is unknown, update the assignment and call the
           function with the new assignment (and remove the current clause)
  (4c) If it's a three-term implication
    (1) For each terminal,
      (1a) if it's consistent with the current assignment, just call the
           function and remove the current clause
      (1b) if it's inconsistent, add a new two-terminal implication with
           the other two terminals then call the function with the same
           assignment and updated implications
      (1c) if the terminal's value is unknown, update the assignment and call
           the function with the new assignment (removing the current clause)

```
### Plan sort of number next - Plan Expansion

Based on the idea that you can get a k-1 terminal implication from two clauses
of length k <br>
And then you can add 2(n-k) k-terminal expansions from those clauses <br>
For example, if you have the clauses
[1, 2, 3]
[1, 2, -3]
[-1, 2, -4]

the first two clauses imply [1, 2] <br>
[1, 2] expands to [1, 2, 4] and [1, 2, -4] <br>
and [1, 2, -4] and [-1, 2, -4] implies [2, -4] <br>

Thus we have a new two terminal clause that cannot be directly implied from two
existing three terminal clauses

Similarly, one terminal clauses like [1] expand to [1, 2, 3], [1, 2, -3], [1, 4, -5], ...

The only thing that CANNOT be expanded is a negative terminal included in the
current clause

So [1, 2] can never expand to clauses that contain -1 or -2

Note: this idea works for three or more terminal clauses, but if you expand
until you cannot expand anymore, you will end up with an exponential number
of expansions... idk there might be some value in expanding beyond three term clauses


algo:
```
(1) Get all two-terminal implications
(2) Get all one-terminal implications
(3) Expand all one terminal implications
(4) Expand all two terminal implications
(5) Repeat 1-4 until you have no more implications
(6) Solve like before, assigning values where they are forced from one-term
    clauses, or trying both values from two-term clauses

```

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

### Plan to optimize solve_expand()
instance - contain all clauses from which you can still get info
processed - all clauses from which you gathered all information
if a clause gets expanded to all possible forms, remove it from instance
if a clause gets reduced, remove it from instance



# Proofs

# Cleanup
- assign a name for the clause in Lemma :)

