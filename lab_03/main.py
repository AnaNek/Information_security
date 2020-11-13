import os
import time
import aes
import sys
    
def main():
    try:
        f = open(sys.argv[1], "rb")
        key = sys.argv[2]
        if len(key) > 16:
            print('Too long Key. Imagine another one')
            return
        
        for symbol in key:
            if ord(symbol) > 0xff:
                print('That key won\'t work. Try another using only latin alphabet and numbers')
                return
    except IndexError:
        print("Error")
        return
          
    enc_file = open("enc_" + sys.argv[1], "wb")
        
    data = f.read()
    f.close()
    
    encrypted_data = []
    temp = []
    for byte in data:
        temp.append(byte)
        if len(temp) == 16:
             print(temp)
             encrypted_part = aes.encrypt(temp, key)
             encrypted_data.extend(encrypted_part)
             temp = []
             
    n = len(temp)
    if 0 < n < 16:
        empty_spaces = 16 - n
        for i in range(empty_spaces - 1):
            temp.append(0)
        temp.append(1)
        print(temp)
        encrypted_part = aes.encrypt(temp, key)
        encrypted_data.extend(encrypted_part)
                
    enc_file.write(bytes(encrypted_data))
    enc_file.close()
    
    data_str = 'Input data:%s\n' % (data)
    print(data_str)
    
    enc_str = 'Encrypted:%s\n' % (encrypted_data)
    print(enc_str)
    
    enc_file = open("enc_" + sys.argv[1], "rb")
    dec_file = open("dec_" + sys.argv[1], "wb")
    
    data = enc_file.read()
    enc_file.close()
    
    decrypted_data = []
    temp = []
    for byte in data:
        temp.append(byte)
        if len(temp) == 16:
             decrypted_part = aes.decrypt(temp, key)
             decrypted_data.extend(decrypted_part)
             temp = []
             
    n = len(temp)
    if 0 < n < 16:
        empty_spaces = 16 - n
        for i in range(empty_spaces - 1):
            temp.append(0)
        temp.append(1)
        decrypted_part = aes.decrypt(temp, key)
        decrypted_data.extend(decrypted_part)
        
    dec_file.write(bytes(decrypted_data))
    dec_file.close()
    
    dec_str = 'Decrypted:%s\n' % (decrypted_data)
    print(dec_str)
    
if __name__ == '__main__':
    main()
