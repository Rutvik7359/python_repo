from sys import platform
import numpy as np, os

# Env variables
WIN = False


# =============================================================================
# Levenshtein Functions
# =============================================================================
def sub_value(char_1, char_2):
    sub = 2

    if char_1 == char_2:
        sub = 0

    return sub


def minimum(val_1, val_2, val_3):
    return min(min(val_1, val_2), val_3)


def backtrace_align_str(ptr, str_1, str_2):
    i = len(str_1) - 1
    j = len(str_2) - 1
    str1 = ""
    str2 = ""

    while i >= 0 or j >= 0:
        # diagonal
        if ptr[i][j] == "d":
            str1 = str_1[i] + str1
            str2 = str_2[j] + str2
            i -= 1
            j -= 1

        # up
        elif ptr[i][j] == 'u':
            str1 = str_1[i] + str1
            str2 = "*" + str2
            i -= 1

        # left
        elif ptr[i][j] == 'l':
            str1 = "*" + str1
            str2 = str_2[j] + str2
            j -= 1

    print str1
    print str2

def levenshtein(str_1, str_2):
    m = len(str_1) + 1
    n = len(str_2) + 1

    D = np.zeros(shape=(m, n), dtype=int)

    for i in range(1, m):
        D[i][0] = i

    for j in range(1, n):
        D[0][j] = j

    ptr = np.zeros(shape=(m-1, n-1), dtype=str)

    for i in range(1, m):
        for j in range(1, n):
            delete = D[i-1][j] + 1
            insert = D[i][j-1] + 1
            substitution = D[i-1][j-1] + sub_value(str_1[i-1], str_2[j-1])

            D[i][j] = minimum(delete, insert, substitution)


            if D[i][j] == substitution or str_1[i-1] == str_2[j-1]:
                ptr[i-1][j-1] = "d"
            # up
            elif D[i][j] == delete:
                ptr[i-1][j-1] = 'u'
            # left
            else:
                ptr[i-1][j-1] = 'l'

    backtrace_align_str(ptr, str_1, str_2)


# =============================================================================
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

    print 'intention/execution:'
    levenshtein('intention', 'execution')
    print '\nspoof/stool:'
    levenshtein('spoof', 'stool')
    print '\npodiatrist/pediatrician:'
    levenshtein('podiatrist', 'pediatrician')
    print '\nblaming/conning:'
    levenshtein('blaming', 'conning')

    print ''



