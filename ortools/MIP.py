from ortools.linear_solver import pywraplp
import time

def schedule_classes(n, m, classes, rooms):
    solver = pywraplp.Solver('schedule_classes', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Create variables for each class and each time slot: 
    x = {}
    for i in range(n):
        x[i] = {}
        for j in range(60):
            x[i][j] = solver.IntVar(0, 1, f'class_{i}_slot_{j}')

    # Create variables for each room and each time slot
    y = {}
    for i in range(m):
        y[i] = {}
        for j in range(60):
            y[i][j] = solver.IntVar(0, 1, f'room_{i}_slot_{j}')

    # Constraint 1: Classes taught by the same teacher are assigned to different time slots
    for teacher in range(1, 101):
        for day in range(5):
            for time_slot in range(12):
                indices = [i for i in range(n) if classes[i][1] == teacher]
                solver.Add(sum(x[i][12 * day + time_slot] for i in indices) <= 1)

    # Constraint 2: The number of students in a class is less than or equal to the capacity of the room
    for i in range(n):
        for j in range(60):
            solver.Add(sum(y[k][j] for k in range(m) if rooms[k] >= classes[i][2]) >= x[i][j])

    #Contraint 3: A class can only be scheduled once:
    for i in range(n):
      solver.Add(sum(x[i][j] for j in range(60)) <= classes[i][0])

    #constraint 4: A room can only be assigned to one class:
    for j in range(60):
      solver.Add(sum(y[k][j] for k in range(m)) <=1)
    
    #constraint 5: A class must be scheduled at t[i] constructive period


     # Constraint 3: The class i must be scheduled from period j to period j + t[i]
    for i in range(n):
        for j in range(60):
            if j + classes[i][0] > 60:
                continue
            solver.Add(sum(x[i][k] for k in range(j, j + classes[i][0])) <= classes[i][0])
    # Constraint 4: The number of classes scheduled is maximized
    objective = solver.Objective()
    for i in range(n):
        for j in range(60):
            objective.SetCoefficient(x[i][j], 1)
    objective.SetMaximization()

    solver.Solve()

    # Extract the solution
    result = []
    for i in range(n):
        for j in range(60):
            if x[i][j].solution_value() == 1:
                result.append((i, j, [k for k in range(m) if y[k][j].solution_value() == 1][0]))
                break

    return len(result)

if __name__ == '__main__':
    with open("/content/sample_data/data cua thay.txt", "r") as file:
     n, m = map(int, file.readline().split())
     classes = [list(map(int, file.readline().split())) for _ in range(n)]
     rooms = list(map(int, file.readline().split()))
    t1 = time.time()
    result = schedule_classes(n, m, classes, rooms)
    print('Number of classes have been scheduled: ', result)
    t2 = time.time()
    t = t2 - t1
    print('The running time is: ', t)
