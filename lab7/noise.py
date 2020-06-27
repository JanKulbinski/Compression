from sys import argv
import sys
import random

def readFile(name):
    with open(name, "rb") as file:
        byte = file.read()
        bits = str(bin(int.from_bytes(byte,"big")))[2:]
        front = '0'*((8 - (len(bits) % 8)) % 8)
    return front + bits


if __name__ == "__main__":
    if len(argv) != 4:
        print("3 parameters required")
        sys.exit()

    probability = float(argv[1])
    source_file = argv[2]
    output_file = argv[3]
    random.seed()
    
    bits = list(readFile(source_file))
    for index, value in enumerate(bits):
        if random.uniform(0, 1) < probability:
            if value == '1':
                bits[index] = '0'
            else:
                bits[index] = '1'
    bits = "".join(bits)
    bits = int(bits, 2).to_bytes(len(bits) // 8, byteorder='big')
    with open(output_file, "wb") as file:
        file.write(bits)  

