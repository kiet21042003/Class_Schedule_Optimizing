#11
#6 1 2 9 7 5 3 10 4 11 12
import sys
def Input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    A = [int(x) for x in sys.stdin.readline().split()]
    A.insert(0,0) # use the array from index 1 to index N
    return N,A

N,A = Input()

def swap(i,j):
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp
def heapify(i, N):
    #perform the heapify from index i until index N of the sequence A
    L = 2*i # Index from the left child
    R = 2*i + 1 # Index from the right child
    maxInx = i # MaxIndex will be the index of the maximum elements among the children of A[i]
    if L <= N and A[L] > A[maxInx]:
        maxInx = L
    if R <= N and A[R] > A[maxInx]:
        maxInx = R
    if maxInx != i:
        swap(i, maxInx)
        heapify(maxInx, N)

def BuildHeap():
    for i in range(N//2, 0, -1):
        heapify(i, N)

def HeapSort():
    BuildHeap()
    for i in range(N,1,-1):
        swap(1,i) #swap the biggest element A[1] and the last element of the remaining sequence
        heapify(1, i-1)


HeapSort()
print(*A[1:])