from math import inf
from random import randint
import random

def gen(filename, N, M):
  with open(filename,'w') as f:
    smallest = 50
    largest = 60
    
    # Initialize the number of teacher
    number_teacher = 4

    # Initialize the room's capacity
    room_capacity = [randint(smallest, largest) for _ in range(M)]

    # Initialize data of each class
    info_class = [[0,-1,1e10] for _ in range(N)]

    # Initialize the teacher of each class
    CBG = {}
    teacher = [0 for _ in range(number_teacher)]
    classes = [_ for _ in range(N)]
    while len(classes) != 0:
      i = teacher.index(min(teacher))
      choose = random.choice(classes)
      classes.remove(choose)
      info_class[choose][1] = i + 1
      CBG[choose] = i + 1 
      teacher[i] += 1
    
    # Initialize the number of student in each class
    smallest_class = float("inf")
    for _ in range(N):
      number = randint(smallest - 10, max(room_capacity)-10)
      info_class[_][2] = number
      if number < smallest_class:
        smallest_class = number

    # To make sure that there are no room is left unused.
    if smallest_class > min(room_capacity):
      classes = random.sample([_ for _ in range(N)], N//2)
      while len(classes) != 0:
        temp = classes.pop()
        info_class[temp][2] = randint(smallest - 10, min(room_capacity) + 10)

    # Initialize t(i) for each class
    for i in range(N):
        info_class[i][0] = random.randint(3, 4)
    # Write input created to file .txt 
    f.write(f'{N} {M}\n')
    for t, g, s in info_class:
      f.write(f'{t} {g} {s}\n')
    for _ in room_capacity:
      f.write(f'{_} ') 

if __name__ == "__main__":
  gen("data.txt", 15, 2)