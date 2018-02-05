from util import *

# =============================================================================
# Constants
# =============================================================================
FILE = "retail.dat"
THRESHOLD = 5000

def PCY_hash(item1, item2, num=3):
    return (int(item1) ^ int(item2)) % num


# gets character frequency from given ascii text file
def get_char_freq(file):
    pair_count = dict()
    item_count = dict()
    with open(file) as f:
        for line in f:

            tempData = line.split()

            for t in tempData:
                if (t in item_count):
                    item_count[t] += 1
                else:
                    item_count[t] = 1


            basket_pairs = list(itertools.combinations(tempData, 2))

            # print basket_pairs

            for b in basket_pairs:
                j = PCY_hash(b[0], b[1], 5)

                if j in pair_count:
                    pair_count[j] += 1
                else:
                    pair_count[j] = 1

    return item_count, pair_count


# def get_char_freq_pairs(file, combs):
#     d = dict()
#     with open(file) as f:
#         for line in f:
#             for c in combs:
#                 if c[0] in line and c[1] in line:
#                     if str(c) in d:
#                         d[str(c)] += 1
#                     else:
#                         d[str(c)] = 1
#     return d


if __name__ == "__main__":
    clear_screen()
    usage = "Usage: python lab1.py <threshold>(optional)"
    num_args, error = check_args(1, usage)

    if error:
        sys.exit(0)

    thresh = THRESHOLD
    if num_args == 1:
        thresh = int(sys.argv[1])


    item_count, pair_count = get_char_freq(FILE)
    countDict = sorted(pair_count.iteritems(), key=lambda (k,v): (v,k), reverse=True)

    most_common = []
    for key, value in countDict:
        if value >= thresh:
            most_common.append(key)


    print "Frequent Pairs"
    print most_common


    pair_common = []
    with open(FILE) as f:
        for line in f:
            tempData = line.split()
            basket_pairs = list(itertools.combinations(tempData, 2))
            for b in basket_pairs:
                j = PCY_hash(b[0], b[1], 5)

                if j in most_common:
                    pair_common.append(b)


    print len(pair_common)

    for i in range(len(pair_common)):
        if (pair_common[i] > 2):
            pair_common[i] = 1




