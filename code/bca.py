from ortools.linear_solver import pywraplp
import sys
def input():
	[m,n] = [int(x) for x in sys.stdin.readline().split()]
	P = []
	P.append([])
	for j in range(m):
		p = [int(x) for x in sys.stdin.readline().split()]
		P.append(p)
		p.pop(0)
	C = []
	[K] = [int(x) for x in sys.stdin.readline().split()]
	for k in range(K):
		[i1,i2] = [int(x) for x in sys.stdin.readline().split()]
		C.append([i1,i2])
		
	return n,m,C,P	
	
n,m,C,P = input()
# create solver
solver = pywraplp.Solver.CreateSolver('BCA','CBC')

# create variables
X = [[solver.IntVar(0,1,'X( ' + str(i) + ',' + str(j) + ')') for i in range(n+1)]for j in range(m+1)]
y = [solver.IntVar(0,n,'y(' + str(j) + ')') for j in range(m+1)]
z = solver.IntVar(0,n,'z')

# create constraints
# constraint: each teacher j cannot be assigned to a course i that is NOT in the preference list P[j]
for j in range(1,m+1):
	for i in range(1,n+1):
		if i not in P[j]:
			X[j][i] = solver.IntVar(0,0,'X(' + str(i) + ',' + str(j) + ')')
			print('set X[' + str(i) + ',' + str(j) + ') be zero')

# constraint: each course is assigned to only one teacher
for i in range(1,n+1):
	c = solver.Constraint(1,1)
	for j in range(1,m+1):
		c.SetCoefficient(X[j][i],1)

# constraint: conflict courses
for [i1,i2] in C:
	for j in range(1,m+1):
		c = solver.Constraint(0,1)
		c.SetCoefficient(X[j][i1],1)
		c.SetCoefficient(X[j][i2],1)

# constraint over y[j] and X[j][i]: y[j] = \sum_{i = 0..n-1} X[j][i]		
for j in range(1,m+1):
	c = solver.Constraint(0,0)
	for i in range(1,n+1):
		c.SetCoefficient(X[j][i],1)
	c.SetCoefficient(y[j],-1)	

# constraint between z and y: z >= y[j], forall j = 0,...,m-1	
INF  = solver.infinity()
for j in range(1,m+1):
	c = solver.Constraint(0,INF)
	c.SetCoefficient(z,1)
	c.SetCoefficient(y[j],-1)

# objective
obj = solver.Objective()
obj.SetCoefficient(z,1)

status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL:
	print('cannot find optimal solution')
else:	
	print(solver.Objective().Value())		

for j in range(1,m+1):
	for i in range(1,n+1):
		if X[j][i].solution_value() > 0:
			print('X(' + str(j) + ',' + str(i) + ') = ', X[j][i].solution_value())

for j in range(1,m+1):
	print('courses of teacher ',j, end = ': ')
	for i in range(1,n+1):
		if X[j][i].solution_value() > 0:
			print(i, end = ' ')
			
	print('')		