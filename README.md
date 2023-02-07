# mini_project_opti
There are N classes 1, 2, …, N that need to be scheduled. 

Each class i have: t[i] is the number of lessons, g[i] is the teacher teaching class i and s[i] is the number of students of class i.

There are M rooms 1, 2, …, M and c[i] is the number of seats in the room i.

In a week, there are 5 days (from Monday to Friday), each day is divided into 12 shifts (6 morning shifts and 6 afternoon shifts).

Create a schedule (assign day, shift and room to each class) that satisfies:
a. Two class having the same teacher need to be scheduled separately.
b. The number of students in each class has to be smaller than the capacity of the room.
c. The numbers of classes scheduled is maximized
Input:
+ The first line: N and M.
+ The next N line, each line write: t(i), g(i) and s(i).
+ The next line: c(1), c(2), …, c(n).

Output: Timetable

