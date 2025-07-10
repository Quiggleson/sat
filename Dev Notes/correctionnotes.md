so here's the problem
Lemma 5.11, 12, 17, 18, and 19 rely on the idea of "we can derive this clause by deriving other clauses first and these other clauses are all shorter than k because this inequality. And this inequality is true when _ exists and _ has to exist, otherwise we can derive a contradiction." But it's not a matter of existing, it's a matter of having terminals that exist in no other sets. 

For example, consider the clauses
$A := [a, b, \beta, i]$
$B := [c, d, \delta, -i]$
$E := [a, b, \beta, c, d, \delta]$
$C := [-a, f, \phi]$
$D := [b, \beta, c, d, \delta, f, \phi]$
$F := [b, \beta, i, f, \phi]$

Where 
 - A and B imply E
 - C and E imply D
 - A and C imply F
 - F and B imply D

We can go through F to derive D, now what can we say about the length of F?
Ideally, it would be less than k, but that's not so certain

$|F| = b + i + f + \beta + \phi - (\beta \phi)$
$|D| = b + c + d + f + \beta + \delta + \phi - (\beta \delta) - (\beta \phi) - (\delta \phi)$
$|D| - |F| = b + c + d + f + \beta + \delta + \phi - (\beta \delta) - (\beta \phi) - (\delta \phi) - b - i - f - \beta - \phi + (\beta \phi)$
$|D| - |F| = c + d + \delta - (\beta \delta) - (\delta \phi) - i$

nah, what do we want? oi vey idk
We want the bounds on the length of F in terms of k

Let $|D| = k$, then
$k = |b| + |c| + |d| + |f| + |\beta| + |\delta| + |\phi| - |\beta \delta| -  |\beta \phi| - |\delta \phi|$
$|F| = |b| + |i| + |f| + |\beta| + |\phi| - |\beta \phi|$
hmm... ideally it should subtract the intersection between the terminals and the generic sets of terms, try minimizing this by just writing clauses as sets of terms

$A := [\alpha]$
$B := [\beta]$
$C := [\phi]$
$E := [\alpha \cup \beta - \{i, -i\}]$
$D := [\alpha \cup \beta \cup \phi - \{i, -i\} - \{j, -j\}]$
$F := [\alpha \cup \phi - \{j, -j\}]$

Where $i, j \in \alpha, -i \in \beta, -j \in \phi$
And $-i, -j \notin \alpha, i, \notin \beta, j, \notin \phi $

Is this required to be true? $j, -j \notin \beta$ or $i, -i \notin \phi$

Suppose $j \in \beta$

$A := [i, j, a]$
$B := [-i, j, b]$
$C := [-j, c]$
$E := [j, a, b]$
$D := [c, a, b]$

Then $|D|$ > $|E|$, but do we care?

Alright we need to fix k because we want to know how the intermediate terms react in terms of k

Pause

Now $D$ is of length $k$, what can be said about $|F|$?
$|F|$ is 2 more than $|D|$ minus $|\beta'|$ where $\beta'$ is the set of terms in $\beta$ in no other set.
$\beta'$ does contain $i$
$|F| = |D| + 2 - |\beta'|$

Continue

Let's consider the best case scenario: we can derive clauses of length k by processing clauses with a maximum length of k + 2

Step 1: expand up to n-terminal clauses
Step 2: reduce to n-1 terminal clauses, note that we still need the n-terminal clauses
Then reduce to n-2 terminal clauses, still need to process n-t
Now we reduce to n-3 terminal clauses, can we get there without processing clauses of length n?
Welp maybe
How do we know we have all the n-1 and n-2 terminal clauses
Alright, imagine the shape of reducing, we have all the n-terminal clauses we need and we reduce to n-1 terminal clauses then we reduce to n-2 and n-3.
We know we have all the n-2 terminal clauses needed to reduce, but we had to process n-terminal clauses to get those. However, in deriving the n-2 terminal clauses, we can trace the n-terminal clauses back to the n-1 and n-2 terminal clauses that were used to derive them. And we can use those directly to derive the n-3 terminal clauses without ever having to process a clause with a length of n.

