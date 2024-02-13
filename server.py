from flask import Flask, request, jsonify
from flask_cors import CORS
from langdetect import detect
from lzw import LZW
import fano
import rsa
import aes
import des

app = Flask(__name__)
CORS(app)

bits = 32  # Рекомендуется использовать более высокий битовый размер для безопасности
public_key, private_key = rsa.generate_keypair(bits)

aes_key = aes.get_random_bytes(16)
des_key = des.get_random_bytes(8)

# def encrypt_caesar(text, shift):
#     result = ""
#     for char in text:
#         if char.isalpha():
#             if char.islower():
#                 result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
#             else:
#                 result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
#         else:
#             result += char
#     return result


def caesar_cipher(text, shift):
    language = detect(text)
    result = ""
    alphabet = ""

    if language == 'ru':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    else:  # Default to English
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()

            if char in alphabet:
                index = (alphabet.index(char) - shift) % len(alphabet)
                result += alphabet[index].upper() if is_upper else alphabet[index]
            else:
                result += char
        else:
            result += char

    return result


@app.route('/api/submit_text', methods=['POST'])
def submit_text():
    try:
        data = request.get_json()

        if data.get('selectedEncodeValue'):
            method = data.get('selectedEncodeValue', '')
            input_text = data.get('inputText', '')
        else:
            method = data.get('selectedDecodeValue', '')
            input_text = data.get('decodeText', '')

        if method == 'cesar':
            result = caesar_cipher(input_text, -3)
        elif method == 'decode_cesar':
            result = caesar_cipher(input_text, 3)

        elif method == 'fano':
            result = fano.encode_shannon_fano(input_text)[0]

        elif method == 'lzw':
            abc = list(sorted(set(list(input_text))))
            lzw = LZW(abc)
            t = lzw.encode(input_text)
            result = ', '.join([str(i) for i in t])

        elif method == 'rsa':
            result = ', '.join([str(i) for i in rsa.encrypt(public_key, input_text)])
        elif method == 'decode_rsa':
            result = rsa.decrypt(private_key, map(int, input_text.split(', ')))

        elif method == 'aes':
            result = aes.encrypt(input_text.encode('utf-8'), aes_key).hex()
        elif method == 'decode_aes':
            result = str(aes.decrypt(bytes.fromhex(input_text), aes_key))

        elif method == 'des':
            result = des.des_encrypt(des_key, input_text.encode('utf-8')).hex()
        elif method == 'decode_des':
            result = str(des.des_decrypt(des_key, bytes.fromhex(input_text)))


        else:
            result = f"Что-то пошло не так"

        response = jsonify({'result': result})
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
        # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        # response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)


