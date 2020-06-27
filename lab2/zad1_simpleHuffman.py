import heapq 
import math
import os.path
import sys

class Node:
    def __init__(self, char='--', left=None, right=None, probability=0):
        self.left = left
        self.right = right
        self.char = char
        self.probability = probability

    def __lt__(self,other):
        return self.probability < other.probability

    def search(self,value):
        if(self.char == value):
            return ''
        if self.left:
            v = self.left.search(value)
            if v != None:
                return '0' + v         
        if self.right:
            v = self.right.search(value)
            if v != None:
                return  '1' + v

    def printTree(self, level=0):
        print('\t' * level, end="")
        print(f'{self.char}:{self.probability}')
        if self.left:
            self.left.printTree(level+1)
        if self.right:
            self.right.printTree(level+1)


def build_tree(source, f) :
    letters = {}
    all_bytes = 0
    byte = f.read(1)
    while byte:
        if byte in letters:
            letters[byte] += 1
        else:
            letters[byte] = 1
        all_bytes += 1
        byte = f.read(1)

    nodes = []
    heapq.heapify(nodes)
    for char, apperance in letters.items():
        new_node = Node(char=char, probability=apperance/all_bytes)
        heapq.heappush(nodes,new_node)
     
    while len(nodes) > 1:
        node1 = heapq.heappop(nodes) 
        node2 = heapq.heappop(nodes)
        probability_sum = node1.probability + node2.probability
        new_node = Node(left=node1, right=node2, probability=probability_sum)
        heapq.heappush(nodes, new_node)

    return nodes[0], letters, all_bytes

def encode(tree, r, w):
    source_size = 0
    compressed_size = 0
    result = '11111111'
    byte = r.read(1)
    while byte:
        code = tree.search(byte)
        result += code
        compressed_size += len(code) # in bits
        source_size += 1 # in bytes
        byte = r.read(1)
    source_size *= 8 # in bits
    r = int(result, 2).to_bytes((len(result) + 7) // 8 , 'big')
    w.write(r)
    if compressed_size != 0:
        return source_size / compressed_size
    else:
        return source_size

def decode(tree, f, w):
    byte = f.read()
    byte_string = bin(int.from_bytes(byte, "big"))[10:]
    current_node = tree
    for bit in byte_string:
        if bit == '1':
            current_node = current_node.right
        else:
            current_node = current_node.left
        if current_node.char != '--':
            w.write(current_node.char)
            current_node = tree

if __name__== "__main__":
    filename_source = sys.argv[1]
    filename_target = "encoded.bin"
    filename_decoded = "decoded.bin"

    with open(filename_source,'rb') as f:
            tree, letters, all_bytes = build_tree(filename_source,f)
    with open(filename_source, 'rb') as r:
        with open(filename_target, 'wb') as w:
            compression_rate = encode(tree, r, w)
    with open(filename_target, 'rb') as f:
        with open(filename_decoded, 'wb') as w:           
            decode(tree, f, w)


    print(f'Compression rate {compression_rate}') # = 8/average code length

    average_code_length = 0
    for char in letters:
        code = len(tree.search(char))
        average_code_length += code * letters[char] / all_bytes   
    print(f'Average code length {average_code_length}')

    entropy = 0
    for char in letters:
        p = letters[char] / all_bytes  
        entropy -= p * math.log2(p)
    print(f'Entropy {entropy}') # optimal coding should have entropy = average code length
    

    