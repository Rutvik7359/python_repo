from util import *

# =============================================================================
# Constants
# =============================================================================
FILE = "retail.txt"


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
    countDict = sorted(get_char_freq(FILE).iteritems(), key=lambda (k,v): (v,k), reverse=True)

    print countDict


