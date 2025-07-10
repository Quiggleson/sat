Given the following path

A n - 2
B n - 2 -> E n - 2
C n - 2
D n - 2 -> F n - 2 -> G n - 3

Where each of the n-1-terminal clauses can be derived in one of the four following ways:

(1) 

n - 3 -> n - 2 -> n - 1

(2)

n - 3 -> n - 2 
n - 3 -> n - 2 -> n - 1

(3)

n - 3 -> n - 2 
n - 3 -> n - 2 -> n - 2 -> n - 1

(4)

n - 3 -> n - 2 
n - 3 -> n - 2 -> n - 3 -> n - 2 -> n - 1

Which, in reality, boils down to one of two choices:

(1) the n-1-t clause is expanded to by clauses shorter than n-1
(2) the n-1-t clause is implied by lemma 5.9 using clauses shorter than n-1

Can you derive the final n-3-terminal clause without processing an n-1-terminal clause?

Define the clauses in the following manner:

$A := [\alpha]$

$B := [\beta]$

$C := [\delta]$

$D := [\phi]$

$E := [\alpha \cup \beta - \{i, -i\}]$

$F := [\delta \cup \phi - \{j, -j\}]$

$G := [\alpha \cup \beta \cup \delta \cup \phi - \{i, -i\} - \{j, -j\}]$

Where $i \in \alpha$, $-i \in \beta$, $j \in \delta$, $-j \in \phi$
And $-i \notin \alpha$, $i \notin \beta$, $-j \notin \delta$, $j \notin \phi$

Know $A$ can be derived in the following manner

