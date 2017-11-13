from util import *


# =============================================================================
# Constants
# =============================================================================
FILE = "file.txt"


# =============================================================================
# Node Class
# =============================================================================
class Node():
    def __init__(self, value, key=None):
        self.value = value
        self.key = key
        self.left = None
        self.right = None
        self.code = ""

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def set_code(self, code):
        self.code = code


# =============================================================================
# Huffman Function
# =============================================================================
def huffman(countDict):
    print_title("HUFFMAN TREE", False, '-')

    keyList = list(set(countDict.elements()))
    valList = sorted([countDict[k] for k in keyList])
    nodes = []
    for i in range(0, len(keyList)):
       nodes.append(Node(valList[i], keyList[i]))

    while len(nodes) > 1:
        nodes = sorted(nodes, key=op.attrgetter('value'))
        node1 = nodes.pop(0)
        node2 = nodes.pop(0)

        newNode = Node(node1.value + node2.value)
        newNode.set_left(node1)
        newNode.set_right(node2)
        nodes.append(newNode)

    # convert tree to array and then print tree
    node = nodes.pop()
    arr = []
    tree_to_array(node, arr, 0)
    print_tree(arr, 0, 0)

    return arr, print_table(arr)


# =============================================================================
# Helper Functions
# =============================================================================
# prints table with prefix codes for each character and returns the new size of
# the document
def print_table(arr):
    print ""
    print_title("HUFFMAN TABLE", False, '-')

    length = 0
    print "Character\tValue\tCode"
    for node in arr:
        if node.key != None:
            length += node.value*len(node.code)
            print " "*4 + str(node.key) + "\t\t" + str(node.value) + "\t" + node.code

    return float(length)/8.

# prints a binary tree with prefix codes for each character
def print_tree(arr, i, depth, code=""):
    r = r_child(i)
    l = l_child(i)
    heap_size = len(arr)

    if r < heap_size:
        print_tree(arr, r, depth + 1, code + "1")
    else:
        print_nodes(arr[i], code, depth)
    
    if l < heap_size:
        if r < heap_size:
            print_nodes(arr[i], code, depth)
        print_tree(arr, l, depth + 1, code + "0")

# prints the character, frequency and code(also sets it) at each node 
# (if they exist)
def print_nodes(node, code, depth):
    if node.value != -1:
        if node.key == None:
            print "\t"*depth + str(node.value)
        else:
            node.set_code(code)
            print "\t"*depth + str(node.key) + ":" + str(node.value)

# converts binary tree to an array
def tree_to_array(node, arr, i, code=""):
    if i >= len(arr):
        while i >= len(arr):
            arr.append(Node(-1))
        arr[i] = node
    else:
        arr[i] = node

    if node.left != None:
        tree_to_array(node.left, arr, l_child(i), code)

    if node.right != None:
        tree_to_array(node.right, arr, r_child(i), code)

# Get left child index of i
def l_child(i):
    return 2*i + 1

# Get right child index of i
def r_child(i):
    return 2*i + 2

# gets character frequency from given ascii text file
def get_char_freq(file):
    with open(file) as f:
        counter = Counter()

        for x in f:
            counter += Counter(x.strip())

    return counter


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print_title("HUFFMAN CODING")
    
    file = FILE

    usage = "Usage: python part4.py <text_file>(optional)"
    num_args, error = check_args(1, usage)

    if num_args <= 1:
        if num_args == 1:
            file = str(sys.argv[1])

            if not os.path.isfile(file):
                print "Error: File " + file + " does not exist"
                error = True

    if error:
        sys.exit(0)

    countDict = get_char_freq(file)
    nodes, doc_size = huffman(countDict)

    print "\nThe length of the document before using prefix codes is " + str(nodes[0].value) + " bytes"
    print "\nThe length of the document after using prefix codes is " + str(doc_size) + " bytes\n"