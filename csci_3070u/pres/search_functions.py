import numpy as np

def get_kmp_table(word):
    n = len(word)
    
    T = np.zeros(n + 1, int)
    T[0] = -1
    c = 0

    for i in range(1, n):
        curr_char = word[i]
        rep_char = word[c]
        if curr_char == rep_char:
            T[i] = T[c]
        else:
            T[i], c = c, T[c]

            while c >= 0 and word[i] != word[c]:
                c = T[c]

        c += 1

    T[-1] = c

    print T
    return T

def kmp_search(search_word, text):
    n_text = len(text)
    n_word = len(search_word)

    P = [] # indecies in text that the search word is found
    j = 0 # text index
    i = 0 # search word index

    # get the kmp table for the search word
    T = get_kmp_table(search_word)

    while (j + i) < n_text:
        if search_word[i] == text[j + i]:
            i += 1
            if i == n_word:
                P.append(j)
                j += i - T[i]
                i = T[i]
        else:
            if T[i] > -1:
                j += i - T[i]
                i = T[i]

            else:
                j += i + 1
                i = 0

    print "indecies, time:"
    return P


