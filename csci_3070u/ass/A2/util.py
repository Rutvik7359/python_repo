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

def print_title(title, clear=True, lineType="="):
    if clear:
        clear_screen()
        
    line = lineType*len(title)*2
    print line
    print title
    print line

def check_args(num_args, usage):
    arg_len = len(sys.argv) - 1
    error = False

    if arg_len > num_args:
        print usage
        error = True

    return arg_len, error