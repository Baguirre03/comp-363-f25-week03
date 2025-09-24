from Node import Node

ALPHABET_COUNT = 27


def filter_uppercase_and_spaces(input_string: str) -> str:
    """
    Filters the input string to retain only uppercase letters and spaces.
    """
    return "".join(
        char for char in input_string.upper() if char.isalpha() or char == " "
    )


def count_frequencies(input_string: str) -> list[int]:
    """
    Counts the frequency of each uppercase letter in the input string.
    Returns a list of 26 integers, where index 0-25 correspond to 'A'-'Z'.
    You can assume the input string contains only uppercase letters and spaces.
    And that spaces are the most frequent character, so really we dont need
    to count them.
    """
    freq_array: list[int] = [0] * ALPHABET_COUNT
    for char in input_string:
        if char != " ":
            # if not space then find the index - A to put it into 26 fit
            freq_array[ord(char) - ord("A")] += 1
        else:
            # put the last index as the "space"
            freq_array[-1] += 1
    return freq_array


def initialize_forest(frequencies: list[int]) -> list[Node]:
    """
    Initializes a forest (list) of Node objects for each character with a non-zero frequency.
    """
    node_array: list[Node] = []
    for index, freq in enumerate(frequencies):
        # check if the char has a frequency
        if index == len(frequencies) - 1:
            node_array.append(Node(freq, " "))
        elif freq:
            # grab the char
            char = chr(index + ord("A"))
            node_array.append(Node(freq, char))

    return node_array


def find_least_frequent_nodes(node_array: list[Node]) -> int:
    """
    Returns the index of the smallest node within the forest
    so we can pop it in the building of the huffman tree
    """
    smallest = Node(frequency=float("Inf"))
    smallest_index = -1
    for index, node in enumerate(node_array):
        if node.__lt__(smallest):
            smallest = node
            smallest_index = index
    return smallest_index


def build_huffman_tree(frequencies: list[int]) -> Node:
    """
    Builds the Huffman tree from the list of frequencies and returns the root Node.
    """
    forest: list[Node] = initialize_forest(frequencies)  # returns all the nodes
    while len(forest) > 1:
        # find two smallest nodes in forest
        first_smallest: Node = forest.pop(find_least_frequent_nodes(forest))
        second_smallest: Node = forest.pop(find_least_frequent_nodes(forest))
        # create a new parent node with frequencies added
        parent_node = Node(
            first_smallest.get_frequency() + second_smallest.get_frequency()
        )
        # set nodes children
        parent_node.set_left(first_smallest)
        parent_node.set_right(second_smallest)
        # add parent node back into forest
        forest.append(parent_node)

    # Your code here
    return forest[0]


def build_encoding_table(huffman_tree_root: Node) -> list[str]:
    """
    Builds the encoding table from the Huffman tree.
    Returns a list of 27 strings, where index 0-25 correspond to 'A'-'Z'
    and index 26 corresponds to space.
    Each string is the binary encoding for that character.
    """
    encoded_table: list[str] = [0] * ALPHABET_COUNT

    def dfs(node: Node, cur_string: list[str]):
        if node.get_symbol():
            sym = node.get_symbol()
            if sym != " ":
                encoded_table[ord(sym) - ord("A")] = "".join(cur_string)
            else:
                encoded_table[-1] = "".join(cur_string)

        if node.get_left():
            cur_string.append("0")
            dfs(node.get_left(), cur_string)
            cur_string.pop()
        if node.get_right():
            cur_string.append("1")
            dfs(node.get_right(), cur_string)
            cur_string.pop()
        return

    dfs(huffman_tree_root, [])
    return encoded_table


def encode(input_string: str, encoding_table: list[str]) -> str:
    """
    Encodes the input string using the provided encoding table. Remember
    that the encoding table has 27 entries, one for each letter A-Z and
    one for space. Space is at the last index (26).
    """
    encoded_str: list[str] = []
    for char in input_string:
        binary = ""
        if char == " ":
            binary = encoding_table[-1]
        else:
            binary = encoding_table[ord(char) - ord("A")]
        encoded_str.append(binary)
    return "".join(encoded_str)


def decode(encoded_string: str, huffman_root: Node) -> str:
    """
    Decodes the encoded string using the Huffman table as a key.
    """
    # current node for tree traversal
    cur_node: Node = huffman_root
    res = []
    # turn to list for indexes
    encoded_arr: list[str] = list(encoded_string)

    for i in range(len(encoded_arr)):
        # check if we have a symbol in our tree
        if cur_node.get_symbol():
            # if we do add it to the result
            res.append(cur_node.get_symbol())
            cur_node = huffman_root
        # still move the ucrrent node by which binary we are at
        if encoded_arr[i] == "0":
            cur_node = cur_node.get_left()
        elif encoded_arr[i] == "1":
            cur_node = cur_node.get_right()
    res.append(cur_node.get_symbol())
    return "".join(res)


def main(input_string: str):
    # count frequencies
    freq_map: list[int] = count_frequencies(input_string)
    # make the tree and return forest head
    forest_head: Node = build_huffman_tree(freq_map)
    # build the encoded table
    encoding_table: list[str] = build_encoding_table(forest_head)
    # encode the string
    encoded_str: str = encode(input_string, encoding_table)
    # finally return the res
    decoded_str: str = decode(encoded_str, forest_head)

    print(encoded_str, decoded_str)
    return decoded_str


TEST_STRING = "HELLO WORLD THIS IS A MUCH LONGER TEST"
if __name__ == "__main__":
    main(TEST_STRING)
