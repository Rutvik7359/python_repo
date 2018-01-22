from util import *

# =============================================================================
# Constants
# =============================================================================
FILE = "retail.txt"
THRESHOLD = 5


# gets character frequency from given ascii text file
def get_char_freq(file):
    d = dict()
    with open(file) as f:
        for line in f:

            tempData = line.split()
            for t in tempData:
                if t in d:
                    d[t] += 1
                else:
                    d[t] = 1
    return d


if __name__ == "__main__":


    clear_screen()
    usage = "Usage: python lab1.py <threshold>(optional)"
    num_args, error = check_args(1, usage)

    if error:
        sys.exit(0)

    thresh = THRESHOLD
    if num_args == 1:
        thresh = int(sys.argv[1])

    countDict = sorted(get_char_freq(FILE).iteritems(), key=lambda (k,v): (v,k), reverse=True)

    most_common = []
    for key, value in countDict:
        if value >= thresh:
            most_common.append(key)


    print most_common





