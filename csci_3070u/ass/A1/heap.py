import numpy as np
import random
from sys import platform
import os

# Env variables
WIN = False
DASH_SIZE = 40

# =============================================================================
# Heap
# =============================================================================
# Get parent index of i
def parent(i):
    return (i-1)//2

# Get left child index of i
def l_child(i):
    return 2*i + 1

# Get right child index of i
def r_child(i):
    return 2*i + 2

# Fixes a heap with 1 violation
def max_heapify(A, i):
    heap_size = len(A)
    p = parent(i)
    l = l_child(i)
    r = r_child(i)

    if i > 0 and A[i] > A[p]:
        A[i], A[p] = A[p], A[i]
        max_heapify(A, p)

    if l < heap_size and A[l] > A[i]:
        largest = l
    else:
        largest = i

    if r < heap_size and A[r] > A[largest]:
        largest = r

    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest)
 
 # Builds a max heap from an arbitary array
def build_max_heap(A):
    heap_size = len(A)
    for i in range(heap_size//2, -1, -1):
        max_heapify(A, i)

# Uses a heap to sort an array
def heapsort(A):
    build_max_heap(A)
    heap_size = len(A)
    for i in range(heap_size-1, 0, -1):
        A[0], A[i] = A[i], A[0]
        max_heapify(A, 0)

# Returns the top element of a max heap
def heap_maximum(A):
    return A[0]

# Removes the top element of a max heap and returns it
def heap_extract_max(A):
    if (len(A) < 1):
        print "heap underflow"
    max = A[0]
    A.pop(0)
    build_max_heap(A)

    return max

def max_heap_insert(A, key):
    A.append(key)
    build_max_heap(A)


# =============================================================================
# Printing
# =============================================================================
# Print out the array form and tree form of two given arrays
def print_all(A, B):
    print "Before:"
    print str(A) + "\n"
    print_as_tree(A)
    print "\n"

    print "After:"
    print str(B) + "\n"
    print_as_tree(B)
    print "\n"

# Print the tree form of an array
def print_as_tree(A):
    heap_size = len(A)
    print_tree(A, 0, 0)

# Helper function of print_as_tree(A) to print tree form recursively
def print_tree(A, i, depth):
    r = r_child(i)
    l = l_child(i)
    heap_size = len(A)

    if r < heap_size:
        print_tree(A, r, depth+1)
    else:
        print "\t"*depth + str(A[i])
    
    if l < heap_size:
        if r < heap_size:
            print "\t"*depth + str(A[i])
        print_tree(A, l, depth+1)

# =============================================================================
# Other Functions
# =============================================================================
def clear_screen():
    if WIN:
        os.system('cls')
    else:
        os.system('clear')


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":

    if platform == "win32":
        WIN = True
    clear_screen()

    user_input = 0
    while user_input != -1:

        print "="*DASH_SIZE
        print "HEAP MENU"
        print "="*DASH_SIZE
        print " 0: Build Max Heap"
        print " 1: Max Heapify"
        print " 2: Heap Maximum"
        print " 3: Heap Extract Maximum"
        print " 4: Max Heap Insert"
        print "-1: Exit\n"


        user_input = int(raw_input("Type an integer corresponding to menu items below: "))
        clear_screen()
            
        # creates a random array of 10 integers between 1 and 99, inclusive
        A = random.sample(range(1, 100), 10)
        B = A[:]
                
        output = ""
        print "="*DASH_SIZE
        if(user_input == 1):
            print "Max Heapify"
            print "="*DASH_SIZE

            i = len(B)-1
            A = [99, 44, 79, 24, 32, 21, 36, 17, 1, 49]
            B = A[:]
            max_heapify(B, i)
            output = "Value, " + str(A[i]) + ", heapified to correct spot"

        # Builds max heap (and outputs the top element or extracts it out)
        else:
            build_max_heap(B)
            if (user_input == 0):
                print "Build Max Heap"
                print "="*DASH_SIZE
            
            # Gets the the top element in a max heap
            elif (user_input == 2):
                print "Heap Maximum"
                print "="*DASH_SIZE

                print B
                print_as_tree(B)
                output = "\n\nThe heap max value is " + str(heap_maximum(B))

            # Removes the top element of a max heap
            elif(user_input == 3):
                print "Heap Extract Maximum"
                print "="*DASH_SIZE

                output = "Maximum value, " + str(heap_extract_max(B)) + ", extracted"
            
            # Inserts a value into max heap
            else:
                clear_screen()
                user_input = int(raw_input("Please enter an integer to insert in the heap: "))
                clear_screen()

                print "="*DASH_SIZE
                print "Max Heap Insert"
                print "="*DASH_SIZE

                max_heap_insert(B, user_input)

        # Prints out before and after of heap
        if user_input != 2:
            print_all(A, B)

        if output != "":
            print output + "\n" 