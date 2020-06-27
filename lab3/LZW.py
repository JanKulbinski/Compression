import math
import io
import sys

def encode(file_to_code, target, coder):
    # statistics
    bytes_in_file_to_encode = 1
    letters_in_file_to_encode = {}

    table = get_all_possible_characters()
    result = '1'
    with open(file_to_code, "rb") as f:
        p = f.read(1)
        letters_in_file_to_encode[p] = 1
        c = f.read(1)
        while c:
            #statistics
            bytes_in_file_to_encode += 1
            if c in letters_in_file_to_encode:
                letters_in_file_to_encode[c] += 1
            else:
                letters_in_file_to_encode[c] = 1

            concat = p + c
            if concat in table:
                p = concat
            else:
                result += coder.encode_int(table[p])
                table[concat] = len(table) + 1
                p = c
            c = f.read(1)
        result += coder.encode_int(table[p])

    with open(target, "wb") as t:
        t.write(int(result,2).to_bytes((int(result, 2).bit_length() + 7 )// 8,"big"))

    return bytes_in_file_to_encode, letters_in_file_to_encode


def decode(encoded_file, target, coder):
    bytes_in_file_to_decode = 0

    table = get_all_possible_characters()    
    with open(encoded_file, "rb") as f:
        data = f.read()
        bits = str(bin(int.from_bytes(data,"big")))[3:]
        bytes_in_file_to_decode = (len(bits)+7) // 8 

        with open(target, "wb") as t:
            bits, pk = coder.decode_bin(bits)
            t.write(key_from_value(table,pk))

            while bits:
                bits, k = coder.decode_bin(bits)
                pc = key_from_value(table,pk)
                from_k = key_from_value(table,k)
                if from_k and from_k in table:
                    table[pc + from_k[0:1]] = (len(table) + 1)
                    t.write(from_k)
                else:
                    table[pc + pc[0:1]] = (len(table) + 1)
                    t.write(pc + pc[0:1])
                pk = k
    return bytes_in_file_to_decode


def key_from_value(table, value):
    if len(table) > value - 1:
        return list(table.keys())[value - 1]
    else:
        return None


def get_all_possible_characters():
    table = {}
    for i in range(256):
        table[i.to_bytes(1, byteorder='big')] = len(table) + 1
    return table


def apperances(file):
    letters_in_file_to_decode = {}
    with open(file, "rb") as f:
        byte = f.read(1)
        while byte:
            if byte in letters_in_file_to_decode:
                letters_in_file_to_decode[byte] += 1
            else:
                letters_in_file_to_decode[byte] = 1 
            byte = f.read(1)
    return letters_in_file_to_decode


class Eliash_Gamma:
    def encode_int(self, value):
        binary = bin(value)[2:]
        length = value.bit_length()
        return '0' * (length-1) + binary
    def decode_bin(self, binary):
        number_length = 0
        for bit in binary:
            if bit == '1':
                break
            else:
                number_length += 1
        binary = binary[number_length + 1:]
        result = 2 ** number_length
        number_length -= 1
        while number_length >= 0:
            result += int(binary[0]) * (2 ** number_length)
            binary = binary[1:]
            number_length -= 1
        return binary, result


class Eliash_Delta:
    def __init__(self):
        self.coder_gamma = Eliash_Gamma()
    def encode_int(self, value):
        binary = bin(value)[3:]
        length = value.bit_length()
        length = self.coder_gamma.encode_int(length)
        return length + binary
    def decode_bin(self, binary):
        binary, value = self.coder_gamma.decode_bin(binary)
        value -= 1
        result = 2 ** value
        value -= 1
        while value >= 0:
            result += int(binary[0]) * (2 ** value)
            binary = binary[1:]
            value -= 1
        return binary, result


class Eliash_Omega:
    def encode_int(self,value):
        result = '0'
        k = value
        while k > 1:
            binary = bin(k)[2:]
            result = binary + result
            k = len(binary) - 1
        return result
    def decode_bin(self, binary):
        n = 1
        bit = binary[0]
        while bit != '0':
            old_n = n
            n = int(binary[:n+1], 2)
            binary = binary[old_n + 1:]
            bit = binary[0]
        binary = binary[1:]
        return binary, n


class Fibbonaci:
    def __init__(self):
        self.fib = {1: 1, 2: 2}

    def get_fibo(self, number):
        if number not in self.fib:
            self.fib[number] = self.get_fibo(number-1) + self.get_fibo(number-2)
        return self.fib[number]

    def encode_int(self,value):
        less_or_equal = 0
        fib_key = 1
        while True:
            fib_value = self.get_fibo(fib_key)
            if value < fib_value:
                less_or_equal = fib_key - 1
                break
            elif value == fib_value: 
                less_or_equal = fib_key
                break
            fib_key += 1    
        result = '1'
        while less_or_equal >= 1:
            if self.fib[less_or_equal] > value:
                result = '0' + result
            else:
                result = '1' + result
                value -= self.fib[less_or_equal]
            less_or_equal -= 1 
        return result

    def decode_bin(self, binary):
        previous_bit = 0
        length = 0
        result = 0
        for bit in binary:
            bit = int(bit)
            length += 1
            if bit and previous_bit:
                break
            else:
               result += bit * self.get_fibo(length)
            previous_bit = bit   
        return binary[length:], result


if __name__ == "__main__":
    filename_source = sys.argv[1]
    coding = ''
    if len(sys.argv) == 3:
        coding = sys.argv[2]
    filename_target = 'encoded.bin'
    filename_decoded = 'decoded.bin'

    coder = None
    if coding == 'eg':
        coder = Eliash_Gamma()
    elif coding == 'ed':
        coder = Eliash_Delta()
    elif coding == 'eo':
        coder = Eliash_Omega()
    elif coding == 'fb':
        coder = Fibbonaci()
    else:
        coder = Eliash_Omega()
    bytes_in_file_to_encode, letters_in_file_to_encode = encode(filename_source, filename_target, coder)
    bytes_in_file_to_decode  = decode(filename_target, filename_decoded, coder)
    letters_in_file_to_decode = apperances(filename_target)

    print(f'Length of the file to encode: {bytes_in_file_to_encode} B')
    print(f'Length of the encoded file: {bytes_in_file_to_decode} B')
    print(f'Compression rate: {bytes_in_file_to_encode / bytes_in_file_to_decode }')

    entropy = 0
    for char in letters_in_file_to_encode:
        p = letters_in_file_to_encode[char] / bytes_in_file_to_encode
        entropy -= p * math.log2(p)
    print(f'Entropy in file to encode: {entropy}')

    entropy = 0
    for char in letters_in_file_to_decode:
        p = letters_in_file_to_decode[char] / bytes_in_file_to_decode
        entropy -= p * math.log2(p)
    print(f'Entropy in encoded file: {entropy}')
