from data_gen import gen
import time

def input(filename):
  with open(filename) as f:
    [N, M] = [int(x) for x in f.readline().split()]
    info_classes = [[int(x) for x in f.readline().split()] + [i] for i in range(N)] # [number of lessons, teacher assigned, number of students, class]
    rooms = [int(x) for x in f.readline().split()]
  return info_classes, rooms

def greedy(filename):
  info_classes, rooms = input(filename)
  info_classes_sorted = sorted(info_classes, key=lambda x: -x[2]) # sort classes by its number of students (decreasing)
  rooms_sort = sorted([(rooms[i], i) for i in range(len(rooms))], key = lambda x : x[0]) # sort rooms by its capacity (increasing)
  teacher = [g for t, g, s, _ in info_classes]

  state_room = [[True for _ in range(len(rooms))] for __ in range(60)] # state_room[i][j] = True if room i is available in shift j (0-59)
  state_teacher = [[True for _ in range(len(set(teacher)) + 1)] for __ in range(60)] # state_teacher[i][j] = True if teacher i is available in shift j (0-59)

  timetable = {}
  for info_class in info_classes_sorted:
    timetable[info_class[-1]] = [] # timetable of class each class 
    for _ in range(info_class[0]): # If we loop this way, we will sure that each class has enough shift.
      x = select(info_class, state_room, state_teacher, rooms_sort)
      if x == None:
        continue
      timetable[info_class[-1]].append(x)
  return timetable

def select(info_class, state_room, state_teacher, rooms):
  for p in range(60):
    for capacity, room_index in rooms:
      if feasible(info_class, state_room, state_teacher, capacity, p, room_index):
        state_room[p][room_index] = False
        state_teacher[p][info_class[1]] = False
        return p, room_index

def feasible(info_class, state_room, state_teacher, capacity, p, index_room): # check if a partial solution is feasible
  # At a moment, a teacher teaches at most one class
  if not state_teacher[p][info_class[1]]:
    return False
  # At a moment, a room is used by at most one class
  if not state_room[p][index_room]:
    return False
  # The room's capacity is bigger than the number of student in class
  if info_class[2] > capacity:
    return False
  return True

def print_timetable(timetable):
  classes = sorted(list(timetable.keys()))
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  num_class = 0
  for i in classes:
    if len(timetable[i]) > 0:
      num_class += 1
    for p, r in timetable[i]:
      d = p // 12
      shift = p % 12
      print(f"Class {i+1} has class at shift {shift+1} on {days[d]} in room {r+1}")
    print()
  print("Number of classes that can be scheduled:", num_class)

if __name__ == "__main__":
  filename = 'data.txt'
  #gen(filename, 20, 4)
  t1 = time.time()
  solution = greedy(filename)
  t2 = time.time()
  t = t2 - t1
  print_timetable(solution)
  print("Runtime", t)
