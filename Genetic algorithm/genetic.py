import numpy as np
import random
import copy
import time
'''# Define the number of classes and rooms
N = 10
M = 4

# Define the number of lessons, teachers, and students for each class
t = [random.randint(5, 10) for _ in range(N)]
g = [random.randint(3, 5) for _ in range(N)]
s = [random.randint(30, 40) for _ in range(N)]

# Define the number of seats in each room
c = [random.randint(40, 60) for _ in range(M)]'''

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
# Define the number of days and shifts in a week
days = 5
shifts = 12

# Define the genetic algorithm parameters
population_size = 8 #population_size is the number of individuals that make up one generation
generations =8 #generations is the number of times the genetic algorithm goes through the process of creating a new generation.
crossover_rate=0.8
mutation_rate=0.11

def find_max_number(N,days,shifts,M):
    maximum_lesson=min(60*(max(g)+1),60*M)
    while sum(t)>maximum_lesson:
        max_lesson=max(t)
        max_index=t.index(max_lesson)
        t.pop(max_index)
        g.pop(max_index)
        s.pop(max_index)
        N-=1
        maximum_lesson=min(60*len(g),60*M)
    return N
# Define the initial population
#population = [np.random.randint(0, M, size=(N, 3)) for _ in range(population_size)]
'''Each individual in the population is represented by a 2D array of size Nx3, where N is the number of classes and 
3 is the number of columns. Each element in the array represents a class, and the three columns in each element
represent the room, the day, and the shift in which the class will take place.'''

'''So now we get the population that has 50 individuals'''
# Define the fitness function

def fitness(individual):
    global s, c, t, g
    # Initialize the fitness value
    fit = 0
    # Check if the number of students is greater than the capacity of the room
    
    # Check if the teacher has classes at the same time
    for i in range(len(individual)-1):
        for j in range(i + 1, len(individual)):
            for q in range(t[i]):
                for k in range(t[j]):
                    if (individual[i][q][0] == individual[j][k][0]
                        and individual[i][q][1] == individual[j][k][1]):
                        if g[i]==g[j]:
                            fit -= 1
                        if individual[i][q][2] == individual[j][k][2]:
                            fit -= 1
        for s1 in range(t[i]-1):
            for s2 in range(s1+1,t[i]):
                if individual[i][s1][0]==individual[i][s2][0] and individual[i][s1][1]==individual[i][s2][1]:
                    fit-=1

    # Check if the room is occupied at the same time
    for i in range(len(individual)):
        for j in range(t[i]):
            day, shift, room = individual[i][j]
            if s[i]>c[room]:
                fit-=1    
                # Check if the number of students is greater than the capacity of the room
    return fit

def fitness_class(individual):
    scheduled_classes = 0
    for i in range(N): #for each class
        class_scheduled = True
        for j in range(t[i]): #for each lesson
            day,shift,room = individual[i][j]
            if c[room] < s[i]:
                class_scheduled = False
                break
        if class_scheduled:
            scheduled_classes += 1
    return scheduled_classes



def create_individual(N, days, shifts, M):
    #an individual is a schedule, individual[i] is timetable for class[i]
    #individual[i] has t[i] elements, each element individual[i][0] is [day,shift,room] for lesson q.
    individual=[]
    has_been_assigned=set()
    
    for i in range(N): #set lessons for class[i]:
        class_lesson=[]
        for j in range(t[i]): #for j in range number of lessons:
            day,shift,room=random.randint(0,days-1),random.randint(0,shifts-1),random.randint(0,M-1)
            while (day,shift,room) in has_been_assigned:
                day,shift,room=random.randint(0,days-1),random.randint(0,shifts-1),random.randint(0,M-1)
            has_been_assigned.add((day,shift,room))   

                
            class_lesson.append([day,shift,room]) 
            #this function means that the lesson j will take on (day,shift,room)
        individual.append(class_lesson)    
    
    return individual
    

    #create individual is a single solution to the scheduling problem.
    #Each individual is represented as an array of size Nx3.
    #Each element represents the day, the shift and the class to be placed.


def select_parents(population, fitnesses, num_parents):
    #population:list of individuals in the population
    #fitnesses: a list of fitness value of each individual in the population
    #num_parents: an integer representing the number of parents to select from the population
    parents = []
    for i in range(num_parents):
        max_fitness = max(fitnesses) #max_fitness is the element that has largest fitness value
        max_index = fitnesses.index(max_fitness) #return the index of max_fitness in the fitnesses array.
        parents.append(population[max_index]) #parents append the population of index max_index
        fitnesses[max_index] = -99999
    return parents

def crossover(parent1, parent2):
    """This function performs crossover on two parents to create a child"""
    child = []
    for i in range(N):
        if np.random.rand() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child
def mutation(offspring):
    global has_been_assigned
    for i in range(len(offspring)):
        for j in range(t[i]):
            if random.uniform(0, 1) < mutation_rate:
                day = random.randint(0, days-1)
                shift = random.randint(0, shifts-1)
                room = random.randint(0, M-1)
                '''while (day,shift,room) in has_been_assigned:
                    day = random.randint(0, days-1)
                    shift = random.randint(0, shifts-1)
                    room = random.randint(0, M-1)'''
                offspring[i][j] = [day, shift, room]
    return offspring

def genetic_algorithm(N, days, shifts, M):
    population = [create_individual(N, days, shifts, M) for i in range(population_size)]
    for generation in range(generations):
        # Evaluate the fitness of each individual
        fitness_values = [fitness(individual) for individual in population]
        # Select the parents for crossover
        parents = select_parents(population, fitness_values, 8)
        # Create the next generation
        population = create_next_generation(parents)
    # Select the best individual
    best_individual = population[np.argmax(fitness_values)]
    return best_individual


