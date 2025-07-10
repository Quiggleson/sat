Step 1. Expand the given clauses to n-terminal clauses. Notice the following pattern exists

C1 n - 2 -> C5 n - 1 -> C9 n
C2 n - 2 -> C6 n - 1 -> C10 n -> C13 n - 1
C3 n - 2 -> C7 n - 1 -> C11 n 
C4 n - 2 -> C8 n - 1 -> C12 n -> C14 n - 1 -> C15 n - 2

By Lemma 5.19, we don't need to process the n-terminal clauses to derive all the n-1-terminal clauses needed.

We can derive C13 and C14 by processing clauses with a maximum length of n - 1.

How many different ways to get C13?
Consider the opposite form term from C9 and C10

consider 3 cases
1. the opposite form term does not exist in C1 or C2
2. the opposite form term exists in either C1 or C2
3. the opposite form term exists in C1 and C2

Consider each case

1. Then all of the terms in C1 exist in C13 and 
C1 -> C13
2. Then the clause that does not contain the opposite form term can expand to C13 so
C1 -> C13 or 
C2 -> C13
3. Then C1 and C2 can imply a new clause. Note that all of the terms in the new clause exist in C13 so
imply(C1, C2) -> C13 or
imply(C1, C2) -> C16 and expand(C16) -> C13

Now we know we can derive C15 without processing an n-terminal clause. 

Now can we show that we can derive an n-3-terminal clause without processing an n-1-terminal clause?

What do we know about deriving an n-3-terminal clause?

The inputs are n-3-terminal clauses that expand to n-2-terminal clauses
and 
these n-2-terminal clauses either 1) expand to, 2) imply, or 3) imply then expand to a bunch of n-1-terminal clauses and
these n-1-terminal clauses imply n-2-terminal clauses and
these n-2-terminal clauses imply n-3-terminal clauses
and there exists a *fun* :sparkle: case where an n-2-terminal clause and a 3-terminal clause imply the final 3-terminal clause

define the following 
n-3 -> n-2 -> 
n-3 -> n-2 -> 
n-3 -> n-2 ->    -> n-1
n-3 -> n-2 ->  ? -> n-1 -> n-2
n-3 -> n-2 ->    -> n-1
n-3 -> n-2 ->    -> n-1 -> n-2 -> n-3
n-3 -> n-2 -> 
n-3 -> n-2 -> 

For each n-1-terminal clause, there are a maximum of two n-3-terminal clauses implying it
1. the n-2-terminal clause expands to the n-1-terminal clause
2. the n-2-terminal clauses imply the n-1-terminal clause
3. the n-2-terminal clauses imply a new clause which expands to the n-1-terminal clause

Consider the first n-2-terminal clause. Can it be derived without processing an n-1-terminal clause?

There are five ways to derive n-2 via n-1-terminal clauses

(1) and (1)
Define the following clauses
n-3
$C_1 := [\alpha_1]$
$C_2 := [\alpha_2]$
n-2
$C_5 := [\alpha_1 \cup \beta_1]$
$C_6 := [\alpha_2 \cup \beta_2]$
n-1
$C_9 := [\alpha_1 \cup \beta_1 \cup \delta_1]$
$C_{10} := [\alpha_2 \cup \beta_2 \cup \delta_2 ]$
n-2
$C_{11} := [\alpha_1 \cup \beta_1 \cup \delta_1 \cup \alpha_2 \cup \beta_2 \cup \delta_2 - \{i , -i\}]$

Rules
expand($C_1$) $\rightarrow C_5$
expand($C_2$) $\rightarrow C_6$
expand($C_5$) $\rightarrow C_9$
expand($C_6$) $\rightarrow C_{10}$
imply($C_9, C_{10}$) $\rightarrow C_{11}$ 

Known: 
$i \in \alpha_1 \cup \beta_1 \cup \delta_1$
$-i \in \alpha_2 \cup \beta_2 \cup \delta_2$

