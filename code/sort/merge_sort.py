#11
#6 1 2 9 7 5 3 10 4 11 12
import sys
def Input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    A = [int(x) for x in sys.stdin.readline().split()]
    A.insert(0,0) # use the array from index 1 to index N
    return N,A


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

def Merge(L, M, R):
    # merge to sorted list: A[L, ..., M] and A[M+1, ..., R] in to a unique sort list A[L, ..., R]
    i = L # index runs on the left sub-sequence A[L, ... , M]
    j = M+1 # index runs on the right sub-sequence A[M+1, ... , R]
    for k in range(L, R+1):
        if i > M: # i is out of the left sub-sequence
            TA[k] = A[j]
            j +=1
        elif j > R: # j is out of the right sub-sequence
            TA[k] = A[i]
            j +=1
        else:
            if A[i] < A[j]:
                TA[k] = A[i]
                i+= 1
            else:
                TA[k] = A[j]
                j+= 1
    for k in range(L, R+1):
        A[k] = TA[k]
        
def MergeSort(L, R): #sort the subsequence A[L, ..., R], merge sort is based on divide and conquer
    if L >= R:
        return
    M = (L+R)//2 #index of the element in the middle
    MergeSort(L, M)
    MergeSort(M+1,R)
    Merge(L,M,R)

N,A = Input()
TA= [0 for i in range(N+1)]
MergeSort(1, N)
# HeapSort()
print(*A[1:])