In general, we have a clause of length k we are deriving. Recall the bounds for deriving a clause: By Lemma 5.9, two clauses of lengths k and m will derive a clause in the range max(k, m) - 1 to k + m - 2. So The largest clause that could be the input to output a k-terminal clause is of length k + 1. And we know this k+1 clause came from smaller clauses or k+2-t clauses.
Dang, but how do we know we have all the k+1-t clauses we need?

---
Given an unsat instance, derive contra 1-t clauses in poly time
Step 1
Input: given 3-t clauses
Output: necessary n-t clauses
Time: exponential
Step 2:
Input: necessary n-t clauses
Output: necessary n-1-t clauses
Time: poly

---
Well we know it's reduction at the end so
A (n-1) -> C (n)
B (n-1) -> D (n) -> E (n-1)
How can we get E?
$A := [\alpha]$
$B := [\beta]$
$C := [\alpha \cup \delta]$
$D := [\beta \cup \phi]$
$E := [\alpha \cup \delta \cup \beta \cup \phi - \{i, -i\}]$

$F := [\alpha \cup \beta - \{i, -i\}]$

3 cases
 1. opposite form term dne in A or B
 2. exists in either A or B
 3. exists in both

(1) If $i \notin \alpha$, then $A \subseteq  E$, which in the case of n-1-t clauses means $A = E$
(2) If $i \in \alpha$ then $-i \notin \beta$ and $B \subseteq E$, which in the case of n-1-t clauses means $B = E$
(3) If $i \in \alpha$ and $-i \in \beta$ then we can use the intermediate clause F to derive E. What's the length of F?

Say either C or D is of length k and E is shorter than k. Say D is of length k. Now all but one of the terms in C exist in D.
Who cares?
D is of length k, E is of length k or k-1, how big is F?
$D := [\beta \cup \phi]$
$E := [\alpha \cup \delta \cup \beta \cup \phi - \{i, -i\}]$

$F := [\alpha \cup \beta - \{i, -i\}]$

What if $\delta \subseteq \beta$ and perhaps $\phi \subseteq \alpha$? Then if E is of length k, so is F

$A := [1, 2, 3]$
$B := [-1, 2, 4]$
$C := [1, 2, 3, 4]$
$D := [-1, 5, 3, 4]$
$E := [2, 3, 4, 5]$

$F := [2, 3, 4]$

--- 
oi vey, alright what's our end goal?
The old way relied on "we don't need n-terminal clauses to get all the n-1-terminal clauses we need" and "we don't need n-1-terminal clauses to get all the n-2-terminal clauses we need", but now we *do* need clauses of length k+1 to derive clauses of length k, and in the best case scenario, it will be like "we may have to process clauses of length k+1 to derive the clauses of length k, but we can just use the smaller clauses that were used to derive the k+1-terminal clauses to derive the k+1-terminal clauses w/o processing clauses of length k+2"

```
A(k+3)
B(k+3) -> I(k+2)
C(k+3)
D(k+3) -> J(k+2) -> M(k+1)
E(k+3)
F(k+3) -> K(k+2)
G(k+3)
H(k+3) -> L(k+2) -> N(k+1) -> O(k)
```

We know all the k+3-terminal clauses can be traced back to a set of 3-terminal clauses, say GC, but will we be able to derive the k-terminal clause by only processing clauses of length k+1 using GC? Hopefully yes

Suppose not?
Maybe rework the old way - (look at just k+2) we know there are a finite number of ways any given k+2 clause can be derived, it just *may* end up required a k+3-terminal clause. However we may not need to directly process the k+3-terminal clause if we just have the set of k+2 terminal clauses that are needed. Perhaps if we use these k+2 terminal clauses required to derive I (by going through a k+3-terminal clause) in addition to the k+2-terminal clauses required to derive J (by going through a k+3-terminal clause) then we know there will be some opposite form term in I and J and perhaps we can derive M by processing clauses with a maximum length of k+2

---

