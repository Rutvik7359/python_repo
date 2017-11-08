import random, sys, os, numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Constants
# =============================================================================
# default height and number of runs
HEIGHT   = 100
NUM_RUNS = 1000

# leaf motion default probabilities
P_UP    = 0.1
P_DOWN  = 0.55
P_LEFT  = 0.15
P_RIGHT = 0.15
P_NULL  = 0.05

MOTION = [[1, 0], [-1, 0], [0, -1], [0, 1], [0, 0]]
P_NAMES = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'NOTHING']

# chi-square value to check (4 degrees of freedom at 95% confidence)
X2_CHI = 9.488

TITLE    = 'LEAF IN THE WIND'
ONE_LINE = '-'*55
TWO_LINE = ONE_LINE + '\n' + ONE_LINE
# =============================================================================
# End of Constants=============================================================================


# =============================================================================
# Environment Variables
# =============================================================================
in_windows = False
# =============================================================================
# End of Env Vars==============================================================


# =============================================================================
# Leaf Fall Function
# =============================================================================
def simulate_leaf_fall(h, ranges, probs):
    x = 0
    time = 0
    changes = []
    choices = []

    random.seed(random.random())
    while h > 0:
        # assuming every change in position takes 1 second
        time += 1

        change = random.uniform(0, 1)
        changes.append(change)

        # Goes through each cumulutive probability
        for j in range(0, len(ranges)):
            if change <= ranges[j]:
                choices.append(P_NAMES[j])
                h += MOTION[j][0]
                x += MOTION[j][1]
                break

    return time, x, changes, choices
# =============================================================================
# End of Leaf Fall Function====================================================


# =============================================================================
# Helper Functions
# =============================================================================
# Clears terminal screen
def clear_screen():
    if in_windows:
        os.system('cls')
    else:
        os.system('clear')

# Prints usage
def usage():
    print TITLE
    print TWO_LINE
    print 'Usage:'
    print ONE_LINE
    print 'python *q4* <#_of_runs(optional)>'
    print '            <height(optional)>'
    print '            <left_probability_in[0, 0.3](optional)>'
    print TWO_LINE
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
    usage()

    h = HEIGHT
    n = NUM_RUNS

    # get cmdline args
    num_args = len(sys.argv) - 1

    p_left = P_LEFT
    p_right = P_RIGHT

    error = False
    if num_args > 3:
        error = True
        clear_screen()
        usage()
    else:
        # number of runs input
        if num_args >= 1:
            n = int(sys.argv[1])

            if n <= 0:
                error = True
                clear_screen()
                print "Error: Number of runs must be greater than 0"

        # height input
        if num_args >= 2:
            h = int(sys.argv[2])

            if h <= 0:
                error = True
                clear_screen()
                print "Error: Height must be greater than 0"

        # left movement probability input
        if num_args == 3:
            p_left = round(float(sys.argv[3]), 2)

            if p_left < 0 or p_left > 0.3:
                error = True
                clear_screen()
                print "Error: Left probability must be in [0, 0.3]"

            p_right += round(P_LEFT - p_left, 2)

    if error:
            sys.exit(0)


    probs = [P_UP, P_DOWN, p_left, p_right, P_NULL]
    ranges = [round(p, 2) for p in np.cumsum(probs)]


    print "\nNumber of runs:\t" + str(n)
    print "\nHeight:\t\t" + str(h)
    print "\nProbabilities:"
    print P_NAMES, ": " + str(probs)
    print "Cumulative Probability Range:"
    print P_NAMES, ": " + str(ranges)

    time = []
    disp = []
    changes = [] # stores probabilities generated in simulate_leaf_fall from all runs
    choices = [] # stores movement choices made depending on the random number generator
    # run simulation n times
    for i in range(0, n):
        t, x, change, choice= simulate_leaf_fall(h, ranges, probs)
        time.append(t)
        disp.append(x)
        for j in range(0, h):
            changes.append(change[j])
            choices.append(choice[j])

    print "\nTime:\t\tmean: " + str(np.mean(time)) + "\tvariance: " + str(np.var(time))
    print "\nDisplacement:\tmean: " + str(np.mean(disp)) + "\tvariance: " + str(np.var(disp))

    # calculate chi-sqaure value for the movement choices made
    # includes all choices made through in height*number of runs
    x2 = 0
    for i in range(0, len(probs)):
        ei = probs[i]*n*h
        x2 += ((choices.count(P_NAMES[i]) - ei)**2)/ei

    print "\nThe chi-square value is ", x2
    if x2 < X2_CHI:
        print "Since ", round(x2, 3), " < ", X2_CHI, ", we ACCEPT the null hypothesis"
        print "because there is no statistically significant difference"
        print "between the observed and the expected frequencies."
    else:
        print "Since ", round(x2, 3), " > ", X2_CHI, ", we REJECT the null "
        print "hypothesis."

    # plot histograms for time and displacement
    plt.figure(1)
    plt.hist(time)
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.title('Histogram of Time Leaf Takes to Reach Ground')

    plt.figure(2)
    plt.hist(disp)
    plt.xlabel('Displacement')
    plt.ylabel('Count')
    plt.title('Histogram of Displacement of Leaf When it Reaches the Ground')

    plt.figure(3)
    plt.hist(changes, bins=[0] + ranges)
    plt.xlabel('Cumulative Probabilities')
    plt.ylabel('Count')
    plt.title('Histogram of the Frequency of Movement Choices Made\n(Chi-Square value=' + str(x2) + ')')

    plt.show()
# =============================================================================
# End of Main Function=========================================================

if __name__ == '__main__':
    main()