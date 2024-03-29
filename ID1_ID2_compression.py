import os
import sys
import inspect
from time import sleep


class Node:
    def __init__(self, left=None, right=None, letters=None, count=None, code="", unique_value=0):
        self.left = left
        self.right = right
        self.letters = letters
        self.node_count = count
        self.code = code
        self.unique_value = unique_value

    def get_unique_value(self):
        return self.unique_value

    def children(self):
        return self.left, self.right

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code += code

    def set_child(self, left_child: bool, node):
        if left_child:
            self.left = node
        else:
            self.right = node

    def get_node_count(self):
        return self.node_count

    def get_letters(self):
        return self.letters

    def __str__(self):
        if len(self.letters) == 1:
            return self.letters
        else:
            return self.unique_value


def read_file(file_path):
    try:
        file = open(file_path, "r")
        text = file.read()
        file.close()
        return text
    except Exception as e:
        print(str(e))


def inorder_interval(root: Node, inorder_list=[]):
    """
    Inorder interval on a tree: left --> root --> right
    :param root: Node type
    :param inorder_list: List - KEEP IT EMPTY unless you want to add the tree from the root param to a list of your own
    :return: complete inorder list
    """
    if not root:
        return
    inorder_interval(root.left)
    if len(root.get_letters()) == 1:
        inorder_list.append(root.get_letters())
    else:
        inorder_list.append(str(root.get_unique_value()))
    inorder_interval(root.right)

    return inorder_list


def preorder_interval(root, preorder_list=[]):
    """
    Preorder interval on a tree: root --> left --> right
    :param root: Node type
    :param preorder_list: List - KEEP IT EMPTY unless you want to add the tree from the root param to a list of your own
    :return: complete preorder list
    """
    if not root:
        return
    if len(root.get_letters()) == 1:
        preorder_list.append(root.get_letters())
    else:
        preorder_list.append(str(root.get_unique_value()))
    preorder_interval(root.left, preorder_list)
    preorder_interval(root.right, preorder_list)

    return preorder_list


def filter_abc(text: str) -> dict:
    """
    Filter the input text to a letter histogram (hash table)
    :param text: string of text with no numbers
    :return: letter histogram
    """
    try:
        letter_histogram = {}
        for letter in text:
            try:
                letter_histogram[letter] += 1
            except KeyError:
                letter_histogram[letter] = 1
        return letter_histogram
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e


def make_text_binary(text: str, huffman_code: dict) -> str:
    """
    Make one long string from the original text string using the huffman decoding hash map
    :param text: text
    :param huffman_code: letter hashmap
    :return: The original text file decoded by the huffman code
    """
    binary_text = ""
    for letter in text:
        binary_text += huffman_code[letter]
    return binary_text


def find_placeholder(text):
    """
    Finds the unused character in text
    :param text: string
    :return: char, ASCII value
    """
    ascii_count = [0 for i in range(0, 256)]
    free_ascii = []
    for i in range(0, len(text), 8):
        bits_chunk = text[i: i + 8]
        integer_bits = int(bits_chunk, 2)
        if integer_bits > 31 and integer_bits != 127:
            ascii_count[integer_bits] += 1

    for idx in range(0, 256):
        if ascii_count[idx] == 0:
            if idx > 31 and idx != 127:
                return chr(idx)
            free_ascii.append(idx)

    for idx in range(0, 32):
        if idx in free_ascii and idx != 8:
            return chr(idx)
    raise Exception("no free placeholder for unprintable characters!")


def write_to_txt_file(text: str, file_name: str):
    """
    Write the encoded * binary * text to a file.
    Uses a placeholder to recognize invalid characters (ascii number lower than 32 or equal to 127)
    When encountering such character, we calculate the difference between '64' to the number we got.
    In the file, whenever we will find the placeholder (~) we know that following number afterward is that difference.

    When decoding, to find the original 8-bit stream, just calculate bit_stream = 64 - ord(difference)

    :param text: converted binary text
    :param file_name: file name to write to
    :return: None
    """
    if not os.path.exists(file_name):
        new_file = open(file_name, 'a', encoding='utf-8')
    else:
        new_file = open(file_name, 'w', encoding='utf-8')
    placeholder = find_placeholder(text)
    write_to_file = placeholder  # file first byte --> place holder!
    for i in range(0, len(text), 8):
        bits_chunk = text[i: i + 8]
        integer_bits = int(bits_chunk, 2)
        if integer_bits < 32 or integer_bits == 127:
            if integer_bits == 127:
                write_to_file = write_to_file + placeholder + placeholder
            else:
                dif = 64 - integer_bits  # to find the original bit stream --> integer_bits = 64 - dif

                write_to_file = write_to_file + placeholder + chr(dif)
        else:
            write_to_file += chr(integer_bits)
    new_file.write(write_to_file)
    new_file.write('\n')
    new_file.close()