def create_next_generation(parents):
    """This function creates the next generation of individuals"""
    next_population = []
    for i in range(population_size):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = crossover(parent1, parent2)
        child = mutation(child)
        next_population.append(child)
    return next_population
def print_schedule(schedule):
    #print the header row:
    print('Lesson\tDay\tShift\troom\tTeacher\tStudent\tCapacity')
    print("------\t---\t-----\t----\t-------\t-------\t--------")
    for i in range(N):
        print('Class'+str(i+1)+':')
        for j in range(t[i]):
            print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(j+1,schedule[i][j][0]+1,schedule[i][j][1]+1,schedule[i][j][2]+1
            ,g[i],s[i],c[schedule[i][j][2]]))
        print('-------------------------------------------------------------')

                
if __name__=='__main__':
    file_name='data.txt'
    N,M,t,g,s,c=input(file_name)
    N=find_max_number(N,days,shifts,M)
    
    
    schedule=genetic_algorithm(N,days,shifts,M)
    
    
    
    import random
    
    def refine_schedule(schedule):
        schedule_info = [[[0 for room in range(M)] for shift in range(shifts)] for day in range(days)]
        teacher_info=[[[0 for teacher in range(len(t))] for shift in range(shifts)] for day in range(days)]
        for i in range(len(schedule)):
            for j in range(t[i]):
                room = -1
                for day in range(days-1, -1, -1):
                    for shift in range(shifts-1, -1, -1):
                        for k in range(M):
                            if c[k] >= s[i] and schedule_info[day][shift][k] == 0 and teacher_info[day][shift][g[i]-1] == 0:
                                room = k
                                break
                        if room != -1:
                            break
                    if room != -1:
                        break
                if room == -1:
                    break
                schedule[i][j] = day, shift, room
                schedule_info[day][shift][room] = 1
                teacher_info[day][shift][g[i]-1]=1

        while True:
            schedule_changed = False
            for i in range(len(schedule)):
                for j in range(t[i] - 1):
                    for k in range(j + 1, t[i]):
                        if schedule[i][j][0] == schedule[i][k][0] and schedule[i][j][1] == schedule[i][k][1]:
                            day, shift, room = schedule[i][k]
                            for new_day in range(days):
                                for new_shift in range(shifts):
                                    if (new_day, new_shift) != (day, shift) and schedule_info[new_day][new_shift][room] == 0 and teacher_info[new_day][new_shift][g[i] - 1] == 0:
                                        schedule[i][j] = new_day, new_shift, room
                                        schedule_info[new_day][new_shift][room] = 1
                                        teacher_info[new_day][new_shift][g[i] - 1] = 1
                                        schedule_changed = True
                                        break
                                if schedule[i][j] != (day, shift, room):
                                    break
            for i in range(len(schedule) - 1):
                for j in range(i + 1, len(schedule)):
                    if g[i] == g[j]:
                        for q in range(t[i]):
                            for k in range(t[j]):
                                if schedule[i][q][0] == schedule[j][k][0] and schedule[i][q][1] == schedule[j][k][1]:
                                    day, shift, room = schedule[j][k]
                                    for new_day in range(days):
                                        for new_shift in range(shifts):
                                            if (new_day, new_shift) != (day, shift) and schedule_info[new_day][new_shift][room] == 0 and teacher_info[new_day][new_shift][g[i] - 1] == 0:
                                                schedule[i][q] = new_day, new_shift, room
                                                schedule_info[new_day][new_shift][room] = 1
                                                teacher_info[new_day][new_shift][g[i] - 1] = 1
                                                schedule_changed = True
                                                break
                                        if schedule[i][q] != (day, shift, room):
                                            break
            if not schedule_changed:
                break

        #Check the last time:
        
        return schedule




    t1=time.time()
    final_schedule=refine_schedule(schedule)
    while fitness(final_schedule)<0:
        max_lesson=max(t)
        max_index=t.index(max_lesson)
        t.pop(max_index)
        g.pop(max_index)
        s.pop(max_index)
        N-=1
        schedule=genetic_algorithm(N,days,shifts,M)
        final_schedule=refine_schedule(schedule)
    t2=time.time()
    thoigian=t2-t1
   
    table = [[[] for j in range(shifts)] for i in range(days)]

    for i in range(N):
        for j in range(t[i]):
            day, shift, room = final_schedule[i][j]
            table[day-1][shift-1].append((room, g[i], i+1))
    def print_table(table):
    # Print the header
        header = "|Day/Shift"
        for i in range(1, 13):
            header += "|  {:^6d}  ".format(i)
        header += "|"
        print(header)
        print("+" + "-"*160)
        for i in range(0, 5):
            line = "|   {:^4d}   ".format(i+1)
            for j in range(0, 12):
                if len(table[i][j]) > 0:
                    line += "|"
                    for tup in table[i][j]:
                        line += "({:^1d},{:^1d},{:^1d})".format(tup[0]+1, tup[1], tup[2])

                        line += ","
                    line = line[:-1]
                else:
                    line += "|          "
            line += "|"
            print(line)
            print("+" + "-"*160)


    print_table(table)
    
    print_schedule(final_schedule)
    print('Number of conflict: ',fitness(final_schedule))
    print(thoigian)
    with open('genetic_test.txt', 'a') as f:
        f.write(str(thoigian) + " ")
    print('Maximum number of classes:',fitness_class(final_schedule))














































