from ortools.linear_solver import pywraplp

solver = pywraplp.CreateSolver('DEMO', 'CBC')
INF = solver.infinity()
x = [solver.NumVar(0,INF,'x + 'str(i)) for i in range(0)]

#x1 = solver.NumVar(0,INF,'x1')
#x2 = solver.NumVar(0,INF,'x2')

c1=solver.Constraint(4,4)
c1.SetCoefficient(x[1],1)
c1.SetCoefficient(x[2],1)
c1.SetCoefficient(x[3],-1)
c1.SetCoefficient(x[4],-1)
c1.SetCoefficient(x[5],1)
c1.SetCoefficient(x[6],0)
c1.SetCoefficient(x[7],0)

c2=solver.Constraint(7,7)
c2.SetCoefficient(x[1],1)
c2.SetCoefficient(x[2],0)
c2.SetCoefficient(x[3],1)
c2.SetCoefficient(x[4],1)
c2.SetCoefficient(x[5],0)
c2.SetCoefficient(x[6],1)
c2.SetCoefficient(x[7],0)