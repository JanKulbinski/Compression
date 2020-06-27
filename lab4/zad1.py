import math
import copy
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def readFile(name):
    with open(name, "rb") as file:
        header = list(file.read(18))
        width = header[13] * (2**8) + header[12]
        height = header[15] * (2**8) + header[14]
        
        matrixRed = [[0 for x in range(width+2)] for y in range(height+2)] 
        matrixGreen = [[0 for x in range(width+2)] for y in range(height+2)] 
        matrixBlue = [[0 for x in range(width+2)] for y in range(height+2)] 

        image = list(file.read(width * height * 3))
        reds = [byte for index, byte in enumerate(image) if index % 3 == 2]
        green = [byte for index, byte in enumerate(image) if index % 3 == 1]
        blue = [byte for index, byte in enumerate(image) if index % 3 == 0]
        
        for index, byte in enumerate(reds):
            matrixRed[1 + (index // width)][1 + (index % width)] = byte
        for index, byte in enumerate(green):
            matrixGreen[1 + (index // width)][1 + (index % width)] = byte
        for index, byte in enumerate(blue):
            matrixBlue[1 + (index // width)][1 + (index % width)] = byte

    return matrixRed, matrixGreen, matrixBlue, width, height


def getEntropy(matrixRed, matrixGreen, matrixBlue, width, height):

    def getEntropyOneColor(matrix):
        stats = [0 for x in range(0,256)]
        for x in range(1, width+1):
            for y in range(1, height+1):
                stats[matrix[y][x]] += 1
        return stats

    redStats = getEntropyOneColor(matrixRed)
    greenStats = getEntropyOneColor(matrixGreen)
    blueStats = getEntropyOneColor(matrixBlue)
    allStats = [0 for x in range(0,256)]

    for index, value in enumerate(redStats):
        allStats[index] = value + greenStats[index] + blueStats[index]

    def calculateEntropy(stats, ifAllStats=1):
        entropy = 0
        for value in stats:
            if value == 0:
                continue 
            p = value / (width*height*ifAllStats)
            entropy -= p * math.log2(p)
        return entropy

    return calculateEntropy(redStats), calculateEntropy(greenStats), calculateEntropy(blueStats), calculateEntropy(allStats, 3)


def jpegLs(matrix, width, height, method):
    result =  [[0 for x in range(width+2)] for y in range(height+2)]  
    for y in range(1, height+1):
        for x in range(1, width+1):
            n = matrix[y - 1][x]
            w = matrix[y][x - 1]
            nw = matrix[y - 1][x - 1]
            result[y][x] = ((matrix[y][x] - method(n, w, nw)) % 256)
    return result


def newStandard(n, w, nw):
    if nw >= max(w,n):
        return max(w,n) % 256
    elif nw <= min(w, n):
        return min(w,n) % 256
    else:
        return (n + w - nw) % 256

def standard1(n, w, nw):
    return w

def standard2(n, w, nw):
    return n

def standard3(n, w, nw):
    return nw

def standard4(n, w, nw):
    return (n + w - nw) % 256

def standard5(n, w, nw):
    return (n + (w - nw)//2) % 256

def standard6(n, w, nw):
    return (n + (nw - w)//2) % 256

def standard7(n, w, nw):
    return ((n + w)//2) % 256  

if __name__ == "__main__":

    filename_source = sys.argv[1]
    matrixRed, matrixGreen, matrixBlue, width, height = readFile(filename_source)
    red, green, blue, whole = getEntropy(matrixRed, matrixGreen, matrixBlue, width, height)
    print(f'{bcolors.WARNING}Begin entropy:{bcolors.ENDC} Red={red} Green={green} Blue={blue} ALL={whole}')

    methods = [standard1,standard2,standard3,standard4,standard5,standard6,standard7,newStandard]
    redEntropy = []
    greenEntropy = []
    blueEntropy = []
    allEntropy = []
    for method in methods:
        r = jpegLs(matrixRed, width, height, method)
        g = jpegLs(matrixGreen, width, height, method)
        b = jpegLs(matrixBlue, width, height, method)
        re, ge, be, we = getEntropy(r, g, b, width, height)
        redEntropy.append(re)
        greenEntropy.append(ge)
        blueEntropy.append(be)
        allEntropy.append(we)
        print(f'{bcolors.WARNING}{method.__name__} entropy:{bcolors.ENDC} Red={re} Green={ge} Blue={be} ALL={we}')

    print(f'{bcolors.FAIL }Best for red entropy: {min(redEntropy)}  --> {methods[redEntropy.index(min(redEntropy))].__name__}{bcolors.ENDC}')
    print(f'{bcolors.OKGREEN }Best for green entropy: {min(greenEntropy)}  --> {methods[greenEntropy.index(min(greenEntropy))].__name__}{bcolors.ENDC}')
    print(f'{bcolors.OKBLUE }Best for blue entropy: {min(blueEntropy)}  --> {methods[blueEntropy.index(min(blueEntropy))].__name__}{bcolors.ENDC}')
    print(f'{bcolors.UNDERLINE }Best for all entropy: {min(allEntropy)}  --> {methods[allEntropy.index(min(allEntropy))].__name__} {bcolors.ENDC}')

