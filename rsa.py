import random
import math


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = pow(e, -1, phi)

    return ((e, n), (d, n))


def encrypt(public_key, plaintext):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in plaintext]
    return cipher_text


def decrypt(private_key, cipher_text):
    d, n = private_key
    plain_text = [chr(pow(char, d, n)) for char in cipher_text]
    return ''.join(plain_text)


if __name__ == "__main__":
    # Генерация ключей
    bits = 32 # Рекомендуется использовать более высокий битовый размер для безопасности
    public_key, private_key = generate_keypair(bits)

    # Пример использования
    message = "My name is Danil!"
    print("Original message:", message)

    # Шифрование
    cipher_text = encrypt(public_key, message)
    print("Encrypted message:", cipher_text)

    # Дешифрование
    decrypted_message = decrypt(private_key, cipher_text)
    print("Decrypted message:", decrypted_message)
