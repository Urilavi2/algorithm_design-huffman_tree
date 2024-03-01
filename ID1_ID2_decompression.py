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


def read_file(file_path):
    try:
        file = open(file_path, "r", encoding='utf-8')
        text = file.read()
        file.close()
        return text
    except Exception as e:
        print(str(e))


def extract_order(text):
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
    for i in range(start, end + 1):
        if arr[i] == value:
            return i


def buildTree(inorder, preorder, in_start, in_end, pre_index=0):
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
                    print(huffman_codes_hash)
            else:
                print(f"Did not found file name {file_name}. Exiting...")
                sleep(2)
                exit(-1)

            print("SUCCESS!")

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
