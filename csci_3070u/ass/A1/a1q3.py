
def search_word(input_str, search_str):
    return div_search(input_str, search_str, 0, len(input_str))


def div_search(input_str, search_str, l, r):

    print input_str[l:r]

    mid = (l+r)//2
    if (input_str[mid] == search_str[0]):
        return check(input_str, search_str, mid)

    if l + 1 >= r:
        return False

    return div_search(input_str, search_str, l, mid) or div_search(input_str, search_str, mid, r)

def check(input_str, search_str, i):
    print "checking...."
    search_len = len(search_str)
    in_len = len(input_str)

    if (i + search_len < in_len):
        if (input_str[i:i+search_len] == search_str):
            return True
    
    return False



search_str = "string"

input_str = "You have a long string containing many characters (such as this paragraph), and you want to search for a substring within this string"
if (search_word(input_str, search_str)):
    print "search word exists"
else:
    print "search word DNE"

