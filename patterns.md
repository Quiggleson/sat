|a| c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | 
|---|---|---|---|---|---|---|---|---|---|---|
|Clause|$(x_1 \vee x_2 \vee x_3)$|

### Lemma 1 - referencing a clause
WTS a way to give each clause a decimal value
$ \sum_{j=1}^{3} 2^j$
where $j$ is the subscript for each variable in the clause
$2^1 + 2^2 + 2^3 = 14$
$2^1 + 2^2 + 2^4 = 22$
$2^-1 + 2^2 + 2^3 = 10$
$2^1 + 2^2 + 2^3 = 14$
nah doesn't work $:<$


### Looping through clauses
WTS an algorithm to loop through clauses
Fix an n
Try k possible clauses for each 1 < k < n

i,j,l
```py

clauses = []
For i in range(3,n):
    For j in range(2,i):
        For l in range(1,j):
            clauses.add([l,j,i])
```