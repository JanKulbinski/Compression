import math
import sys

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Result:
    def __init__(self, matrix, inaccurancy, snr):
        self.matrix = matrix
        self.inaccuracy = inaccurancy
        self.snr = snr

def readFile(name):
    with open(name, "rb") as file:
        header = file.read(18)
        header_list = list(header)
        width = header_list[13] * (2**8) + header_list[12]
        height = header_list[15] * (2**8) + header_list[14]
        
        matrixRed = [[0 for x in range(width)] for y in range(height)] 
        matrixGreen = [[0 for x in range(width)] for y in range(height)] 
        matrixBlue = [[0 for x in range(width)] for y in range(height)] 

        image = list(file.read(width * height * 3))
        reds = [byte for index, byte in enumerate(image) if index % 3 == 2]
        green = [byte for index, byte in enumerate(image) if index % 3 == 1]
        blue = [byte for index, byte in enumerate(image) if index % 3 == 0]
        
        for index, byte in enumerate(reds):
            matrixRed[index // width][index % width] = byte
        for index, byte in enumerate(green):
            matrixGreen[index // width][index % width] = byte
        for index, byte in enumerate(blue):
            matrixBlue[index // width][index % width] = byte

        footer = file.read(26)
    return matrixRed, matrixGreen, matrixBlue, header, footer

def quantization(matrix, bits):
    height = len(matrix)
    width = len(matrix[0])
    interval = 2 ** (8-bits)
    result =  [[0 for x in range(width)] for y in range(height)]
    inaccuracy = []
    snr = []

    for y in range(height):
        for x in range(width):
            result[y][x] = (matrix[y][x] // interval) * interval + (interval // 2)
            inaccuracy.append((result[y][x] - matrix[y][x]) ** 2)
            snr.append(matrix[y][x] ** 2)
    return Result(result, inaccuracy, snr)

def writeToFile(matrixRed, matrixGreen, matrixBlue, file_name, header, footer):
    height = len(matrixRed)
    width = len(matrixRed[0])
    with open(file_name, "wb") as file:
        file.write(header)

        for y in range(height):
            for x in range(3 * width):
                if x % 3 == 0:
                    file.write(bytes([matrixBlue[y][x // 3]]))
                elif x % 3 == 1:
                    file.write(bytes([matrixGreen[y][x // 3]]))
                else:
                    file.write(bytes([matrixRed[y][x // 3]]))
        file.write(footer)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("5 parameters required")
        sys.exit()

    filename_source = sys.argv[1]
    filename_target = sys.argv[2]
    bitsforRed = int(sys.argv[3])
    bitsForGreen = int(sys.argv[4])
    bitsForBlue = int(sys.argv[5])

    matrixRed, matrixGreen, matrixBlue, header, footer = readFile(filename_source)
    
    red = quantization(matrixRed, bitsforRed)
    green = quantization(matrixGreen, bitsForGreen)
    blue = quantization(matrixBlue, bitsForBlue)
    writeToFile(red.matrix, green.matrix, blue.matrix, filename_target, header, footer)

    inaccuracy =  red.inaccuracy + green.inaccuracy + blue.inaccuracy
    mse = sum(inaccuracy)/len(inaccuracy)
    mser = sum(red.inaccuracy)/len(red.inaccuracy)
    mseg = sum(green.inaccuracy)/len(green.inaccuracy)
    mseb = sum(blue.inaccuracy)/len(blue.inaccuracy)
    print(f'mse   ={bcolors.WARNING}{mse:.6f}{bcolors.ENDC}')
    print(f'mse(r)={bcolors.FAIL}{mser:.6f}{bcolors.ENDC}')
    print(f'mse(g)={bcolors.OKGREEN}{mseg:.6f}{bcolors.ENDC}')
    print(f'mse(b)={bcolors.OKBLUE}{mseb:.6f}{bcolors.ENDC}\n')

    if(mse and mser and mseg and mseb):
        snr = red.snr + green.snr + blue.snr
        snr = (sum(snr)/len(snr)) / mse
        snrr = (sum(red.snr)/len(red.snr)) / mser
        snrg = (sum(green.snr)/len(green.snr)) / mseg
        snrb = (sum(blue.snr)/len(blue.snr)) / mseb
        print(f'snr   ={bcolors.WARNING}{snr:.6f} ({10 * math.log10(snr):.6f} dB) {bcolors.ENDC}')
        print(f'snr(r)={bcolors.FAIL}{snrr:.6f} ({10 * math.log10(snrr):.6f} dB) {bcolors.ENDC}')
        print(f'snr(g)={bcolors.OKGREEN}{snrg:.6f} ({10 * math.log10(snrg):.6f} dB) {bcolors.ENDC}')
        print(f'snr(b)={bcolors.OKBLUE}{snrb:.6f} ({10 * math.log10(snrb):.6f} dB) {bcolors.ENDC}')
    else:
        print("Cant calculate snr when one of mse is 0")