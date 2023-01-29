from ortools.linear_solver import pywraplp
# from ortools.init import pywrapinit

def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return
    #input
    
    global N, distance
    N=int(input())
    distance=[[0]*(N+1)]
    for i in range(N):
        distance.append([0]+[int(j) for j in input().split()])
    #create the varibles x(i,j)
    
    X = [[solver.IntVar(0,1,'X(' + str(i) + ',' + str(j) + ')') if i!=j else solver.IntVar(0,0,'X(' + str(i) + ',' + str(j) + ')')  for j in range(N+1)]for i in range(N+1)]
    
    # constraint: tranverse one direction
    
    for i in range(1,N+1):
        c=solver.Constraint(1,1)
        for j in range(1,N+1):
            c.SetCoefficient(X[i][j],1)
        for j in range(1,N+1):
            c.SetCoefficient(X[j][i],1)
        
    
    #constraint: SEC
    #1 subsetgenerator
    class SubSetGenerator:
        def __init__(self,N):
            self.N=N
            self.x=[0 for i in range(N+1)]
            
        def __CollectSubset__(self):
            S=[]
            for i in range(1, self.N+1):
                if self.x[i]==1:
                    S.append(i)
            return S
        def GenerateFirstSubset(self):
            return self.__CollectSubset__()
        def GenerateNextSubset(self):
            N=self.N
            x=self.x
            i=N
            while i>=1 and x[i]==1:
                i=i-1
            if i==0:
                return None
            x[i]=1
            for j in range(i+1,N+1):
                x[j]=0
            return self.__CollectSubset__()
    SG=SubSetGenerator(N)
    S=SG.GenerateFirstSubset()
    while True:
        S=SG.GenerateNextSubset()
        if S==None:
            break
        if len(S)>=2 and len(S)<N:
            c=solver.Constraint(0,len(S)-1)
            for i in S:
                for j in S:
                    if i!=j:
                        c.SetCoefficient(X[i][j],1)
                        
        
        
    #objective function   
    objective=solver.Objective() 
    for i in range(1,N+1):
        for j in range(1,N+1):
            objective.SetCoefficient(X[i][j],distance[i][j])
            
    objective.SetMinimization()
    solver.Solve()
    print('Objective value =', objective.Value())
if __name__ == '__main__':
    main() 
            
            
     