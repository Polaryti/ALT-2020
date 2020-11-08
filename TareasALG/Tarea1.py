import numpy as np

def levenshtein(a, b):
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

    # for fil in range(f):
    #     print(M[fil]) 

    return M[c - 1, f - 1]

def levenshteinOpt(a, b):
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

if __name__ == "__main__":
    print(levenshtein("ho","hola"))
    print(levenshteinOpt("ho","hola"))