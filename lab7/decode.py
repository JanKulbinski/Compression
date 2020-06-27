from sys import argv
import sys

codes = [
    "00000000",
    "11010010",
    "01010101",
    "10000111",
    "10011001",
    "01001011",
    "11001100",
    "00011110",
    "11100001",
    "00110011",
    "10110100",
    "01100110",
    "01111000",
    "10101010",
    "00101101",
    "11111111",
]

def readFile(name):
    with open(name, "rb") as file:
        byte = file.read()
        bits = str(bin(int.from_bytes(byte,"big")))[2:]
        front = '0'*((8 - (len(bits) % 8)) % 8)
    return front + bits

def decodeHamming(message):
    if message in codes:
        return message[2] + message[4:7], 0

    for code in codes:
        diffs = len([1 for i in range(len(message)) if message[i] != code[i]])
        if diffs == 1:
            return code[2] + code[4:7], 0
        elif diffs == 2:
            return "0000", 1
    return "0000", 0

if __name__ == "__main__":
    if len(argv) != 3:
        print("2 parameters required")
        sys.exit()
    
    source_file = argv[1]
    output_file = argv[2]
    bits = readFile(source_file)
    results = ""
    errors = 0

    for index in range(0, len(bits), 8):
        message = bits[index:(index+8)]
        result, error = decodeHamming(message) 
        results += result
        errors += error

    results = int(results, 2).to_bytes(((int(results, 2).bit_length() + 7) // 8), byteorder='big')
    print(f'Double errors: {errors}') 
    with open(output_file, "wb") as file:
        file.write(results)  