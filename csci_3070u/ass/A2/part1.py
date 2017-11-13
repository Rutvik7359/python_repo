from util import *


# =============================================================================
# Minimum Edit Distance Functions
# =============================================================================
def min_edit_distance(str_1, str_2):
    m = len(str_1) + 1
    n = len(str_2) + 1

    D = np.zeros(shape=(m, n), dtype=int)

    for i in range(1, m):
        D[i][0] = i

    for j in range(1, n):
        D[0][j] = j

    # init backtrace pointer
    ptr = np.zeros(shape=(n-1, m-1), dtype=str)

    for i in range(1, m):
        for j in range(1, n):
            delete = D[i-1][j] + 1
            insert = D[i][j-1] + 1
            substitution = D[i-1][j-1] + sub_value(str_1[i-1], str_2[j-1])

            D[i][j] = minimum(delete, insert, substitution)

            # setting backtrace pointer
            # diagonal
            if D[i][j] == substitution:
                ptr[j-1][i-1] = "d"
            # up
            elif D[i][j] == delete:
                ptr[j-1][i-1] = 'u'
            # left
            else:
                ptr[j-1][i-1] = 'l'

    backtrace_align_str(ptr, str_1, str_2)

# gets the substitution value base don two characters at an index
def sub_value(char_1, char_2):
    sub = 2

    if char_1 == char_2:
        sub = 0

    return sub

# aligns the strings based on the stored backtrace pointer
def backtrace_align_str(ptr, str_1, str_2):
    i = len(str_1) - 1
    j = len(str_2) - 1
    str1 = ""
    str2 = ""

    while i >= 0 or j >= 0:
        if i >=0 and j >= 0:
            p = ptr[j][i]
            char1 = str_1[i]
            char2 = str_2[j]
        else:
            if i < 0:
                char1 = "*"
                char2 = str_2[j]
                p = ptr[j][0]
            else:
                char1 = str_1[i]
                char2 = "*"
                p = ptr[0][i]

        # diagonal
        if p == 'd':
            str1 = char1 + str1
            str2 = char2 + str2
            i -= 1
            j -= 1

        # up
        elif p == 'u':
            str1 = char1 + str1
            str2 = "*" + str2
            i -= 1

        # left
        elif p == 'l':
            str1 = "*" + str1
            str2 = char2 + str2
            j -= 1

    print str1
    print str2


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print_title("Minimum Edit Distance")

    word1 = ""
    word2 = ""

    usage = "Usage: python part1.py <word1>(optional) <word2>(optional)"
    num_args, error = check_args(2, usage)

    if num_args == 2:
        word1 = str(sys.argv[1])
        word2 = str(sys.argv[2])
    elif num_args == 1:
        print "Error: Enter 2 words to compare"
        error = True

    if error:
        sys.exit(0)

    if num_args == 2:
        print word1 + '/' + word2 + ':'
        min_edit_distance(word1, word2)
    else:
        print 'intention/execution:'
        min_edit_distance('intention', 'execution')

        print '\nspoof/stool:'
        min_edit_distance('spoof', 'stool')

        print '\npodiatrist/pediatrician:'
        min_edit_distance('podiatrist', 'pediatrician')
        
        print '\nblaming/conning:'
        min_edit_distance('blaming', 'conning')

    print ''



