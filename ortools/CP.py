from ortools.sat.python import cp_model
import time

'''
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
	# print intermediate solution
	def __init__(self,vars, N, M, c, s, g, limit = 1):
		cp_model.CpSolverSolutionCallback.__init__(self) 
		self.__vars = vars 
		self.__solution_count = 0
		self.__N = N
		self.__M = M
		self.__c = c
		self.__s = s
		self.__g = g
		self.__limit = limit
	def on_solution_callback(self):
		self.__solution_count += 1
		print(f'\nSolution {self.__solution_count}:')
		for n in range(self.__N):
			for i in range(5):
				for j in range(12):
					for m in range(self.__M):
						if self.Value(self.__vars[n][i][j][m]):
							print(f'\tClass {n} has lesson in shift {j} of day {i} at room {m} having {self.__c[m]} slots, has {self.__s[n]} students and is taught by teacher {self.__g[n]}')
		
		if self.__solution_count >= self.__limit:
			self.StopSearch()
	def solution_count(self):
		return self.__solution_count
'''

def Time(d):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return days[d]

def input(filename):
    t = []
    g = []
    s = []
    with open(filename) as f:
        [N, M] = [int(x) for x in f.readline().split()]
        for _ in range(N):
            l = [int(x) for x in f.readline().split()]
            t.append(l[0])
            g.append(l[1])
            s.append(l[2])
        c = [int(x) for x in f.readline().split()]
    return N, M, t, g, s, c

def CP(filename):
    N, M, t, g, s, c = input(filename)
    model = cp_model.CpModel()
    G0 = set(g)
    G = {}
    for i in G0:
        G[i] = [j for j in range(N) if g[j] == i]

    # Create variables
    x={}
    for i in range(N):
        for d in range(5):
            for k in range(12):
                for r in range(M):
                    x[i,d,k,r] = model.NewIntVar(0, 1, f'x[{i},{d},{k},{r}]')
    y = [model.NewIntVar(0, 1, f'y[{i}]') for i in range(N)]

    # Constraints
    ## Two classes having the same teacher need to be scheduled separately
    for p in G:
        for d in range(5):
            for k in range(12):
                model.AddLinearConstraint(\
                    sum(x[i,d,k,r] \
                        for i in G[p] for r in range(M)), 0, 1)
    
    ## If a class studies in 1 room, number of students <= room capacity
    for i in range(N):
        for d in range(5):
            for k in range(12):
                for r in range(M):
                    model.Add(s[i] * x[i,d,k,r] <= c[r])
                    
    ## The total number of times that class i is scheduled in the timetable must be less than the number of lessons for class i (t[i]). 
    ## This ensures that the class is not scheduled more times than it should be
    '''for i in range(N):
        model.Add(sum(x[i,d,k,r] \
             for d in range(5) for k in range(12) for r in range(M)) <= t[i])'''

    ## There can be only be one class at one room in a moment
    for d in range(5):
        for k in range(12):
             for r in range(M):
                model.Add(sum(x[i,d,k,r] \
                    for i in range(N)) <= 1)
    
    ## Value for y 
    for i in range(N):
        c = model.NewBoolVar('c')
        model.Add(y[i] == 1).OnlyEnforceIf(c)
        model.Add(y[i] == 0).OnlyEnforceIf(c.Not())
        model.Add(sum(x[i,d,k,r] for d in range(5) for k in range(12) for r in range(M)) == t[i]).OnlyEnforceIf(c)
        model.Add(sum(x[i,d,k,r] for d in range(5) for k in range(12) for r in range(M)) <= t[i]).OnlyEnforceIf(c.Not())

    '''Total_Shifts = {}
    for i in range(N):
        for d in range(5):
            Total_Shifts[i, d] = model.NewIntVar(0, t[i], f'Total_Shifts[{i}, {d}]')

    Most_Shifts_Day = {}
    for i in range(N):
        Most_Shifts_Day[i] = model.NewIntVar(0, t[i], f'Most_Shifts_Day[{i}]')
        model.AddMaxEquality(Most_Shifts_Day[i], [Total_Shifts[i, d] for d in range(5)])

    Least_Shifts_Day = {}
    for i in range(N):
        Least_Shifts_Day[i] = model.NewIntVar(0, t[i], f'Least_Shifts_Day[{i}]')
        model.AddMinEquality(Least_Shifts_Day[i], [Total_Shifts[i, d] for d in range(5)])'''
    
    # Objective function

    model.Maximize(sum(y[i] for i in range(N)))

    # Create solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print("Solution: ")
        for i in range(N):
            for d in range(5):
                for k in range(12):
                    for r in range(M):
                        if solver.Value(x[i,d,k,r]):
                        #if result[i][d][k][r]:
                            print(f'Class {i+1} has lesson in {Time(d)} shift {k+1} in room {r+1}')
            print()       
        print(f'Number of class that can be scheduled: {int(solver.ObjectiveValue())}')
    else:
        print("No solution")

if __name__ == '__main__':
    from data_gen import *
    filename = "data.txt"
   #gen(filename, 100, 50)
    t1 = time.time()
    CP(filename)
    t2 = time.time()
    t = t2 - t1
    print(t)
