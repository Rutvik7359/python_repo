from util import *


# =============================================================================
# Constants
# =============================================================================
RAND_MAX = 1000000
NUM_VALUES = 10


# =============================================================================
# Radix Sort Functions
# =============================================================================
# Gets an array of single digits at the digit index of each number in the
# provided array
def get_digit_arr(arr, digit_index):
    digitArray = []
    for num in arr:
        digitArray.append((num//10**(digit_index-1))%10)

    return digitArray


# Gets a random array of n numbers between 0(inclusive) and rand_max(exclusive)
def get_rand_arr(n, rand_max):
    randArray = np.random.randint(0, rand_max, n)
    
    return randArray


# Performs counting sort on the array by using its provided single digit array
def count_sort(digitArray, arr):
    digitList = list(digitArray)
    uniqueList = list(set(digitArray))

    # creates an list of occurrences of each number in digitArray
    c0 = []
    for num in uniqueList:
        c0.append(digitList.count(num))

    # creates a list of cumulative occurences based on c0
    c1 = [i for i in np.cumsum(c0)]

    # Inserts arr values based on c1 values used as its indexes
    # Next, decrements c1 at that index to place repeated values in the index
    # before
    b = np.zeros(len(arr), int)
    for i in range(len(digitArray)-1, -1, -1):
        ind = uniqueList.index(digitArray[i])
        b[c1[ind]-1] = arr[i]
        c1[ind] -= 1

    return b[:]


def radix_sort(arr):
    digitArrayMax = -1

    i = 1
    # get array of digits at index i
    digitArray = get_digit_arr(arr, i)
    while digitArrayMax != 0:
        arr = count_sort(digitArray, arr[:])

        i += 1
        digitArray = get_digit_arr(arr, i)
        digitArrayMax = np.amax(digitArray)
    return arr


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print_title("Radix Sort")

    num_values = NUM_VALUES

    usage = "Usage: python part2.py <num_values>(optional)"
    num_args, error = check_args(1, usage)

    if num_args == 1:
        num_values = int(sys.argv[1])
        if num_values < 1:
            print "Error: Number of values must be > 0"
            error = True

    if error:
        sys.exit(0)

    arr = get_rand_arr(num_values, RAND_MAX)
    print "Array before radix_sort:"
    print arr

    arr = radix_sort(arr)
    print "\nArray after radix_sort:"
    print arr
    print ""



