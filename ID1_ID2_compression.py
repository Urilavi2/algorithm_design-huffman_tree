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
        return self.letters


def read_file(file_path):
    try:
        file = open(file_path, "r")
        text = file.read()
        file.close()
        return text
    except Exception as e:
        print(str(e))


def inorder_interval(root: Node, inorder_list=[]):
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


def make_text_binary(text: str, huffman_code: dict):
    binary_text = ""
    for letter in text:
        binary_text += huffman_code[letter]
    return binary_text


def text_encoder(text: str, huffman_code: dict):
    new_file = open("ID1_ID2_compressed.txt", "w", encoding='utf-8')
    for i in range(0, len(text), 8):
        write_to_file = ""
        bits_chunk = text[i: i + 8]
        integer_bits = int(bits_chunk, 2)
        if integer_bits < 32 or integer_bits > 126:
            dif = 255 - integer_bits


    new_file.write('\n')
    new_file.close()


def build_huffman_codes(node: Node, left=True, code='', hashmap={}):
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


def main():
    try:
        if (len(sys.argv)) > 1:
            file_name = sys.argv[1]
            if os.path.exists(file_name):
                file_directory = os.getcwd()
                file_path = file_directory + '/' + file_name
                text = read_file(file_path)
                if text:
                    print(text[-1])
                    text = text[:-3]  # "\x1a" == EOF
                    text_histogram = filter_abc(text)
                    text_histogram = sorted(text_histogram.items(), key=lambda x: x[1], reverse=True)

                    unique_value = len(text_histogram)
                    # no meaning for the number itself as long that every junction has a unique number

                    nodes_list = [(Node(letters=key, count=val), val) for key, val in text_histogram]

                    while len(nodes_list) > 1:
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
                    huffman_code = build_huffman_codes(nodes_list[0][0])

                    # ~~~~~~~~~~~~~~ PRINTING ~~~~~~~~~~~~~~~#

                    # print(' Char | Huffman code      | Count ')
                    # for letter, val in text_histogram:
                    #     print(' %-4r |%16s   |%s' % (letter, huffman_code[letter], val))

                    inorder = inorder_interval(nodes_list[0][0])
                    preorder = preorder_interval(nodes_list[0][0])
                    binary_huffman_text = make_text_binary(text, huffman_code)

                    #  zero padding - the first byte of the file indicate the number of zeros of padding
                    modulo = len(binary_huffman_text) % 8
                    padding = ""
                    if modulo:
                        padding += format(ord(str(8 - modulo)), '08b')  # first byte, how many pads
                        print(str(8 - modulo), padding)
                        for i in range(0, 8 - modulo):
                            padding += '0'

                    else:  # if we did not pad at all
                        padding += '0'
                    binary_huffman_text = padding + binary_huffman_text

                    # end of zero padding

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