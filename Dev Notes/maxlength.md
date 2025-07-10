These are notes about the length of the longest clause required to be processed. Hopefully it's 6.

Reminder how 5.11 fails:

```
A := [-3, 4, 5]
B := [1, 2, 3]
C := [1, 2, -5]
E := [1, 2, 4, 5]
D := [1, 2, 4]
F := [1, 2, -3, 4]

```
It is seen 

```
A + B -> E
E + C -> D
```
But you must process a 4-t clause to derive D. Now, why is this the case?

Consider the assignment table for $D$

|$x_1$|$x_2$|$x_3$|$x_4$|$x_5$|blocked|
|---|---|---|---|---|---|
|0|0|0|0|0|B and E
|0|0|0|0|1|B and C
|0|0|1|0|0|A and E
|0|0|1|0|1|C

How would we know A only blocks one? Because it only shares one terminal so the resulting clause from combining A and D is a 5-t clause, ``[1, 2, -3, 4, 5]``, perhaps? And the other clauses, A and C, share two terminals with D so the resulting clauses are 4-t, ``[1, 2, 3, 4]`` and ``[1, 2, 4, -5]``

Okay that's all fine and dandy, but how does this (1) help us limit the length of the longest clause we need to process and (2) tell us anything we need to know about the original three clauses without relying on information from the final clause?

The longest clause that can be "derived" by sticking two clauses together is 6-t. Is there any reason you would have to stick together more clauses? Consider a 7 terminal assignment table for all assignments blocked by a 3-t clause:

```
A := [1, 2, 3]
B := [4, 5, 6]
C := [4, 5, 7]
```

|$x_1$|$x_2$|$x_3$|$x_4$|$x_5$|$x_6$|$x_7$|blocked|
|---|---|---|---|---|---|---|---|
|0|0|0|0|0|0|0|B and C|
|0|0|0|0|0|0|1|B|
|0|0|0|0|0|1|0|C|
|0|0|0|0|0|1|1|
|0|0|0|0|1|0|0|
|0|0|0|0|1|0|1|
|0|0|0|0|1|1|0|
|0|0|0|0|1|1|1|
|0|0|0|1|0|0|0|
|0|0|0|1|0|0|1|
|0|0|0|1|0|1|0|
|0|0|0|1|0|1|1|
|0|0|0|1|1|0|0|
|0|0|0|1|1|0|1|
|0|0|0|1|1|1|0|
|0|0|0|1|1|1|1|

Here A + B block the first two rows

Would you ever need to process a 7-t clause?

You need to process a 4-t clause in the first table because no two clauses span the whole table. Maybe similarly here, you can span the whole table without a 7-t clause. Eventually WTS you can span every table with at most a 6-t clause.

If two clauses, A and B, block some set of assignments, you can block these same assignments by combining A and B. Unless, what about A := [1, 2, 3] and B := [-1, -2, 3]?

Correction: if any number of assignments share the same value for the same terminal, say K times, then these assignments can be blocked by a single clause whose longest possible length is K. Note that it may not be valid to add this clause, as it may block other, unblocked assignments.

|$x_1$|$x_2$|$x_3$|blocked|
|---|---|---|---|
|0|0|0|A
|0|0|1|
|0|1|0|
|0|1|1|
|1|0|0|
|1|0|1|
|1|1|0|B
|1|1|1|

Suppose you have an assignment table for a clause, [1, 2, 3]. You combine everything you can and run out of new derivations at 6-t clauses. What do we know?

- We can (exponentially) derive a clause for every [1, 2, 3, 4, 5, ... n] for all combinations of positive and negative 4, 5, ..., n.
- Each 3, 4, 5, and 6-t clause can be traced to the corresponding n-t clause
- We cannot derive any more clauses without going over 6-t
- Is it possible we have yet to derive [1, 2, 3]?
  - Say yes, then
    - there must be a K-terminal clause required to derive [1, 2, 3] where K > 6
    - eventually there will come The Great Collapse where the K-t clauses go from K -> K - 1 -> K - 2 -> ... -> 4 -> 3
    - Each K-t clause will have K-3 terminals which are the opposite form of the same terms in other K-t clauses
    - X
  - Say no

Why 5.11 fail? Why did we have to process a 4-t clause?
We were deriving D := [1, 2, 4] and we had
```
A := [-3, 4, 5]
B := [1, 2, 3]
C := [1, 2, -5]
```

Keep in mind we didn't know the goal was D:= [1, 2, 4]. We had to derive a 4-t clause because:

- A, B, C implied D, but no combo of A, B, or C implied a 3-t clause
- The upper bound of the length of an implied clause by 5.9 is 2k-2, which is 4 here
- Looking at the assignment table, there is no selection of two 3-t clauses which block the whole table

Is there any way we could've known it would only take a 4-t clause?

Each implication can (1) add needed terminals (2) add unnecessary terminals (3) remove unnecessary terminals (4) remove necessary terminals. So what's stopping something like the following:

```
Want A := [1, 2, 3]

Have
B := [1, 4, 5]      (working: [1, 4, 5])
C := [-4, 6, 7]     (working: [1, 5, 6, 7])
D := [-6, 8, 9]     (working: [1, 5, 7, 8, 9])
E := [-7, 10, 11]   (working: [1, 5, 8, 9, 10, 11])

(now must remove 5, 8, 9, 10, 11)
(and add 2, 3)
F := [2, -11, 12]   (working: [1, 2, 5, 8, 9, 10, 12])
G := [3, -12, 11]   (working: [1, 2, 3, 5, 8, 9, 10, 11])

(now must remove 5, 8, 9, 10, 11)
H := [-5, 8, 10]    (working: [1, 2, 3, 8, 9, 10, 11])
I := [-8, 9, 11]    (working: [1, 2, 3, 9, 10, 11])
J := [-9, 3, 10]    (working: [1, 2, 3, 10, 11])
K := [-10, 1, 3]    (working: [1, 2, 3, 11])
L := [-11, 2, 3]    (working: [1, 2, 3])

```

