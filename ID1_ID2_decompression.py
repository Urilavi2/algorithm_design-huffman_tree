import sys
from time import sleep
import os
import inspect


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


def write_to_txt_file(text: str, file_name: str):
    if not os.path.exists(file_name):
        new_file = open(file_name, 'a', encoding='utf-8')
    else:
        new_file = open(file_name, 'w', encoding='utf-8')
    new_file.write(text)
    new_file.close()


def read_file(file_path):
    try:
        file = open(file_path, "r", encoding='utf-8')
        text = file.read()
        file.close()
        return text
    except Exception as e:
        print(str(e))


def extract_order(text):
    """
    Extract from the end of the file the order of the tree.

    NOTE:
    -----
    there is no check if there is a list! it should be there and should be separate from data by '\\n'
    :param text: string with a list at the end of file's data
    :return: tuple of list and the new text without the list
    """
    idx = len(text) - 1
    placeholder = text[idx]
    while placeholder != '\n':
        idx -= 1
        placeholder = text[idx]
    order_list = []
    new_text = text[:idx]
    order = text[idx + 1:len(text)]
    long_string = ''
    while order:
        temp_letter = order[0]
        order = order[1:]
        if temp_letter == ',' and order[0] == ',':
            order_list.append(long_string)
            long_string = ''
            order_list.append(temp_letter)
            order = order[2:]
            continue

        if temp_letter != ',':
            long_string += temp_letter
        else:
            if long_string == '\\n':
                long_string = '\n'
            order_list.append(long_string)
            long_string = ''

    order_list.append(long_string)
    return order_list, new_text


def search(arr, start, end, value):
    """
    Search for value in array
    :param arr: list
    :param start: index integer to start
    :param end: index integer to stop
    :param value: value to look for
    :return: value's index
    """
    for i in range(start, end + 1):
        if arr[i] == value:
            return i


def buildTree(inorder, preorder, in_start, in_end, pre_index=0):
    """
    Recursive function to build a binary tree from preorder and inorder traversals
    :param inorder: inorder traversal list
    :param preorder: preorder traversal list
    :param in_start: index to start
    :param in_end: index to stop
    :param pre_index: DO NOT ENTER A VALUE!
    :return: Binary tree of Nodes
    """
    if in_start > in_end:
        return None, pre_index

    # Pick current node from preorder traversal using
    # preIndex and increment preIndex
    info = preorder[pre_index]
    try:
        node = Node(unique_value=int(info))
        node.letters = "1234567890"
    except ValueError:
        node = Node(letters=info)
    pre_index += 1

    # If this node has no children then return
    if in_start == in_end:
        return node, pre_index

    # Else find the index of this node in inorder traversal
    in_index = search(arr=inorder, start=in_start, end=in_end, value=info)

    # Using index in inorder Traversal, construct left 
    # and right subtrees
    node.left, pre_index = buildTree(inorder=inorder, preorder=preorder, in_start=in_start, in_end=in_index - 1, pre_index=pre_index)
    node.right, pre_index = buildTree(inorder=inorder, preorder=preorder, in_start=in_index + 1, in_end=in_end, pre_index=pre_index)

    return node, pre_index


def build_huffman_codes(node: Node, left=True, code='', hashmap={}):
    """
    recursive function that apply the huffman code algorithm

    :param node: type Node, consider as the root of our huffman-tree
    :param left: indicator for left leaf
    :param code: recursive argument, used for gather the '1' and '0' to establish the right code for each letter
    :param hashmap: KEEP IT EMPTY, recursive argument, will contain the letter codex
    :return: binary hashmap
    """
    l, r = node.children()
    if not l and not r:
        hashmap[str(code)] = str(node)
        return hashmap
    node.set_code(code)
    if l:
        build_huffman_codes(node=l, left=True, code=code + "0", hashmap=hashmap)
    if r:
        build_huffman_codes(node=r, left=False, code=code + "1", hashmap=hashmap)
    return hashmap


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


def text_to_binary(text, placeholder) -> str:
    """
    Convert coded text (by Huffman code) to binary.
    :param text: compressed text by Huffman code
    :param placeholder: Place-holder for unprintable chars
    :return: binary text string
    """
    binary_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == placeholder:
            if text[idx + 1] == placeholder:
                original = 127
            else:
                original = 64 - ord(text[idx + 1])

            idx += 2
        else:
            original = ord(text[idx])
            idx += 1

        binary_text += str(format(original, '08b'))

    return binary_text


def zero_padding_organizer(text):
    """
    clean text from zero padding
    :param text: text with zero padding. The amount of padding is in the first byte
    :return: Plain text
    """
    zeros_amount = int(chr(int(text[0:8], 2)))
    text = text[zeros_amount+8:]
    return text


def text_compare(file1: str, file2: str):
    try:
        com_bin_file = open(file1, 'r')
        decom_bin_file = open(file2, 'r')
        com = com_bin_file.read()
        decom = decom_bin_file.read()
        return com == decom
    except Exception as e:
        print(e)


def huffman_decoder(original_binary: str, huffman_hash: dict):
    """
    Decode binary string by the given Huffman hashmap to a readable text.
    :param original_binary: Binary string of the original data
    :param huffman_hash: Huffman code hashmap, key-value pairs of binary_sequence-letter
    :return: original text
    """
    prefix = ""
    original_text = ""
    idx = 0
    huffman_binary = list(huffman_hash.keys())
    min_len = len(min(huffman_binary, key=lambda x: len(x)))
    while idx < len(original_binary):
        prefix += original_binary[idx]
        if len(prefix) >= min_len and prefix not in huffman_binary:
            try:
                letter = huffman_hash[prefix[:-1]]
            except KeyError:
                idx += 1
                continue
            original_text += letter
            prefix = ""
            continue
        idx += 1
    if prefix:
        try:
            letter = huffman_hash[prefix]
            original_text += letter
        except KeyError:
            pass
    return original_text


def text_decoding(text, huffman_histogram: dict):
    """
    Decode a text string by Huffman histogram.
    The first letter in the text string is the place-holder indicator
    :param text: string
    :param huffman_histogram: hashmap of binary_sequence-letter
    :return: Original text
    """
    placeholder = text[0]
    binary_text = text_to_binary(text[1:], placeholder=placeholder)
    original_binary = zero_padding_organizer(binary_text)
    return huffman_decoder(original_binary, huffman_histogram)


def main():
    output_file = "ID1_ID2_decompressed.txt"
    garbage = None
    try:
        if (len(sys.argv)) > 1:
            file_name = sys.argv[1]
            if os.path.exists(file_name):
                file_directory = os.getcwd()
                file_path = file_directory + '/' + file_name
                text = read_file(file_path)
                if text:
                    preorder, text = extract_order(text)
                    inorder, text = extract_order(text)
                    root, garbage = buildTree(inorder=inorder, preorder=preorder, in_start=0, in_end=len(inorder) - 1)
                    huffman_codes_hash = build_huffman_codes(root)
                    original_text = text_decoding(text, huffman_histogram=huffman_codes_hash)
                    write_to_txt_file(original_text, output_file)
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
