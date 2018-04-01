from util import *

# =============================================================================
# Constants
# =============================================================================
FILE = "retail.dat"
THRESHOLD = 2000


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


def get_char_freq_pairs(file, combs):
    d = dict()
    with open(file) as f:
        for line in f:
            for c in combs:
                if c[0] in line and c[1] in line:
                    if str(c) in d:
                        d[str(c)] += 1
                    else:
                        d[str(c)] = 1
    return d

def get_char_freq_trips(file, combs):
    d = dict()
    with open(file) as f:
        for line in f:
            for c in combs:
                if c[0] in line and c[1] in line and c[2] in line:
                    if str(c) in d:
                        d[str(c)] += 1
                    else:
                        d[str(c)] = 1
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


    combs_2 = [list(x) for x in itertools.combinations(most_common, 2)]
    combs_3 = [list(x) for x in itertools.combinations(most_common, 3)]

    print "PAIRS"
    print len(get_char_freq_pairs(FILE, combs_2))
    print "\nTRIPLES"
    print len(get_char_freq_trips(FILE, combs_3))







