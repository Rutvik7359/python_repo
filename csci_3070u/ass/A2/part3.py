from util import *
from numpy import random
import numpy as np, operator

# =============================================================================
# Constants
# =============================================================================
WEIGHT_CAP = 75.0 #lbs
NUM_ITEMS = 10


class Item():
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = float(value)/weight
        self.fraction = 0.0

    def set_fraction(self, fraction):
        self.fraction = fraction


def get_knapsack(weight, items):
    items = sorted(items, reverse=True, key=operator.attrgetter('ratio'))
    remain_weight = weight
    total_value = 0

    knapsack = []
    for item in items:
        if (item.weight <= remain_weight):
            knapsack.append(item)
            item.set_fraction(1.0)
            remain_weight -= item.weight
            total_value += item.value
        else:
            frac = remain_weight/item.weight
            item.set_fraction(frac)
            total_value += item.value*frac
            break

    return items, total_value

# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    clear_screen()


    items = []
    for i in range(0, NUM_ITEMS):
        weight = round(random.uniform(1, 20), 2)
        value = random.randint(1, 200)

        items.append(Item(weight, value))

    items, opt_value = get_knapsack(WEIGHT_CAP, items)

    total_weight = 0
    i = 0
    print "item #\tweight\tvalue\tratio\tfraction in knapsack"
    for item in items:
        total_weight += item.weight*item.fraction
        i += 1
        print str(i) + "\t" + str(item.weight) + "\t" + str(item.value) + "\t" + str(round(item.ratio, 2)) + "\t\t" + str(round(item.fraction, 2))

    print "\nThe optimum value is " + str(opt_value)