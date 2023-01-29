def F(n):
    if n <= 1:
        return 1
    if n %2 == 0:
        return 3*F(n-1)+2*F(n-2)
    else:
        return 2*F(n-1) + 3*F(n-2)
print(F(5))