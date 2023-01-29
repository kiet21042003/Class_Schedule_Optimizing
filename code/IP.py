from ortools.linear_solver import pywraplp
import sys
def Input():
    [m,n] = [int(x) for x in sys.stdin.readline().split()]
    P = []
    for j in range(m):
        p = [int(x) for x in sys.stdin.readline().split()]
        P.append(p)
    C = []
    [K] = [int(x) for x in sys.stdin.readline().split()]
    for k in range(K):
        [i1,i2] = [int(x) for x in sys.stdin.readline().split()]
        C.append([i1,i2])
    return n,m,C,P
n,m,C,P = Input()
solver = pywraplp.Solver_CreateSolver('BCA', 'CBC')

# Create variables
X = [[solver.IntVar(0,1, 'X(' + str(i) + ',' + str(j) + ')') for i in range(n)] for j in range(m)]
y = [solver.IntVar(0,n, 'y(' + str(j) + ')') for j in range(m)]
z = solver.IntVar(0,n,'z')

# Create constraints
for j in range(m):
    for i in range(n):
        if i not in P[j]:
            X[j][i] = solver.IntVar(0,0, 'X(' + str(i) + ',' + str(j) + ')')

# Constraint: each course is assigned to only one teacher 
for i in range(n):
    c = solver.Constraint(1,1)
    for j in range(m):
        c.SetCoefficient(X[j][i] , 1)