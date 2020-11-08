import numpy as np

def DLR(a, b):
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

    # for fil in range(f):
    #     print(M[fil]) 

    return M[c - 1, f - 1]


def DLROpt(a, b):
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

if __name__ == "__main__":
    print(DLR("ayz","abc"))
    print(DLROpt("ayz","abc"))