import math 

def read_file(filename) :
    appearances = {}
    succeedings = {}

    with open(filename, 'rb') as f:

        byte = f.read(1)
        if byte :
            appearances[b'\x00'] = 0
            appearances[byte] = 1
            succeedings[b'\x00'] = {byte : 1}
            succeedings[byte] = {}
            previous = byte
            numberOfBytes = 1

        while byte:
            byte = f.read(1)
            if not byte:
                break

            if byte in appearances :
                appearances[byte] += 1
            else :
                appearances[byte] = 1
                succeedings[byte] = {}

            if byte in succeedings[previous] :
                succeedings[previous][byte] += 1
            else :
                succeedings[previous][byte] = 1 
            
            previous = byte
            numberOfBytes += 1

    return appearances,succeedings, numberOfBytes

def compute(appearances, succeedings, numberOfBytes):
    result = 0
    result2 = 0
    sumAll = 0
    for char in appearances.keys():
        if not appearances[char] == 0:
            result += appearances[char] * (math.log2(numberOfBytes) - math.log2(appearances[char]) )

        sum = 0
        for _ , b in succeedings[char].items():
            sum += b

        h = 0
        for _ , b in succeedings[char].items():
            h += b * (math.log2(sum) - math.log2(b))
        
        result2 += h
        sumAll += sum
    return result/numberOfBytes, result2/sumAll

if __name__== "__main__":
    #filename = input("Enter file name:\n")
    #r1, r2,numberOfBytes = read_file(filename)
    #r1, r2, numberOfBytes = read_file('pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt')
    r1, r2, numberOfBytes = read_file('test3.bin')
    result1, result2 = compute(r1, r2, numberOfBytes)
    print(result1)
    print(result2)
    print(result2 - result1)
