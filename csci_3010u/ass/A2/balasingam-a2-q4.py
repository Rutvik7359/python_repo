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
def simulate_leaf_fall(h, ranges):
    x = 0
    time = 0

    while h > 0:
        # assuming every change in position takes 1 second
        time += 1

        change = random.uniform(0, 1)

        # P(0.1) of moving up
        if change <= ranges[0]:
            h += 1
        # P(0.55) of moving down
        elif change > ranges[0] and change <= ranges[1]:
            h -= 1
        # P(0.15 + P_LEFT_OFFSET) of moving left
        elif change > ranges[1] and change <= ranges[2]:
            x -= 1
        # P(0.15 - P_LEFT_OFFSET) of moving right
        elif change > ranges[2] and change <= ranges[3]:
            x += 1
        # P(0.05) of staying in the same spot

    return time, x
# =============================================================================
# End of Leaf Fall Function====================================================


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
        ranges.append(round(r, 2))

    return ranges

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


    probs = [P_UP, P_DOWN, p_left, p_right]
    ranges = get_prob_range(probs)

    order = "[top, down, left, right]"
    print "Probabilities:"
    print order + ": " + str(probs)
    print "\nRange End:"
    print order + ": " + str(ranges)

    time = []
    disp = []

    # run simulation n times
    for i in range(0, n):
        t, x = simulate_leaf_fall(h, ranges)
        time.append(t)
        disp.append(x)

    print "Time:\t\tmean: " + str(np.mean(time)) + "\tvariance: " + str(np.var(time))
    print "\n\nDisplacement:\tmean: " + str(np.mean(disp)) + "\tvariance: " + str(np.var(disp))

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
    plt.show()
# =============================================================================
# End of Main Function=========================================================

if __name__ == '__main__':
    main()