hmmm there's a missing step
Even if we can say "input clauses of length k-1, we can derive a clause of length k by processing a clause with a max length of k+1", what do we know about the input clauses?
Well, they must have been derived at some point. And ideally we can say the input clauses of length k-1 were derived by processing clauses with a maximum length of k.

Step 1. 
input < k 
output k or k-1
How do we get the < k clauses?
Step 0.
Input X, but process up to k-terminal clauses
And how do we get X?
Oi vey, there are quite a few ways.

Let's enumerate the possibilities:
A clause, C of length k, can be derived by Lemma 5.8 or 5.9
```
A
B -> C
OR
D -> C
```
What can be said about A, B, and D?
|C| is in the range $[max(|A|, |B|) - 1, |A| + |B| - 2]$
So if C is of length k, then
max(|A|, |B|) - 1 <= k <= |A| + |B| - 2
max(|A|, |B|) - 1 <= k
max(|A|, |B|) <= k + 1

k + 1 >= max(|A|, |B|)
k + 2 <= |A| + |B|

The maximum of |A| and |B| is k + 1
The minimum of |A| + |B| is k + 2
The smallest |A| and |B| occurs when |A| = |B|
and |A| = |B| = k/2 + 1

alright what I really want is

"I know A, B, and D were derived by a schmorgesborg of clauses of length k+2 and up, but I also know those clauses were derived from 3-terminal clauses (and at some point passed k-terminal clauses) and I want to use those 3-terminal clauses (or k-terminal clauses) to directly imply C without processing a clause of length k + 2 or greater."

or

if we have a bunch of n-terminal clauses and we reduce them to n-1-terminal clauses processing clauses.. no the problem with this is "we agree that given k-1-terminal clauses that imply k-terminal clauses, you can derive a k or k-1-terminal clause processing clauses with a max length of k+1, but you have to process a clause of potentially up to k, k+1, and k+2 to derive the input k-1-terminal clauses"

However we do know potential paths to get from k+2 to k-1

$X_1$
$X_2 \rightarrow Y_1$
$X_3$
$X_4 \rightarrow Y_2 \rightarrow Z_1$
$X_5$
$X_6 \rightarrow Y_3$
$X_7$
$X_8 \rightarrow Y_4 \rightarrow Z_2 \rightarrow W_1$

Where $|X_i| = k + 2$, $|Y_i| = k + 1$, $Z_i = k$, and $|W_i| = k - 1$

And for each $X_i$:

$V_a \rightarrow V_b \rightarrow V_c \rightarrow ... \rightarrow X_i$

Where $|V_i| < k + 2$

So we have a set of $V$ clauses that are shorter than k + 2 and are used to imply k+2-terminal clauses, but they could use a potentially wild, wild path.
Well we do know they are upper bounded by some value because if they ever get to imply a clause of length k + 4, then we can just reset and find a new set of V's that imply that 4-terminal clause and we can derive the k+2-terminal clause by processing clauses with a max length of k+3.
So the highest an intermediate clause can get is of length k+3, but we already know this. We don't actually have to derive the k+2-terminal clause, we just need to use the given clauses that derived it to derive this new k or k-1-terminal clause by processing clauses with a max length of k+1.

Want to show that these V clauses are all we need to derive W by processing clauses with a maximum length of k+1.

What do we know about these V clauses?
They can either expand to W or not. If they can, it's easy, so assume they cannot.
Now we know the V-clauses cannot expand to W.
We know the V-clauses eventually derive the X-clauses.
All of the terms in the X clauses exist in the V-clauses? naaahhhhh
```
[a, -i]
[a, i] -> [a] -> [a, b, c]
                 [-a, c]   -> [b, c] -> [b, c, d]
```
one term in the X clauses exist in the V clauses? idk maybe
All of the V-clauses eventually derive the X-clauses and each step is either Lemma 5.8 or 5.9

Generally, we have the algorithm
Each step is
$C_i \rightarrow C_{i+1}$ or
$C_i, C_j \rightarrow C_{i+1}$
Where $C_i$ and $C_j$ exist in the instance and $C_{i+1}$ is the next clause in the path to the X-clause

---

The lemmas do not matter beyond the k+1-terminal clauses.

