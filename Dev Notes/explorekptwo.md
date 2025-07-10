idk why this file is named like this.

Alright we are exploring

k --> ? --> k + 2 --> ? --> k + 1 --> k

and we know we are allowed to process clauses up to length k + 1

Want to show we can derive that last k-t clause by processing clauses with a maximum length of k+1.

Since we have clauses of length k+1, we can imagine there exists at least one k+2-t clause that does not rely on any other k+2-t clauses

they can exist in one of three ways

(1)

``k + 1 --> k + 2``

(2)
```
   k + 1 --
<= k + 1 ----> k + 2
```
(3)
```
   k -- 
<= k ----> k + 2
```
Now consider any further derivation done with these k+2-t clauses

Specifically
```
   k + 2 --
<= k + 2 ----> k + 1 --> ?
```

