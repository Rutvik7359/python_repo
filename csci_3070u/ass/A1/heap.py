import numpy as np
import random

def parent(i):
    return (i-1)//2

def l_child(i):
    return 2*i + 1

def r_child(i):
    return 2*i + 2

def max_heapify(A, i, heap_size):
    l = l_child(i)
    r = r_child(i)

    if l < heap_size and A[l] > A[i]:
        largest = l
    else:
        largest = i

    if r < heap_size and A[r] > A[largest]:
        largest = r

    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest,heap_size)
 
def build_max_heap(A):
    heap_size = len(A)
    for i in range(heap_size//2, -1, -1):
        max_heapify(A, i, heap_size)

def heapsort(A):
    build_max_heap(A)
    heap_size = len(A)
    for i in range(heap_size-1, 0, -1):
        A[0], A[i] = A[i], A[0]
        heap_size -= 1
        max_heapify(A, 0, heap_size)

def heap_maximum(A):
    return A[0]

def heap_extract_max(A, heap_size):
    if (heap_size < 1):
        print "heap underflow"
    build_max_heap(A)
    max = A[0]
    A.pop([0])
    max_heapify(A, 0, len(A))

    return max

def heap_increase_key(A, i, key):
    if (key < A[i]):
        print "new key is smaller than current key"
    A[i] = key
    while i > 0 and A[parent(i)] < A[i]:
        A[i], A[parent(i)] = A[parent(i)], A[i]
        i = parent(i)

def max_heap_insert(A, key, heap_size):
    heap_size += 1
    A.append(999)
    heap_increase_key(A, heap_size-1, key)

def print_as_tree(A):
    heap_size = len(A)
    print_as_tree2(A, 0, 0)

def print_as_tree2(A, i, depth):
    r = r_child(i)
    l = l_child(i)
    heap_size = len(A)

    if r < heap_size:
        print_as_tree2(A, r, depth+1)
    else:
        print "\t"*depth + str(A[i])
    
    if l < heap_size:
        if r < heap_size:
            print "\t"*depth + str(A[i])
        print_as_tree2(A, l, depth+1)

if __name__ == "__main__":

    user_input = 0
    while user_input != -1:
        user_input = raw_input("Please enter something: ")

        print "=============="
        if (user_input == 0):
            print "Build Max Heap"
        elif(user_input == 1):
            print "Max Heapify"
        elif(user_input == 2):
            print "Heap Maximum"
        elif(user_input == 3):
            print "Heap Extract Maximum"
        elif(user_input == 4):
            print "Max Heap Insert"
        print "=============="

        A = random.sample(range(1, 100), 10)