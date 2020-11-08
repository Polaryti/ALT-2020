# -*- coding: utf-8 -*-
import sys

def langford_directo(N, allsolutions):
    N2   = 2*N
    seq  = [0]*N2
    
    def backtracking(num):
        if num<=0:
            yield "-".join(map(str, seq))
        else:
            for i in range(2*N - num - 1):
                if seq[i] == 0 and seq[i + num + 1] == 0:
                    seq[i] = num; seq[i + num + 1] = num
                    for s in backtracking(num-1):
                        yield s
                    seq[i] = 0; seq[i + num + 1] = 0

    if N%4 not in (0,3):
        yield "no hay solucion"
    else:
        count = 0
        backtracking(3)
        for s in backtracking(N):
            count += 1
            yield "solution %04d -> %s" % (count, s)
            if not allsolutions:
                break

# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3, 4):
        print('\nUsage: %s N [TODAS] [EXACT_COVER] \n' % (sys.argv[0],))
        sys.exit()
    try:
        N = int(sys.argv[1])
    except ValueError:
        print('First argument must be an integer')
        sys.exit()
    allSolutions = False
    langford_function = langford_directo
    for param in sys.argv[2:]:
        if param == 'TODAS':
            allSolutions = True
    for sol in langford_function(N, allSolutions):
        print(sol)