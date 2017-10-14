
def search_word(input_str, search_str):
    input_len = len(input_str)
    search_len = len(search_str)

    if (search_str == input_str):
        return True
    elif (search_len >= input_len or search_len == 0):
        return False
    else:
        return div_search(input_str, search_str, 0, len(input_str))


def div_search(input_str, search_str, l, r):
    print input_str[l:r]

    mid = (l+r)//2
    checks = False
    if (input_str[mid] == search_str[0]):
        checks = check(input_str, search_str, mid)

    if checks:
        return True

    if l+1 >= r:
        return False
    

    return div_search(input_str, search_str, l, mid) or div_search(input_str, search_str, mid, r)

def check(input_str, search_str, i):
    print "checking...."
    search_len = len(search_str)
    in_len = len(input_str)

    if (i + search_len <= in_len):
        if (input_str[i:i+search_len] == search_str):
            return True
    
    return False


search_str = " "
input_str  = "  d"
if (search_word(input_str, search_str)):
    print "search word exists"
else:
    print "search word DNE"

