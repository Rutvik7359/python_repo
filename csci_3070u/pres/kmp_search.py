import numpy as np

def build_table(word):
    n = len(word)
    count = 0 # keeps track of time complexity
    
    T = np.zeros(n + 1, int)
    T[0] = -1
    c = 0 # next character of current candidate substring

    # i is current position to determine in T
    for i in range(1, n):
        #print i
        count += 1

        if word[i] == word[c]:
            T[i] = T[c]
        else:
            T[i] = c
            c = T[c]

            while c >= 0 and not word[i] == word[c]:
                count += 1
                c = T[c]
        c += 1

    T[-1] = c
    print T
    return T, count

#      ci      
#      0123456
#      ABABDAB
# T = -1000000
# A != B, T[1]=c (0), c=T[0] (-1), c++ (0)

#      c i           c i
#      0123456      01 23456
#      ABABDAB      AB ABDAB
# T = -1000000     -10-10000
# A == A, T[2]=T[0] (-1), c++ (1)

#       c  i            ci
#      01 23456      01 23456
#      AB ABDAB      AB ABDAB
# T = -10-10000     -10-10000
# B == B, T[3]=T[1] (0), c++ (2)

#         c i        c    i
#      01 23456      01 23456
#      AB ABDAB      AB ABDAB
# T = -10-10200     -10-10200
# A != D, T[4]=c (2), c = T[2] (-1), c++ (0)

#      c     i        c     i
#      01 23456      01 234 56
#      AB ABDAB      AB ABD AB
# T = -10-10200     -10-102-10
# A == A, T[5]=T[0] (-1), c++ (1)

#       c      i         c    i
#      01 234 56      01 234 56
#      AB ABD AB      AB ABD AB
# T = -10-102-10     -10-102-10
# B == B, T[6]=T[1] (0), c = T[1] (0), c++ (2)

# T[-1] = c (2)
# T = -10-102-102

def kmp_search(search_word, text):
    n_text = len(text)
    n_word = len(search_word)

    P = [] # indecies in text that the search word is found
    m = 0 # text index
    i = 0 # search word index

    # get the kmp table for the search word
    T, count = build_table(search_word)

    num_pos = 0

    while (m + i) < n_text:
        count += 1
        if search_word[i] == text[m + i]:
            i += 1
            if i == n_word:
                P.append(m)
                num_pos += 1
                m = m + i - T[i]
                i = T[i]
        else:
            if T[i] > -1:
                m += i - T[i]
                i = T[i]

            else:
                m += i + 1
                i = 0

    print "indecies, time:"
    return P, count


#                                      1         2
#                 0123456    0123456789012345678901234567
print kmp_search("ABABDAB", "ABC  ABCDAB AABABDABABDABCAB")