Search for a general theorem that states

If an instance of 3SAT is unsatisfiable then every possible clause can be derived (by Lemmas 5.8 and 5.9) by processing clauses with a maximum length of 4.

---

The idea changes a bit, it's no longer "the input clauses are remanaged to derive the output clauses", it's "the inputs of the inputs of the ... of the inputs (continue until you get input shorter than k) are remanaged to derive the output clauses without processing a clause of length k+2 or greater"

The real hard part here is now considering the paths to get from the shorter clauses to the input clauses. Well if the input clauses are of length k-1, then they can be derived by processing clauses of length k, but *those* input clauses required clauses of length k+1. Problem: the worst case keeps getting bigger, how do we know when to get the shorter clauses?

Alright let's consider a case:
```
A (< k)
B (< k) -> C (k or k-1)
```
C can be derived by processing clauses with a max length of k+1
```
D (k)
E (< k + 1) -> A (< k)
```
```
F (k)
G (< k + 1) -> B (< k)
```

you really need to find this theorem, these clauses are nearly useless without it - not exactly, if we know that certain patterns have certain bounds for the lengths of the implied clauses, then we can use some of that info. For example, lemma 5.12 allows you to derive the output clause by processing clauses with a max length of k-1. Granted, the input clauses could still require an exponential time to generate, but if we can say that this step exists on a path, then that step will not require the lengths of the clauses to grow.

Say we have the following sets of clauses:
 - $V$, the given clauses
 - $V_1$, the sets of clauses implied by $V$
   - Where $V_{1, j}$ could have length 2, 3, or, 4
 - $V_2$, the sets of clauses implied by the instance after deriving $V_1$
   - Where $V_{2, j}$ could have length [1, 6]
 - $V_3$, the sets of clauses implied by the instance after deriving $V_2$
   - Where $V_{3, j}$ could have length [1, 10]
 - ...
 - $V_i$, the sets of clauses implied by the instance after deriving $V_{i-1}$
   - Where $V_{i, j}$ could have length [1, $X$]
 - max lengths: 3, 4, 6, 10, 18, 34
 - ``(((x*2-2)*2-2)*2-2)``
 

---

A (n-1) -> B (n) -> C (n-1) -> D (n) -> E (n-1) -> F (n-2)

or more specifically

A (n-1) -> B (n) -> C (n-1) -> D (n-2)

Can we derive F/D without processing a clause of length n?

We know
 - two clauses in C must share opposite form terms
 - all but one term in the clauses in C must be shared
 - two clauses in B must share opposite form terms
 - all but one term in the clauses in B must be shared
 - A implies B by lemma 5.8 or 5.9

$C_1 := [\alpha \cup \{i\}]$

$C_2 := [\alpha \cup \{-i\}]$

$D_1 := [\alpha]$

$B_1 := [\alpha \cup \{i\} \cup \{j\}]$

$B_2 := [\alpha \cup \{i\} \cup \{-j\}]$

$B_3 := [\alpha \cup \{-i\} \cup \{k\}]$

$B_4 := [\alpha \cup \{-i\} \cup \{-k\}]$

Where j could equal k

Some cases for $C_1$ implying $B_1$

(1) $C_1$ expands to $B_1$
$C_1 := [\alpha \cup \{i\}]$
$C_1 := [\alpha \cup \{j\}]$
$C_1 := [\{i\} \cup \{j\} \cup \alpha']$

where $\alpha'$ has one term from $\alpha$ removed

(2) $C_1$ implies $B_1$ by Lemma 5.9

Then we have $C_1$ and $C_2$ that share an opposite form term and everything else is in $B_1$

$C_1 := [\beta]$
$C_2 := [\delta]$
where 
$\beta \cup \delta - \{m, -m\} = \alpha \cup \{i\} \cup \{j\}$

so 

$\alpha \cup \{i\} \cup \{j\} \subseteq \beta \cup \delta$

---

Given a 3-t clause that implies another 3-t clause by processing a 4-t clause, can we be sure no additional 3-t clauses can be implied by processing 5- or more -terminal clauses?

And that is the million dollar question