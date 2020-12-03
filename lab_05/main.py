import rsa
import sys
import os
from Cryptodome.Hash import SHA256

# хеш в виде мссива байтов
def hash_file(filename):
    h = SHA256.new()
    with open(filename, "rb") as f:
        data = f.read()
        h.update(data)
    return h.digest() 

# запись электронной подписи в файл
def make_signature(filename, key):
   
    # считаем хеш файла
    h = hash_file(filename)

    # шифруем хеш закрытым ключом
    signature = rsa.encrypt(h, key)

    # записываем электронную подпись в файл
    signature_file_name = "signature"
    with open(signature_file_name, "wb") as f:
        f.write(signature)

    print("File with digital signature '{0}'".format(signature_file_name))

    return signature_file_name

# проверка электронной подписи
def check_signature(message_file, signature_file ,key):
    # считаем хеш файла с сообщением
    h1 = hash_file(message_file)

    # расшифровываем ЭП
    signature = None
    with open(signature_file, "rb") as f:
        signature = f.read()

    try:
        h2 = rsa.decrypt(signature, key)
    except rsa.pkcs1.DecryptionError:
        return False

    return (h1 == h2)

def get_keys():
    (privkey, pubkey) = rsa.newkeys(2048)
    public_key = 'public.pem'
    with open(public_key, "wb") as pub:
        pub.write(pubkey.save_pkcs1('PEM'))
        
    print("File with public key '{0}'".format(public_key))
    return (privkey, pubkey)
    
def main():
    try:
        message_file = sys.argv[1]
    except IndexError:
        print("Usage: python3 ", sys.argv[0], " <filename>")
        return

    if not os.path.exists(message_file):
        print("File is not exist")
        return

    (privkey, pubkey) = get_keys()
    signature_file = make_signature(message_file, privkey)
    
    fsign = input("Input file with signature:")
    fpubkey = input("Input file with public key:")
    fdata = input("Input file to sign:")

    with open(fpubkey, "rb") as k:
        public_key_data = k.read()
        
    public_key = rsa.PrivateKey.load_pkcs1(public_key_data, format='PEM')
    
    is_valid = check_signature(fdata, fsign, public_key)

    if is_valid:
        print("SUCCESS. Sign is correct")
    else:
        print("FAIL. Sign is incorrect")
    

if __name__ == '__main__':
    main()
