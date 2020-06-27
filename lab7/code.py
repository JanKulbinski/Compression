from sys import argv
import sys

def readFile(name):
    with open(name, "rb") as file:
        byte = file.read()
        bits = str(bin(int.from_bytes(byte,"big")))[2:]
        front = '0'*((8 - (len(bits) % 8)) % 8)
    return front + bits

def codeHamming(bits):
    p1 = (int(bits[0]) + int(bits[1]) + int(bits[3])) % 2
    p2 = (int(bits[0]) + int(bits[2]) + int(bits[3])) % 2
    p3 = (int(bits[1]) + int(bits[2]) + int(bits[3])) % 2
    p4 = (p1 + p2 + p3 + len([1 for i in bits if i == "1"])) % 2
    return str(p1) + str(p2) + bits[0] + str(p3) + bits[1:] + str(p4)

if __name__ == "__main__":
    if len(argv) != 3:
        print("2 parameters required")
        sys.exit()
    source_file = argv[1]
    output_file = argv[2]

    bits = readFile(source_file)
    result = ""
    for index in range(0, len(bits), 4):
        message = bits[index:(index+4)]
        result += codeHamming(message)

    result = int(result, 2).to_bytes(len(result) // 8, byteorder='big')    
    with open(output_file, "wb") as file:
        file.write(result)    