from search_functions import *
import sys, os

def clear_screen():
    if sys.platform == "win32":
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":
    clear_screen()
    #                                          1         2         3         4
    #                 01234567890    01234567890123456789012345678901234567890
    print kmp_search("BABCABDABCD", "ABC  ABCDAB AABABDABABDABCAB")
    print kmp_search("PARTICIPATE IN PARACHUTE", "ABC  ABCDAB AABABDABABDABCAB")
    print kmp_search("ABAB",   "ABC ABACABABABACAABACABABCJJKJABACABABC")