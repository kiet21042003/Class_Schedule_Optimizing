import sys
from ortools.linear_solver import pywraplp
class SubSetGenerator:
    def __init__(self, N):
        self.N=N
        self.x = [0 for i in range(N+1)]

    def __CollectSubset__(self):
        S = []
        for i in range(1, self.N + 1):
            if self.x[i] == 1:
                S.append(i)
        return S

    def GenerateFirstSubset(self):
        return self.__CollectSubset__()

    def GenerateNextSubset(self):
        N = self.N
        x = self.x
        i = N
        while i >= 1 and x[i] == 1:
            i = i-1
        if i == 0:
            return None

        x[i] = 1
        for j in range(i+1, N+1):
            x[j] = 0
        return self.__CollectSubset__()


def input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    d.append([])
    for i in range(N):
        r = [int(x) for x in sys.stdin.readline().split()]
        r.insert(0,0)
        d.append(r)
    return N, d


N, d = input()
# for i in range(1, N+1):
#     for j in range(1, N+1):
#         print(d[j][j], end = '')
#     print('')

solver = pywraplp.Solver.CreateSolver('CBC')
X = [[solver.IntVar(0,1,'X' + str(i) + ',' + str(j)+')') for j in range(N+1)] for i in range(N+1)]

#flow balance constraint
for i in range(1, N+1):
    c = solver.Constraint(1,1)
    for j in range(1, N+1):
        if i != j:
            c.SetCoefficient(X[j][i], 1)
    c = solver.Constraint(1,1)
    for j in range(1, N+1):
        if j != i:
            c.SetCoefficient(X[i][j], 1)

#state SEC (Sub-Tour Elimination Constraint)
SG = SubSetGenerator(N)
S = SG.GenerateFirstSubset()
while True:
    if len(S)>= 2 and len(S) < N:
        c = solver.Constraint(0, len(S) - 1)
        for i in S:
            for j in S:
                if i != j:
                    c.SetCoefficient(X[i][j], 1)
    S = SG.GenerateNextSubset()
    if S == None:
        break
def findnext(current):
    for i in range(1, N+1):
        if X[current][i].solution_value() > 0:
            return i
    return -1 # not found
def extractSolutionRoute():
    route = []
    current = 1
    route.append(1)
    for i in range(2, N+1):
        nextPoint = findnext(current)
        route.append(nextPoint)
        current = nextPoint
    return route
#objective function
objective = solver.Objective()
for i in range(1, N+1):
    for j in range(1, N+1):
        if i != j:
            objective.SetCoefficient(X[i][j], d[i][j])

#solver.SetMinimization()
result_status = solver.Solve()
# if result_status != pywraplp.Solver.OPTIMAL:
#     print('cannot find optimal solution')
# else:
#     print('optimal objective value = ', solver.Objective().Value())

# for i in range(1, N+1):
#     for j in range(1, N+1):
#         if X[i][j].solution_value()>0:
#             print('(',i,',',j,')')
route = extractSolutionRoute()
print(N)
for i in route:
    print(i, end = ' ')