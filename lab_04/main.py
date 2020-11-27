import sys
from base64 import *
from random import randrange, randint

limit_primes = 150

class RSA:
    def __init__(self, n):           
        self.primes = self.sieveOfEratosthenes(n)
        self.rand_i = randint(len(self.primes) // 2, len(self.primes) - 1)
        self.rand_j = randint(len(self.primes) // 2, len(self.primes) - 1) 
        self.p = self.primes[self.rand_i]
        self.q = self.primes[self.rand_j]
        self.n = self.p * self.q               # мощность алфавита
        self.phi = (self.p - 1) * (self.q - 1) # функция Эйлера
        self.e = self.chooseE(self.phi)
        self.d = self.getD(self.e, self.phi)
            
    def crypt(self, char, key):
        return char ** key % self.n

    def encrypt_string(self, string):
        result = ""
        for char in string:
            current_char = self.crypt(ord(char), self.e)
            result += chr(current_char)
        return result

    def decrypt_string(self, string):
        result = ""
        for char in string:
            current_char = self.crypt(ord(char), self.d)
            result += chr(current_char)
        return result

    # решето Эратосфена
    def sieveOfEratosthenes(self, n): 
        prime = [True for i in range(n + 1)] 
        p = 2
        while (p * p <= n):      
            if (prime[p] == True):  
                for i in range(p * 2, n + 1, p): 
                    prime[i] = False
            p += 1
        prime[0]= False # 0 не простое число
        prime[1]= False # 1 не простое число
    
        primes = []
        for p in range(n + 1): 
            if prime[p]: 
                primes.append(p)
            
        return primes
      
    # расширенный алгоритм Евклида
    def xgcd(self, a, b):
        x, old_x = 0, 1
        y, old_y = 1, 0

        while (b != 0):
            quotient = a // b
            a, b = b, a - quotient * b
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return a, old_x, old_y
    
    def getD(self, e, phi):
        gcd, x, y = self.xgcd(e, phi)

        if (x < 0):
            d = x + phi
        else:
            d = x
            
        return d
  
    # алгоритм Евклида
    def gcd(self, a, b):
        if (b == 0):
            return a
        else:
            return self.gcd(b, a % b)
            
    def chooseE(self, phi):
        while (True):
            e = randrange(2, phi)

            if (self.gcd(e, phi) == 1):
                return e

def main():
    if len(sys.argv) < 2:
        print("Usage: python3", sys.argv[0], "<filename>")
        return -1

    filename = sys.argv[1]
    with open(filename, 'rb') as input_file:
        data = input_file.read()
        rsa = RSA(limit_primes)
        #print("RSA parametrs\np:", rsa.p, "\nq:", rsa.q, "\ne:", rsa.e, "\nN:", rsa.n, "\nd:", rsa.d)

        source_str = b32encode(data)
        decoded_str = source_str.decode("ascii")
        #print("Encrypting...")

        encrypted = rsa.encrypt_string(decoded_str)
        with open("enc_" + filename, "w") as encrypted_file:
            encrypted_file.write(encrypted)
            encrypted_file.close()
        #print("Decrypting...")

        decrypted = rsa.decrypt_string(encrypted)
        decrypted = b32decode(decrypted)
        with open("dec_" + filename, "wb") as decrypted_file:
            decrypted_file.write(decrypted)
            decrypted_file.close()
    return 0
if __name__ == '__main__':
    main()

    
