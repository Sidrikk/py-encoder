from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
    return ciphertext

def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return plaintext.decode("utf-8")

def main():
    # Генерируем случайный 64-битный ключ
    key = get_random_bytes(8)

    # Оригинальное сообщение в виде byte string
    plaintext = b"Hello, DES encryption!"

    # Шифруем сообщение
    ciphertext = des_encrypt(key, plaintext)
    print("Encrypted:", ciphertext.hex())

    # Дешифруем сообщение
    decrypted = des_decrypt(key, ciphertext)
    print("Decrypted:", decrypted.decode("utf-8"))

if __name__ == "__main__":
    main()
