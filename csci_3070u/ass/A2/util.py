from sys import platform
import os



# =============================================================================
# Helper Functions
# =============================================================================
def clear_screen():
    if platform == "win32":
        os.system('cls')
    else:
        os.system('clear')

def minimum(val_1, val_2, val_3):
    return min(min(val_1, val_2), val_3)