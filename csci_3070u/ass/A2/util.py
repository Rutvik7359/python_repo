from numpy import random
from collections import Counter
import numpy as np, operator as op, sys, os.path, os


# =============================================================================
# Helper Functions
# =============================================================================
def clear_screen():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')

def minimum(val_1, val_2, val_3):
    return min(min(val_1, val_2), val_3)