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
    if len(argv) != 3:
        print("2 parameters required")
        sys.exit()

    source_file = argv[1]
    source_file2 = argv[2]

    bits = readFile(source_file)
    bits2 = readFile(source_file2)

    length = min(len(bits), len(bits2))
    diffs = len([1 for i in range(0, length, 4) if bits[i:i+4] != bits2[i:i+4]])
    print(f'Diffs: {diffs + abs(len(bits) - len(bits2)) // 4}')