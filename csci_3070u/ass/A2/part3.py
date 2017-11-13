from util import *

# =============================================================================
# Constants
# =============================================================================
WEIGHT_CAP = 75.0 #lbs
NUM_ITEMS  = 10
VALUE_MAX  = 200


# =============================================================================
# Item Class
# =============================================================================
class Item():
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.ratio = float(value)/weight
        self.fraction = 0.0

    def set_fraction(self, fraction):
        self.fraction = fraction


# =============================================================================
# Knapsack Function
# =============================================================================
def get_knapsack(weight, items):
    items = sorted(items, reverse=True, key=op.attrgetter('ratio'))
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

# prints table with weight, value, ratio and fraction of item used
def print_table(items):
    i = 0
    print "item #\tweight\tvalue\tratio\tfraction in knapsack"
    for item in items:
        i += 1
        print str(i) + "\t" + str(item.weight) + "\t" + str(item.value) + "\t" + str(round(item.ratio, 2)) + "\t\t" + str(round(item.fraction, 2))


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print_title("Fractional Knapsack")

    num_items = NUM_ITEMS
    weight_cap = WEIGHT_CAP

    usage = "Usage: python part3.py <num_items>(optional) <weight_capacity>(optional)"
    num_args, error = check_args(2, usage)

    if num_args >= 1:
        num_items = int(sys.argv[1])
        if num_args == 2:
            weight_cap = int(sys.argv[2])

    if error:
        sys.exit(0)

    items = []
    for i in range(0, num_items):
        weight = round(random.uniform(1, 20), 2)
        value = random.randint(1, VALUE_MAX)

        items.append(Item(weight, value))

    items, opt_value = get_knapsack(weight_cap, items)

    print_table(items)   
    print "\nThe optimum value is " + str(opt_value) + " for a weight capacity of " + str(weight_cap)