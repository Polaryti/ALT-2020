import numpy as np

def dp_levenshtein_backwards(a, b):
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    M = np.zeros((n, n))
    for i in range(1, n):
        M[i, 0] = i
        M[0, i] = i

    for col in range(1, c):
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            M[col, fil] = min(M[col - 1, fil] + 1,
                              M[col, fil - 1] + 1,
                              M[col - 1, fil - 1] + cost)
                              
    return M[c - 1, f - 1]


def dp_restricted_damerau_backwards(a, b):
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    M = np.zeros((n, n))
    for i in range(1, n):
        M[i, 0] = i
        M[0, i] = i

    for col in range(1, c):
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            M[col, fil] = min(M[col - 1, fil] + 1,
                              M[col, fil - 1] + 1,
                              M[col - 1, fil - 1] + cost,
                              M[col - 2, fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 2] else 2**32)

    return M[c - 1, f - 1]

def dp_intermediate_damerau_backwards(a,b):
    inf = 2**32
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    M = np.zeros((n, n))
    for i in range(1, n):
        M[i, 0] = i
        M[0, i] = i

    for col in range(1, c):
        for fil in range(1, f):            
            cost = not a[col - 1] == b[fil - 1]
            M[col, fil] = min(M[col - 1, fil] + 1,
                              M[col, fil - 1] + 1,
                              M[col - 1, fil - 1] + cost,
                              M[col - 2, fil - 2] + 1 if col > 2 and a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 3] else inf,
                              M[col - 2, fil - 2] + 1 if fil > 2 and a[col - 1] == b[fil - 3] and b[fil - 1] == a[col - 2] else inf,
                              M[col - 2, fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 2] else inf)

    return M[c - 1, f - 1]

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