- you can only remove one at a time (time meaning one clause)
- you can add up to two at a time
- because you must remove every non-essential terminal you add, these two opposite form terms both exist in the original 3-t clauses (TODO: double check this) so you can process them together immediately. However, this could make a 4-t clause and there *may* be no way to guarantee it will stay under some limit 

Unless it hits a 2-t clause before the 3-t (like it derives [1, 2, 4] then [1, 2, -4] then [1, 2] and finally [1, 2, 3]), then there will be (1) a clause which shares two terms and whose third term is used to remove an unnecessary term ([-11, 2, 3] above) and (2) a clause which shares at least one term as well as the negation of an unnecessary term. The third term can either be an unnecessary term (contained in the working clause) or a necessary term (seen as [-10, 1, 3] above)

What about hitting a 2-t clause first? Or in the case where the instance uses the eight forms [1, 2, 3] and never even touches x_4? Hmm I don't think we care about that too much since we're only looking to show that every added unnecessary clause will eventually be removed so we can take the clauses that remove it and process them in a different order to limit the length of the clauses required to be processed. 

Why on earth would order matter? And can we guarantee some maximum length clause? We know the following:
- Each clause in the pattern can 
  - Add 1, 2, or 3 unnecessary terms
  - Add 1 or 2 necessary terms (adding 3 would just be the target clause)
  - Remove 1 unnecessary term
  - Remove 1 unnecessary term and add 1 or 2 more
  - Remove 1 unnecessary term and 1 or 2 necessary terms
  - (potentially) Remove 1 necessary term and add 1 or 2 necessary/unnecessary terms
- All of the unnecessary terms must be removed (however, do we know this isn't done by a clause which first must be derived? Yes, I'm pretty confident we're good)
- Note: if you have clauses like: [1, 2, 3, 4, 5, 6] and [1, 2, 3] then sure you could remove the [6] by deriving [1, 2, 3, -6], but you won't get anything you don't already have. You could just directly get [1, 2, 3, 4, 5] from [1, 2, 3]
- When removing an unnecessary term, the other terms in the clause MUST be in the working clause. However, upon reordering the processing, the working clause may be different so what used to just remove a term now may remove and add a term

Do some work with the following:

```
Want A := [1, 2, 3]

Have
B := [1, 4, 5]      (working: [1, 4, 5])
^ Init; add 1 necessary, 2 unnecessary
C := [-4, 6, 7]     (working: [1, 5, 6, 7])
^ Remove 1 unnecessary, add 2 unnecessary
D := [-6, 8, 9]     (working: [1, 5, 7, 8, 9])
^ Remove 1 unnecessary, add 2 unnecessary
E := [-7, 10, 11]   (working: [1, 5, 8, 9, 10, 11])
^ Remove 1 unnecessary, add 2 unnecessary

(now must remove 5, 8, 9, 10, 11)
(and add 2, 3)
F := [2, -11, 12]   (working: [1, 2, 5, 8, 9, 10, 12])
^ Remove 1 unnecessary, add 1 necessary, add 1 unnecessary
G := [3, -12, 11]   (working: [1, 2, 3, 5, 8, 9, 10, 11])
^ Remove 1 unnecessary, add 1 necessary, add 1 unnecessary

(now must remove 5, 8, 9, 10, 11)
H := [-5, 8, 10]    (working: [1, 2, 3, 8, 9, 10, 11])
^ Remove 1 unnecessary
I := [-8, 9, 11]    (working: [1, 2, 3, 9, 10, 11])
^ Remove 1 unnecessary
J := [-9, 3, 10]    (working: [1, 2, 3, 10, 11])
^ Remove 1 unnecessary
K := [-10, 1, 3]    (working: [1, 2, 3, 11])
^ Remove 1 unnecessary
L := [-11, 2, 3]    (working: [1, 2, 3])
^ Remove 1 unnecessary

---

G + L -> M := [3, -12, 2]
M + F -> N := [3, 2, -11]

To rid the -11, we could use E, (G), or I. Don't want to reuse G.

N + E -> O := [-7, 10, 2, 3]
O + K -> P := [-7, 2, 3, 1]
C + P -> too big :(

---

J + K -> Q := [-9, 3, 1]
Q + I -> R := [-8, 11, 3, 1]


```

Dang, these get difficult to control. How can we know of the maximum? We know one clause contains two terms we're looking for and the opposite of an unnecessary term, like [1, 2, -4] and another clause contains one necessary term, one opposite of a term in the working clause, and one other term in the working clause, like [3, -5, 6]. Then after that, each clause could do any one of the four things

Path looked kinda like this:
Want: 0.3

Init: + 2.1
= 2.1
-1 + 2
= 3.1
-1 + 2
= 4.1
-1 + 2
= 5.1
-1 + 1.1
= 5.2
-1 + 1.1
= 5.3
-1
= 4.3
-1
= 3.3
-1
= 2.3
-1
= 1.3
-1
= 0.3 

The difficulty lies in the fact that not each -1 + 2 or the like will always be the same. It depends on order. It would be nice to start with the final steps at the beginning, but those -1's will likely become +2's

There are two clauses that we know will always contain some of the target clause's terms:
- The final clause (contains two of the target terms and opposite of one extra)
- The second to final clause (contains one of the target terms, one opposite of an extra, and one more from the working clause)
- I suppose the initial clause contains at least one target term and two others to populate the working clause