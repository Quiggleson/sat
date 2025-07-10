Tree for $i$
```mermaid
flowchart TD
    t1["i in C_6"] --> t2["i in C_2"]
    t1 --> t3["i not in C_2"]
    t2 --> t4["i not in beta_2"]
    t3 --> t5["i in beta_2"]

```
Tree for $-i$
```mermaid
flowchart TD
    t1["-i in C_7"] --> t2["-i in alpha_3"]
    t1 --> t3["-i not in alpha_3"]
    t2 --> t4["-i not in beta_3"]
    t3 --> t5["-i in beta_3"]
```
Tree for $j$
```mermaid
flowchart TD
    t1["j in C_9"] --> t2["j in alpha_1"]
    t1 --> t3["j not in alpha_1"]
    t2 --> t4["j not in beta_1"]
    t2 --> t5["j not in delta_1"]
    t3 --> t6["expand(C_1) -> C_11"]
    t6 --> t7["done"]
```
Tree for $-j$
```mermaid
flowchart TD
    t1["-j in C_10"] --> t2["-j in C_6"]
    t1 --> t3["-j not in C_6"]
    t2 --> t4["-j in alpha_2"]
    t2 --> t5["-j not in alpha_2"]
    t4 --> t6["-j not in beta_2"]
    t5 --> t7["-j in beta_2"]
    t3 --> t8["-j in C_7"]
    t8 --> t9["-j in alpha_3"]
    t8 --> t10["-j not in alpha_3"]
    t9 --> t11["-j not in beta_3"]
    t10 --> t12["-j in beta_3"]

```
Now we know all of the potential locations for i, -i, j, and -j
Let's combine some trees

Combine i and -i
```mermaid
flowchart TD
    t1["i in C_6"] --> t2["i in C_2"]
    t1 --> t3["i not in C_2"]
    t2 --> t4["i not in beta_2"]
    t3 --> t5["i in beta_2"]
    
    a1["-i in C_7"] --> a2["-i in alpha_3"]
    a1 --> a3["-i not in alpha_3"]
    a2 --> a4["-i not in beta_3"]
    a3 --> a5["-i in beta_3"]
```
Not much can be said
Add the j-tree

```mermaid
flowchart TD
    t1["i in C_6"] --> t2["i in C_2"]
    t1 --> t3["i not in C_2"]
    t2 --> t4["i not in beta_2"]
    t3 --> t5["i in beta_2"]
    
    a1["-i in C_7"] --> a2["-i in alpha_3"]
    a1 --> a3["-i not in alpha_3"]
    a2 --> a4["-i not in beta_3"]
    a3 --> a5["-i in beta_3"]
    
    b1["j in C_9"] --> b2["j in alpha_1"]
    b1 --> b3["j not in alpha_1"]
    b2 --> b4["j not in beta_1"]
    b2 --> b5["j not in delta_1"]
    b3 --> b6["expand(C_1) -> C_11"]
    b6 --> b7["done"]
```

drats, no real info can be gained, alright combine them all
```mermaid
flowchart TD
    t1["i in C_6"] --> t2["i in C_2"]
    t1 --> t3["i not in C_2"]
    t2 --> t4["i not in beta_2"]
    t3 --> t5["i in beta_2"]
    
    a1["-i in C_7"] --> a2["-i in alpha_3"]
    a1 --> a3["-i not in alpha_3"]
    a2 --> a4["-i not in beta_3"]
    a3 --> a5["-i in beta_3"]
```

```mermaid
flowchart TD
    b1["j in C_9"] --> b2["j in alpha_1"]
    b1 --> b3["j not in alpha_1"]
    b2 --> b4["j not in beta_1"]
    b2 --> b5["j not in delta_1"]
    b3 --> b6["expand(C_1) -> C_11"]
    b6 --> b7["done"]
    
    c1["-j in C_10"] --> c2["-j in C_6"]
    c1 --> c3["-j not in C_6"]
    c2 --> c4["-j in alpha_2"]
    c2 --> c5["-j not in alpha_2"]
    c4 --> c6["-j not in beta_2"]
    c5 --> c7["-j in beta_2"]
    c7 --> c13["i in C_6"]
    c13 --> c14["i in C_2"]
    c13 --> c15["i not in C_2"]
    c14 --> c16["i not in beta_2"]
    c15 --> c17["i in beta_2\ncontradiction\ni in C_2"]
    c18["-j in beta_2\ni in C_2 (alpha_2)\nj in alpha_1"]
    c17 --> c18
    c16 --> c18
    c18 --> c19["-i in C_7"]
    c19 --> c20["-i in alpha_3"]
    c19 --> c21["-i not in alpha_3"]
    c20 --> c22["-i not in beta_3"]
    c21 --> c23["-i in beta_3"]
    c3 --> c8["-j in C_7"]
    c8 --> c9["-j in alpha_3"]
    c8 --> c10["-j not in alpha_3"]
    c9 --> c11["-j not in beta_3"]
    c10 --> c12["-j in beta_3"]
```
