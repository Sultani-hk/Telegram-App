from socket import * 
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

#--------------------------------------------------------------------Encryption and Decryption Methodes : 

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

#-----------------------------------------------------------------------

server = socket(AF_INET,SOCK_STREAM)

try:
    server.bind(("192.168.43.1",1234))


    server.listen(2)

    client,address = server.accept()

#---------------------------------------------key Exchanging : ChatGPT
    KEY = get_random_bytes(32)
    client.send(len(KEY).to_bytes(4,"big"))
    client.sendall(KEY)

    client.recv(2)


#-----------------------------------------------------------------
    

    msg = "Username : "
    msg = encrypt_message(msg)
    client.sendall(msg)

    Username = client.recv(1254)
    Username = decrypt_message(Username)

    if Username =="sultani":
        passwd = "passwd"
        passwd = encrypt_message(passwd)
        client.sendall(passwd)

        passwd = client.recv(1254)
        passwd = decrypt_message(passwd)

        if passwd == "rahmat":
            msg ="Wilcome to Chatbar :) "
            msg = encrypt_message(msg)
            client.sendall(msg)
        else:
            msg = "You are the wrong person !!!"
            msg = encrypt_message(msg)
            client.send(msg)
            client.close()

    else:
        msg = "Sorry You are not Valide User !!!! :("
        msg = encrypt_message(msg)
        client.send(msg)
        client.close()

    while True:
        data = client.recv(1254)
        data = decrypt_message(data)
        print("Bob > ",data)
        msg = input("msg >")
        msg = encrypt_message(msg)
        client.sendall(msg)

except:
    client.close()