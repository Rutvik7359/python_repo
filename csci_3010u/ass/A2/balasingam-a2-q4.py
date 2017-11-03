import random
import numpy as np

def simulate_leaf_fall(h):
    y = h
    x = 0

    while y > 0:
        change = random.uniform(0, 1)


        # P(0.1) of moving up
        if change > 0.05 and change <= 0.15:
            y += 1
        # P(0.55) of moving down
        elif change > 0.15 and change <= 0.70:
            y -= 1
        # P(0.15) of moving left
        elif change > 0.70 and change <= 0.85:
            x -= 1
        # P(0.15) of moving right
        elif change > 0.85 and change <= 1.0:
            x += 1
        # P(0.05) of staying in the same spot

    return x

n = 1000
sum = 0
disp = []
for h in range (100, 1000):
    for i in range(0, n):
        disp.append(simulate_leaf_fall(h))
    print str(h) + ": " + str(np.var(disp))


