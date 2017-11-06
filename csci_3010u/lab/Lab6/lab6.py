import random, sys, os, numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Constants
# =============================================================================
# default number of runs
NUM_RUNS = 10000

# Number probabilities for 1, 2, 3...10
PROBS = [12./100, 13./100, 20./100, 10./100, 6./100, 4./100, 5./100, 9./100, 20./100, 1./100]
# =============================================================================
# End of Constants=============================================================================


# =============================================================================
# Environment Variables
# =============================================================================
in_windows = False
# =============================================================================
# End of Env Vars==============================================================


# =============================================================================
# Sample Number Function
# =============================================================================
def sample_numbers(n, ranges):
    x = 0
    time = 0

    num_list = []
    for i in range(0, n):
        # assuming every change in position takes 1 second
        time += 1

        range_choice = random.uniform(0, 1)

        num = 1
        if range_choice > ranges[9]:
            num = 10
        elif range_choice > ranges[8]:
            num = 9
        elif range_choice > ranges[7]:
            num = 8
        elif range_choice > ranges[6]:
            num = 7
        elif range_choice > ranges[5]:
            num = 6
        elif range_choice > ranges[4]:
            num = 5
        elif range_choice > ranges[3]:
            num = 4
        elif range_choice > ranges[2]:
            num = 3
        elif range_choice > ranges[1]:
            num = 2

        num_list.append(num)
    return num_list

# =============================================================================
# End of Sample Number Function================================================


# =============================================================================
# Helper Functions
# =============================================================================

def get_prob_range(p):
    # setup probability ranges from 0 to 1 in ranges list in the order
    # top, bottom, left right
    ranges = []
    r = 0
    for i in range(0, len(p)):
        r += p[i]
        ranges.append(round(r, 5))

    return ranges

# Clears terminal screen
def clear_screen():
    if in_windows:
        os.system('cls')
    else:
        os.system('clear')


# =============================================================================
# Main Function
# =============================================================================
def main():
    # clear screen and print usage
    global in_windows
    if sys.platform == "win32":
        in_windows = True
    clear_screen()

    n = NUM_RUNS

    # get cmdline args
    num_args = len(sys.argv) - 1

    error = False
    if num_args > 3:
        error = True
        clear_screen()
    else:
        # number of runs input
        if num_args >= 1:
            n = int(sys.argv[1])

            if n <= 0:
                error = True
                clear_screen()
                print "Error: Number of samples must be greater than 0"

    if error:
        sys.exit(0)

    ranges = get_prob_range(PROBS)

    order = list(range(1,11))

    print "Probabilities:"
    print str(order) + ":\n" + str(PROBS)
    print "\nRange End:"
    print str(order) + ":\n" + str(ranges)

    num_list = sample_numbers(n, ranges)

    plt.hist(num_list, 10, normed=True)
    plt.show()
# =============================================================================
# End of Main Function=========================================================

if __name__ == '__main__':
    main()