from util import *
from numpy import random
import numpy as np, operator

# =============================================================================
# Constants
# =============================================================================
WEIGHT_CAP = 100.0 #lbs
NUM_ITEMS = 10


class Item():
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = float(value)/weight
        self.fraction = 0.0

    def set_fraction(self, fraction):
        self.fraction = round(fraction, 2)


def get_knapsack(weight, items):
    items = sorted(items, key=operator.attrgetter('ratio'))
    remain_weight = weight

    knapsack = []
    for i in range(0, len(items)):
        if (items[i].weight <= remain_weight):
            knapsack.append(items[i])
            items[i].set_fraction(1.0)
            remain_weight -= items[i].weight
        else:
            items[i].set_fraction(remain_weight/items[i].weight)
            break


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

    get_knapsack(WEIGHT_CAP, items)

    total_weight = 0
    i = 0
    print "item #\tweight\tvalue\tfraction in knapsack"
    for item in items:
        total_weight = item.weight*item.fraction
        i += 1
        print str(i) + "\t" + str(item.weight) + "\t" + str(item.value) + "\t\t" + str(item.fraction)
