import random
import sys
from struct import pack

SYMBOL_COUNT = 256
ROTORS_COUNT = 3
BUF_SIZE = 512

class Rotor:
    def __init__(self):
        self.__offset = 0
        self.full_cycle = False
        #self.alphabet = [chr(i) for i in range(SYMBOL_COUNT)]
        self.routes = list(range(SYMBOL_COUNT))
        self.initial_routes = self.routes
        random.shuffle(self.routes)
        
    def reset(self):
        self.__offset = 0
        self.routes = self.initial_routes
        
    def __str__(self):
        s = ''
        for i in range(SYMBOL_COUNT):
            s += '%i => %i\n' % (i, self.routes[i])
        return s
		   
    def forward(self, index):
        return self.routes[index]
	
    def backwards(self, index):
        return self.routes.index(index)
		
    def rotate(self):
        self.routes = self.routes[1:] + self.routes[:1]
        self.__offset += 1
        if self.__offset == SYMBOL_COUNT:
            self.__offset = 0
            self.full_cycle = True
        else:
            self.full_cycle = False
	   
class Reflector:
    def __init__(self):
        self.routes = [0] * SYMBOL_COUNT
        first_half = []
        if SYMBOL_COUNT % 2:
            first_half = list(range(SYMBOL_COUNT // 2 + 1, SYMBOL_COUNT))
            random.shuffle(first_half)
            self.routes[:SYMBOL_COUNT // 2] = first_half
            self.routes[SYMBOL_COUNT // 2] = SYMBOL_COUNT // 2
        else:
            first_half = list(range(SYMBOL_COUNT // 2, SYMBOL_COUNT))
            random.shuffle(first_half)
            self.routes[:SYMBOL_COUNT // 2] = first_half
        
        n = len(first_half)
        for i in range(n):
           self.routes[first_half[i]] = i
     
    def __str__(self):
        s = ''
        for i in range(SYMBOL_COUNT):
            s += '%i => %i\n' % (i, self.routes[i])
        return s
		   
    def reflect(self, index):
        return self.routes[index]
 
class Enigma:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector
        
    def reset(self):
        for rotor in self.rotors:
            rotor.reset()  
            
    def __str__(self):
        s = ''
        i = 0
        for rotor in self.rotors:
            s += 'Rotor[%i]:\n' % (i)
            s += rotor.__str__()
            i += 1

        s += "Reflector:\n" + self.reflector.__str__()
        return s
               
    def encrypt(self, symbol):
        encrypted = symbol
        n = len(self.rotors)
        
        for rotor in self.rotors:
            encrypted = rotor.forward(encrypted)
        
        encrypted = self.reflector.reflect(encrypted)   
        
        for rotor in self.rotors[::-1]:
            encrypted = rotor.backwards(encrypted)
            
        self.rotors[0].rotate()
        for i in range(1, n):
            if self.rotors[i - 1].full_cycle:
                self.rotors[i].rotate()
                
        return encrypted
        
    def encrypt_data(self, data):
        encrypted_data = b''
        for symbol in data:
            encrypted = self.encrypt(symbol)
            encrypted_data += pack("B", encrypted)
        return encrypted_data
        
def main():
    try:
        data = open(sys.argv[1], "rb")
    except IndexError:
        print("Error with open")
        return
        
    rotors = [0] * ROTORS_COUNT
    
    for i in range(ROTORS_COUNT):
        rotors[i] = Rotor()
        
    reflector = Reflector()
    enigma = Enigma(rotors, reflector)
  
    enc_file = open("enc_" + sys.argv[1], "wb")
        
    lines = data.read()
    data.close()
    encrypted_data = enigma.encrypt_data(lines)
    enc_file.write(encrypted_data)
    enc_file.close()
    
    data_str = 'Input data:%s\n' % (lines)
    print(data_str)
    
    enc_str = 'Encrypted:%s\n' % (encrypted_data)
    print(enc_str)
    
    enc_file = open("enc_" + sys.argv[1], "rb")
    dec_file = open("dec_" + sys.argv[1], "wb")
    
    enigma.reset()
    
    lines = enc_file.read()
    enc_file.close()
    decrypted_data = enigma.encrypt_data(lines)
    dec_file.write(decrypted_data)
    dec_file.close()
    
    dec_str = 'Decrypted:%s\n' % (decrypted_data)
    print(dec_str)
    
if __name__ == "__main__":
    main()
