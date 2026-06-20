from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad



data = b"Hello word"
KEY =b"12345678901234567890123456789012"

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


massage = "Hello world"
msg = encrypt_message(massage)
print("Encrypted Your massege : ",encrypt_message(massage))
print("Your massege was : ",decrypt_message(msg))
