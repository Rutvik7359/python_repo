import random, sys, os, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

# =============================================================================
# Constants
# =============================================================================
# default number of runs
NUM_RUNS = 10000
X2_CHI = 16.92
# Number probabilities for 1, 2, 3...10
PROBS = [12./100., 13./100., 20./100., 10./100., 6./100., 4./100., 5./100., 9./100., 20./100., 1./100.]
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
    num_list = []
    rand_list = []

    random.seed(random.random())
    for i in range(0, n):
        range_choice = random.uniform(0, 1)
        rand_list.append(range_choice)

        num = 10
        # Goes through each cumulutive probability except the last one which is
        # set as the default in the line above
        for j in range(0, len(ranges)-1):
            if range_choice < ranges[j]:
                num = j+1
                break

        num_list.append(num)

    return num_list, rand_list
# =============================================================================
# End of Sample Number Function================================================


# =============================================================================
# Helper Functions
# =============================================================================
# Clears terminal screen
def clear_screen():
    if in_windows:
        os.system('cls')
    else:
        os.system('clear')
# =============================================================================
# End of Helper Functions======================================================


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

    # get get cumulative probability range from probabilites
    ranges = [round(p, 2) for p in np.cumsum(PROBS)]
    order = list(range(1,11))

    # printing out probabilites and probability range
    print "Probabilities:"
    print str(order) + ":\n" + str(PROBS)
    print "\nCummulative Probability Range:"
    print str(order) + ":\n" + str(ranges)

    # getting the sample numbers
    num_list, rand_list = sample_numbers(n, ranges)

    # Calculating chi-square value and comparing to x^2(0.05) at 9 degrees of
    # freedom
    x = 0
    for i in range(0, len(PROBS)):
        ei = PROBS[i]*n
        x += ((num_list.count(i+1) - ei)**2)/ei


    print "\nThe chi-square value is ", x
    if x < X2_CHI:
        print "Since ", round(x, 3), " < ", X2_CHI, ", we ACCEPT the null "
        print "hypothesis because there is no statistically significant "
        print "difference between the observed and the expected frequencies."
    else:
        print "Since ", round(x, 3), " > ", X2_CHI, ", we REJECT the null "
        print "hypothesis."

    plt.hist(rand_list, bins=[0] + ranges)
    plt.xlabel('Cumulative Probabilities per Number')
    plt.ylabel('Count')
    plt.show()
# =============================================================================
# End of Main Function=========================================================

if __name__ == '__main__':
    main()