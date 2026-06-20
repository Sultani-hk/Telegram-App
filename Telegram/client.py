from socket import * 
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad



#-------------------------------------------------------------------Encryption and Decryption 

def encrypt_message(message):
    """
    Encrypt a string and return IV + ciphertext.
    """
    cipher = AES.new(KEY, AES.MODE_CBC)

    ciphertext = cipher.encrypt(
        pad(message.encode(), AES.block_size)
    )

    return cipher.iv + ciphertext


def decrypt_message(data):
    """
    Decrypt IV + ciphertext and return the original string.
    """
    iv = data[:16]          # First 16 bytes are the IV
    ciphertext = data[16:]  # The rest is the encrypted message

    cipher = AES.new(KEY, AES.MODE_CBC, iv)

    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return plaintext.decode()

#-------------------------------------------------------------------------------------

connect = socket(AF_INET,SOCK_STREAM)

try:
    connect.connect(("192.168.43.1",1234))
#-----------------------------------------------------key Exchange : ChatGPT
    key_size = int.from_bytes(connect.recv(4),"big")
    KEY = b""
    while len(KEY) < key_size:
        KEY += connect.recv(key_size - len(KEY))

    connect.send(b"OK")
#-----------------------------------------------------------

    data = decrypt_message(connect.recv(1254))
    msg = input(data)
    msg = encrypt_message(msg)
    connect.sendall(msg)


    data = decrypt_message(connect.recv(1254))
    passwd = input(data)
    passwd = encrypt_message(passwd)
    connect.sendall(passwd)

    data = decrypt_message(connect.recv(1254))
    print(data)

    msg = input("Alice : ")
    msg = encrypt_message(msg)
    connect.sendall(msg)
    while True:
        data = decrypt_message(connect.recv(1254))
        print("msg > ",data)
        msg = input("Alice > ")
        msg =encrypt_message(msg)
        connect.sendall(msg)

except:
    connect.close()