Cases:
For each set of terms, it either contains the opposite form term or it does not.
2^6 cases \:(

Known:
 - if the opposite form term is not in $C_5$ or $C_6$, then all the terms in these clauses exist in $C_11$ and $C_11$ can be derived without processing an n-1-terminal clause
 - so $C_5$ must contain an opposite form term and $C_6$ must contain an opposite form term, but not necessarily different ones?
 - If they contained the same exact term then the n-1-terminal clause expanded to from the n-2-terminal clause would block 0 assignments since it must have the other form of the term
 - So both $C_5$ and $C_6$ contain an opposite form term, and either clause contains the opposite form of said term, so a new clause may be implied

imply($C_5, C_6$) $\rightarrow C_{12}$

$C_5 := [\alpha_1 \cup \beta_1]$
$C_6 := [\alpha_2 \cup \beta_2]$

$C_{12} := [\alpha_1 \cup \beta_1 \cup \alpha_2 \cup \alpha_2 - \{i, -i\}]$

Now all of the terms in $C_{12}$ exist in $C_{11}$ so $C_{11}$ can be derived by processing clauses with a maximum length of n-2.
For future reference, $C_{12}$ could have length $n-3$ so you may have to expand $C_{12}$ to $C_{11}$

(1) and (2)

n-3
$C_1 := [\alpha_1]$
$C_2 := [\alpha_2]$
$C_3 := [\alpha_3]$
n-2
$C_5 := [\alpha_1 \cup \beta_1]$
$C_6 := [\alpha_2 \cup \beta_2]$
$C_7 := [\alpha_3 \cup \beta_3]$
n-1
$C_9 := [\alpha_1 \cup \beta_1 \cup \delta_1]$
$C_{10} := [\alpha_2 \cup \beta_2 \cup \alpha_3 \cup \beta_3 - \{i, -i\}]$
n-2
$C_{11} := [\alpha_1 \cup \beta_1 \cup \delta_1 \cup \alpha_2 \cup \beta_2 \cup \alpha_3 \cup \beta_3 - \{i, -i\} - \{j, -j\}]$

Rules
expand($C_1$) $\rightarrow C_5$
expand($C_2$) $\rightarrow C_6$
expand($C_3$) $\rightarrow C_7$
expand($C_5$) $\rightarrow C_9$
imply($C_6, C_7$) $\rightarrow C_{10}$
imply($C_9, C_{10}$) $\rightarrow C_{11}$ 

Known:
$i \in \alpha_2 \cup \beta_2$
$-i \in \alpha_3 \cup \beta_3$
$j \in \alpha_1 \cup \beta_1 \cup \delta_1$
$-j \in \alpha_2 \cup \beta_2 \cup \alpha_3 \cup \beta_3$

Two goals to derive $C_{11}$: get rid of $i$, and get rid of $j$

Known:
 - $i$ is in $C_2$ or not $C_2$ (not $C_2$ means it's in $C_5$)
 - $-i$ is in $C_3$ or not $C_3$ (not $C_3$ means it's in $C_6$)
 - could i be in $C_9$? no, this requires a duplicate or a clause that blocks no assignments
 - so i is not in $C_9$, $C_5$, or $C_1$
 - note $j$ is introduced in either $C_1$, $C_5$, or $C_9$
 - if $j$ is not in $C_5$ then all the terms in $C_5$ exist in $C_11$ so $C_5$ can expand to $C_11$ (the claim is true, end here)
 - for the other cases, assume then $j$ is in $C_5$, and not only that, if $j$ is not in $C_1$ then $C_1$ could be expanded to $C_11$ so for the rest of this section assume $j$ is in $C_1$
 - now where is $-j$? and what do we do about the i's?
 - what are the cases?
    - we know $-j$ is in $C_6$, $C_7$, or both
    - simplify this to one or both, now we have two cases
    - $-j \in C_6$ (fixed yet arbitrary since C_6 and C_7 are treated the same)
    - $-j \in C_6$ and $-j \in C_7$
    - since it's in $C_6$ both times, does it matter if it's in C_7, too?
    - So we can imply($C_1,C_6$)

imply($C_1,C_6$) $\rightarrow C_{12}$

$C_{12} := [\alpha_1 \cup \alpha_2 \cup \beta_2 - \{j, -j\}]$

and since $i$ is in $\alpha_2 \cup \beta_2$ and $-i$ is in $C_7$, 

imply($C_{12}, C_7$) $\rightarrow C_{13} \rightarrow$ expand(C_{13}) $ \rightarrow C_{11}$ 

But is $C_{12}$ shorter than n-1?

compare $C_{12}$ and $C_{11}$

$C_{12} := [\alpha_1 \cup \alpha_2 \cup \beta_2 - \{j, -j\}]$
$C_{11} := [\alpha_1 \cup \beta_1 \cup \delta_1 \cup \alpha_2 \cup \beta_2 \cup \alpha_3 \cup \beta_3 - \{i, -i\} - \{j, -j\}]$

what if the following were empty/in other sets
$\beta_1$
$\delta_1$
$\alpha_3$
$\beta_3$

Then $|C_{12}| = |C_{11}| + 2$

Want to show that at least two terms must exist in the aforementioned sets and cannot exist anywhere else.

Because this scenario is so strict (exactly n-3 expands to exactly n-2 expands to exactly n-1), there must be exactly one term in each $\beta$ and $\delta$, but perhaps they could exist in other sets...

Could $\beta_1$ exist in other sets? Consider $\beta_1 \subset \alpha_2$
No problems
Could $\delta_1$ exist in other sets? Well sure $\delta_1 \subset \beta_2$

We know at least one term must be unique to $\alpha_3$ and $\beta_3$, specifically $-i$
could $C_5$ have -i?
If $C_5$ had -i, then 

(1) and (3)
(2) and (2)
(2) and (3)