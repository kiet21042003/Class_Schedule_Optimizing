from ortools.linear_solver import pywraplp

def Time(d):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return days[d]

def solve_timetabling(n,m,t,g,s,rooms):
    solver = pywraplp.Solver('schedule_classes', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    inf=solver.infinity()

    # binary variables indicating if class i is assigned to room r at day d, period p
    x = {}
    for i in range(n):
        for r in range(m):
            for d in range(5):
              for p in range(12):
                x[i,r,d,p] = solver.IntVar(0, 1, 'x[%d,%d,%d,%d]' % (i, r, d, p))
    
    y={}
    for i in range(n):
      y[i]=solver.IntVar(0,1,'y[%d]' % (i))
    
    #constraint 1: a teacher can only teach one class at a moment
    teachers={}
    G=set(g)

    for i in G: 
      teachers[i]=[j for j in range(n) if g[j]==i]

    for teacher in teachers:
      for d in range(5):
        for p in range(12):
          c=solver.Constraint(0,1) 
          for r in range(m):
            for i in teachers[teacher]:
              c.SetCoefficient(x[i,r,d,p],1)
    
    #constraint 2:The number of students is less than the room's capacity
    for i in range(n):
      for r in range(m):
       if s[i] > rooms[r]:
        for d in range(5):
         for p in range(12):
           cstr = solver.Constraint(0, 0)
           cstr.SetCoefficient(x[i,r,d,p], 1)

    #constraint 3: There can be only one class at one room
    for r in range(m):
      for d in range(5):
        for p in range(12):
          cstr=solver.Constraint(0,1)
          for i in range(n):
            cstr.SetCoefficient(x[i,r,d,p],1)
    
    #value for y 
    for i in range(n):
     c = solver.Constraint(t[i], t[i])
    for r in range(m):
        for d in range(5):
            for p in range(12):
                c.SetCoefficient(x[i, r, d, p], 1)
    c.SetCoefficient(y[i], -t[i])

    # create variables for total shifts for each class and day
    Total_Shifts = {}
    for i in range(n):
        for d in range(5):
            Total_Shifts[i, d] = solver.IntVar(0, t[i], f'Total_Shifts[{i}, {d}]')

    ## create variables for most shifts per day for each class
    Most_Shifts_Day = {}
    for i in range(n):
       Most_Shifts_Day[i]=solver.IntVar(0,t[i],f'Most_Shifts_Day[{i}]')
    
    # create constraint to ensure that Most_Shifts_Day[i]
    # is the maximum value of Total_Shifts[i,d] for d in range(5)
    for i in range(n):
      max_cstr=solver.Constraint(0,t[i])
      for d in range(5):
        max_cstr.SetCoefficient(Total_Shifts[i,d],1)
      max_cstr.SetCoefficient(Most_Shifts_Day[i],-1)
   
   #create variables for least shifts per day for each class
    Least_Shifts_Day = {}
    for i in range(n):
      Least_Shifts_Day[i]=solver.IntVar(0,t[i],f'Least_Shifts_Day[{i}]')
  
	  # create constraint to ensure that Least_Shifts_Day[i] is the minimum value of Total_Shifts[i,d] for d in range(5)
    for i in range(n):
      min_cstr = solver.Constraint(0, t[i])
      for d in range(5):
        min_cstr.SetCoefficient(Total_Shifts[i, d], 1)
      min_cstr.SetCoefficient(Least_Shifts_Day[i], -1)
      solver.Add(Least_Shifts_Day[i] >= 1)

    #objective function:
    objective = solver.Objective()
    for i in range(n):
     objective.SetCoefficient(y[i], 1)
     objective.SetCoefficient(Most_Shifts_Day[i], -1)
     objective.SetCoefficient(Least_Shifts_Day[i], 1)
    objective.SetMaximization()
    solver.Solve()

    #print the solution:
    for i in range(n):
        for r in range(m):
            for d in range(5):
                for p in range(12):
                    if x[i,r,d,p].solution_value() == 1:
                        day=Time(d)
                        print(f'Class {i} is assigned to room {r} on day {day} at period {p}')
    count=0
    for i in range(n):
        if y[i].solution_value() == 1:
            count+=1
    print(f"Number of classes scheduled: {count}")
    print(objective.Value())
 
if __name__ == '__main__':
    n, m = map(int, input().split())
    classes = [list(map(int, input().split())) for _ in range(n)]
    rooms = list(map(int, input().split()))
    t=[classes[i][0] for i in range(n)]
    g=[classes[i][1] for i in range(n)]
    s=[classes[i][2] for i in range(n)]
    solve_timetabling(n,m,t,g,s,rooms)