def write_orders_to_file(inorder: list, preorder: list, file_name: str):
    """
    Write inorder and preorder lists to file
    :param inorder: Left-Root-Right
    :param preorder: Root-Left-Right
    :param file_name: string
    :return:
    """
    file = open(file_name, "a")
    for idx, node in enumerate(inorder):
        if node == "\n":
            node = "\\n"
        file.write(node)
        if idx != len(inorder)-1:
            file.write(",")
    file.write("\n")
    for idx, node in enumerate(preorder):
        if node == "\n":
            node = "\\n"
        file.write(node)
        if idx != len(preorder)-1:
            file.write(",")
    file.close()


def create_huffman_tree(nodes_list: list, unique_value: int):
    """
    Build Huffman tree
    :param nodes_list: list
    :param unique_value: integer
    :return: Tree's root
    """
    while len(nodes_list) > 1:  # building the huffman tree
        left, count1 = nodes_list[-1]
        right, count2 = nodes_list[-2]
        nodes_list = nodes_list[:-2]
        parent_code = left.get_code()[:-1]
        parent = Node(left=left,
                      right=right,
                      letters=left.get_letters() + "_" + right.get_letters(),
                      count=count1 + count2,
                      code=parent_code,
                      unique_value=unique_value)
        unique_value -= 1
        nodes_list.append((parent, count1 + count2))
        nodes_list = sorted(nodes_list, key=lambda x: x[1], reverse=True)
    return nodes_list[0][0]


def build_huffman_codes(node: Node, left=True, code='', hashmap={}):
    """
    recursive function that apply the huffman code algorithm

    :param node: type Node, consider as the root of our huffman-tree
    :param left: indicator for left leaf
    :param code: recursive argument, used for gather the '1' and '0' to establish the right code for each letter
    :param hashmap: KEEP IT EMPTY, recursive argument, will contain the letter codex
    :return: letter hashmap
    """
    l, r = node.children()
    if not l and not r:
        hashmap[str(node)] = code
        return hashmap
    node.set_code(code)
    if l:
        build_huffman_codes(node=l, left=True, code=code + "0", hashmap=hashmap)
    if r:
        build_huffman_codes(node=r, left=False, code=code + "1", hashmap=hashmap)
    return hashmap


def zero_padding(text):
    modulo = len(text) % 8
    padding = ""
    if modulo:
        padding += format(ord(str(8 - modulo)), '08b')  # second byte, how many pads
        for i in range(0, 8 - modulo):
            padding += '0'
    else:  # if we did not pad at all
        padding += format(48, '08b')
    text = padding + text
    return text


def main():
    output_file = "ID1_ID2_compressed.txt"

    try:
        if (len(sys.argv)) > 1:
            file_name = sys.argv[1]
            if os.path.exists(file_name):
                file_directory = os.getcwd()
                file_path = file_directory + '/' + file_name
                text = read_file(file_path)
                if text:
                    text_histogram = filter_abc(text)
                    text_histogram = sorted(text_histogram.items(), key=lambda x: x[1], reverse=True)
                    unique_value = len(text_histogram)
                    # there is no meaning for the number itself as long that every junction has a unique number

                    nodes_list = [(Node(letters=key, count=val), val) for key, val in text_histogram]

                    root = create_huffman_tree(nodes_list, unique_value)
                    huffman_code = build_huffman_codes(root)
                    # # ~~~~~~~~~~~~~~ PRINTING Huffman Codes ~~~~~~~~~~~~~~~#
                    # print(' Char | Huffman code      | Count ')
                    # for letter, val in text_histogram:
                    #     print(' %-4r |%16s   |%s' % (letter, huffman_code[letter], val))

                    inorder = inorder_interval(root)
                    preorder = preorder_interval(root)
                    binary_huffman_text = make_text_binary(text, huffman_code)
                    binary_huffman_text = zero_padding(binary_huffman_text)  # second byte = padding amount
                    write_to_txt_file(text=binary_huffman_text, file_name=output_file)  # first byte = place holder
                    write_orders_to_file(inorder=inorder, preorder=preorder, file_name=output_file)

            else:
                print(f"Did not found file name {file_name}. Exiting...")
                sleep(2)
                exit(-1)
        else:
            print("No file has been chosen! Exiting...")
            sleep(2)
            exit(-1)

    except Exception as e:
        frame = inspect.trace()[-1]
        line_number = frame.lineno
        function_name = frame.function
        print(f"FAILED TO START with error: {str(e)} in line number: {line_number}, in function: {function_name}")
        sleep(8)
        exit(-1)


if __name__ == "__main__":
    main()
