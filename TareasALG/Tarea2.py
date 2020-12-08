import numpy as np

def dp_levenshtein_backwards(a, b,thr=2**31):
    c = len(a) + 1
    f = len(b) + 1
    n = max(c,f)
    V1 = np.zeros(n)
    V2 = np.zeros(n)
    for i in range(n):
        V1[i] = i
    
    for col in range(1, c):
        V2[0] = col
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            V2[fil] = min(V1[fil] + 1,
                          V2[fil - 1] + 1,
                          V1[fil - 1] + cost)
        V1, V2 = V2, V1
        if min(V1) > thr: return thr + 1
    if V1[f - 1] > thr: return thr + 1
    return V1[f - 1]

def dp_restricted_damerau_backwards(a, b, thr=2**31):
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
    
    if min(V2) > thr: return thr + 1
    for col in range(2, c):
        V3[0] = col
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            V3[fil] = min(V2[fil] + 1,
                              V3[fil - 1] + 1,
                              V2[fil - 1] + cost,
                              V1[fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 2] else 2**32)
        V1, V2, V3 = V2, V3, V1
        if min(V2) > thr: return thr + 1
    if V2[f - 1] > thr: return thr + 1
    return V2[f - 1]

def dp_intermediate_damerau_backwards(a, b, thr = 2**31):
    inf = 2**32
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
    if min(V2) > thr: return thr + 1
    if len(a) > 2:
        V3[0] = 2
        for i in range(1,f):
            cost = not a[1] == b[i - 1]
            V3[i] = min(V2[i] + 1,
                                V3[i - 1] + 1,
                                V2[i - 1] + cost,
                                V1[i - 2] + 1 if a[1] == b[i - 2] and b[i - 1] == a[0] else inf)
    V1, V2, V3 = V2, V3, V1
    if min(V2) > thr: return thr + 1
    for col in range(3, c):
        V3[0] = col
        for fil in range(1, f):
            cost = not a[col - 1] == b[fil - 1]
            V3[fil] = min(V2[fil] + 1,
                              V3[fil - 1] + 1,
                              V2[fil - 1] + cost,
                              V1[fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 3] else inf,
                              V1[fil - 2] + 1 if fil >= 2 and b[fil - 1] == a[col - 2] and a[col - 1] == b[fil - 3] else inf,
                              V1[fil - 2] + 1 if a[col - 1] == b[fil - 2] and b[fil - 1] == a[col - 2] else inf)
        V1, V2, V3 = V2, V3, V1
        if min(V2) > thr: return thr + 1
    if V2[f - 1] > thr: return thr + 1
    return V2[f - 1]