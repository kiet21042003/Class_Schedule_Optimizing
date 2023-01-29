from ortools.linear_solver import pywraplp
import sys

def input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    d.append([])
    for i in range(N):
        r = [int(x) for x in sys.stdin.readline().split()]
        r.insert(0,0)
        d.append(r)
    return N, d

def CreateVariables(solver):
    X = [[solver.IntVar(0,1,'X' + str(i) + ',' + str(j)+')') for j in range(N+1)] for i in range(N+1)]
    return X
optimal = 0
def TSP_SEC(SECs):
    solver=pywraplp.Solver.CreateSolver('CBC')
    #SECs is the set of sub-tours\
    global X
    global optimal
    X=CreateVariables(solver)
    for i in range(1,N+1):
        c=solver.Constraint(1,1)
        for j in range(1,N+1):
            if i !=j:
                c.SetCoefficient(X[j][i],1)
    c = solver.Constraint(1,1)
    for j in range(1, N+1):
        if j != i:
            c.SetCoefficient(X[i][j], 1)
    
    for S in SECs:
        c = solver.Constraint(0,len(S)-1)
        for i in S:
            for j in S:
                if i !=j:
                    c.SetCoefficient(X[j][i],1)
    
    obj = solver.Objective()
    for i in range(1, N+1):
        for j in range(1, N+1):
            if i != j:
                obj.SetCoefficient(X[i][j], d[i][j])
    
    res_start= solver.Solve()
    if res_start != pywraplp.Solver.OPTIMAL:
        print('Cannot find optimal for sub-problem')
        return None
    else:
        optimal = solver.Objective().Value()
    
    s= [[X[i][j].solution_value() for i in range(N+1)] for j in range (N+1)]
    return s

def findNext(X,current,cand):
    for i in cand:
        if X[current][i]>0:
            return i
    return -1#not found
def getFirst(S):
    for i in S:
        return i

def ExtractSubTour(X):
    S=[]
    #visited=[False for i in range (1,N+1)]
    cand=set()
    for i in range(1,N+1):
        cand.add(i)
    while len(cand)>0:
         current = getFirst(cand)
         T=[]
         T.append(current)
         cand.remove(current)
         while True:
            next=findNext(X,current,cand)
            #if next in T:
            if next==-1:
                break
            T.append(next)
            cand.remove(next)
            current=next
            if len(T)== N:
                return None# golbal tour


         S.append(T)
    if len(S)== 0:
        return None
    return S

def TSP():
    #solver= pywraplp.Solver.CreateSolver('TSP','CBC')
    global SECs
    SECs=[]
    while True:
        solution = TSP_SEC(SECs)
        if solution==None:
            print('Not feasible')
            break
        S=ExtractSubTour(solution)
        print(S)
        if S==None:
            print('found optimal solution')
            break
        for Si in S:
            SECs.append(Si)
    # print(SECs)
N,d=input()
TSP()
print(optimal)
# for i in solution:
#     print(i, end = ' ')