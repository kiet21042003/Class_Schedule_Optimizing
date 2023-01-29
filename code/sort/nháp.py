import sys
def input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    A = [int(x) for x in sys.stdin.readline().split()]
    A.insert(0,0)
    return N,A

def swap(i,j):
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp

def heapify(i,N):
    L = 2*i
    R = 2*i+1
    maxInd = i
    if L<=N and A[L]>A[maxInd]:
        maxInd = L
    if R<=N and A[R]>A[maxInd]:
        maxInd = R
    if maxInd != i:
        swap(i,maxInd)
        heapify(maxInd,N)

def BuildHeap():
    for i in range(N//2,0,-1):
        heapify(i,N)

def HeapSort():
    BuildHeap()
    for i in range(N,1,-1):
        swap(1,i) # Swap the biggest element A[1] and the last element of the remaining sequence
        heapify(1,i-1)

def Merge(L,M,R):
    i = L
    j = M+1
    for k in range(L,R+1):
        if i>M:
            TA[k] = A[j]
            j+=1
        elif j>R:
            TA[k] = A[i]
            i+=1
        else:
            if A[i]<A[j]:
                TA[k] = A[i]
                i+=1
            else:
                TA[k] = A[j]
                j+=1
    for k in range(L,R+1):
        A[k] = TA[k]

def MergeSort(L,R):
    if L>=R:
        return
    M = (L+R)//2
    MergeSort(L,M)
    MergeSort(M+1,R)
    Merge(L,M,R)

N,A = input()
TA = [0 for i in range(N+1)]
# HeapSort()
MergeSort(1,10)
print(*A[1:])
'''
11
6 1 2 9 7 5 3 10 4 11 12
'''