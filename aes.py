from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphertext

def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")

def main():
    # Генерируем случайный 128-битный ключ
    key = get_random_bytes(16)

    # Оригинальное сообщение
    plaintext = b"Hello, AES encryption!"

    # Шифруем сообщение
    ciphertext = encrypt(plaintext, key)
    print("Encrypted:", ciphertext.hex())

    # Дешифруем сообщение
    decrypted = decrypt(ciphertext, key)
    print("Decrypted:", decrypted.decode("utf-8"))

# if __name__ == "__main__":
#     main()
