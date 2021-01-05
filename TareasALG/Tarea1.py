import numpy as np

def dp_levenshtein_backwards(a, b):
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    V1 = np.zeros(n)
    V2 = np.zeros(n)
    for i in range(n):
        V1[i] = i
    
    # print(V1)
    for col in range(1, c):
        V2[0] = col
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            V2[fil] = min(V1[fil] + 1,
                          V2[fil - 1] + 1,
                          V1[fil - 1] + cost)
        V1, V2 = V2, V1
        # print(V1)

    return V1[f - 1]

def dp_restricted_damerau_backwards(a, b):
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    V1 = np.zeros(n)
    V2 = np.zeros(n)
    V3 = np.zeros(n)
    for i in range(f):
        V1[i] = i
        
    if len(a) > 1:
        V2[0] = 1
        for i in range(1, f):
            cost = not a[0] == b[i - 1]
            V2[i] = min(V1[i] + 1,
                        V2[i - 1] + 1,
                        V1[i - 1] + cost)
    # print(V1)
    # print(V2)
    for col in range(2, c):
        V3[0] = col
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            V3[fil] = min(V2[fil] + 1,
                              V3[fil - 1] + 1,
                              V2[fil - 1] + cost,
                              V1[fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 2] else 2**32)
        V1, V2, V3 = V2, V3, V1
        # print(V2)

    return V2[f - 1]

def dp_intermediate_damerau_backwards(a, b):
    inf = 2**32
    c = len(a) + 1
    f = len(b) + 1
    V1 = np.zeros(f)
    V2 = np.zeros(f)
    V3 = np.zeros(f)
    V4 = np.zeros(f)

    for i in range(f):
        V1[i] = i

    if len(a) > 0:
        V2[0] = 1
        for i in range(1, f):
            cost = not a[0] == b[i - 1]
            V2[i] = min(V1[i] + 1,
                        V2[i - 1] + 1,
                        V1[i - 1] + cost)
    else: return len(b)

    if len(a) > 1:
        V3[0] = 2
        for i in range(1, f):
            cost = not a[1] == b[i - 1]
            V3[i] = min(V2[i] + 1,
                        V3[i - 1] + 1,
                        V2[i - 1] + (0 if a[1] == b[i - 1] else 1),
                        (V1[i - 3] + 2) if i > 2 and a[0] == b[i - 1] and a[1] == b[i - 3] else inf,
                        (V1[i - 2] + 1) if i > 1 and a[0] == b[i - 1] and a[1] == b[i - 2] else inf)
    else: return len(b) - (1 if a[0] == b[0] else 0)
    for j in range(3, c):
        V4[0] = j
        for i in range(1, f):
            cost = not a[j - 1] == b[i - 1]
            V4[i] = min(V3[i] + 1,
                        V4[i - 1] + 1,
                        V3[i - 1] + cost,
                        (V2[i - 3] + 2) if i > 2 and a[j - 2] == b[i - 1] and a[j - 1] == b[i - 3] else inf,
                        (V2[i - 2] + 1) if i > 1 and a[j - 2] == b[i - 1] and a[j - 1] == b[i - 2] else inf,
                        (V1[i - 2] + 2) if i > 1 and a[j - 3] == b[i - 1] and a[j - 1] == b[i - 2] else inf)
        V1, V2, V3, V4 = V2, V3, V4, V1
    return V3[f - 1]

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                      (dp_restricted_damerau_backwards,"restricted"),
                      (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                 
"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""    