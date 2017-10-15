from sys import platform
import os

SEARCH_STR = "df substr sfd "
INPUT_STR = "fdgfdgdfgdfgdf substr sfd what"

# Env variables
WIN = False
DASH_SIZE = 40


# =============================================================================
# Search Functions
# =============================================================================
# Checks the base case and then calls the divide search if base cases fail
def search_word(input_str, search_str):
    input_len = len(input_str)
    search_len = len(search_str)

    if (search_str == input_str):
        return True, "c"
    elif (search_len >= input_len or search_len == 0):
        return False, "c"
    else:
        return div_search(input_str, search_str, 0, len(input_str)), "logn"


# Keeps dividing input string until the mid letter matches the first letter of
# the search string.
def div_search(input_str, search_str, l, r):
    #print input_str[l:r]

    mid = (l+r)//2
    checks = False
    if (input_str[mid] == search_str[0]):
        checks = check(input_str, search_str, mid)

    if checks:
        return True

    if l+1 >= r:
        return False
    
    return div_search(input_str, search_str, l, mid) or div_search(input_str, search_str, mid, r)


# Checks if search_str exists starting from index i of input_str
def check(input_str, search_str, i):
    #print "checking...."
    search_len = len(search_str)
    in_len = len(input_str)

    if (i + search_len <= in_len):
        if (input_str[i:i+search_len] == search_str):
            return True
    
    return False

# Other Functions
# =============================================================================
def clear_screen():
    if WIN:
        os.system('cls')
    else:
        os.system('clear')


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":

    if platform == "win32":
        WIN = True
    clear_screen()

    # Divide and conquer search
    found, bigO = search_word(INPUT_STR, SEARCH_STR)

    print "Search String: " + SEARCH_STR
    print "Input String: " + INPUT_STR + "\n"

    if found:
        print "Search word found with O(" + bigO + ") time"
    else:
        print "Search word not found with O(" + bigO + ") time"
    print "\n"

