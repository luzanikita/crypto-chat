from random import random, seed
from datetime import datetime

class Encryptor():
    N = 9973

    def __init__(self, name):
        seed(datetime.now())
        self.name = name
        self.private_key = int(1 + random() ** 1000)
        self.key = None

    def generate_key(self, partial_key):
        key = (partial_key ** self.private_key) % self.N

        return key

    def encrypt_message(self, message):
        encrypted_message = ""
        for c in message:
            encrypted_message += chr(ord(c) ^ self.key)

        return encrypted_message

    def decrypt_message(self, encrypted_message):
        return self.encrypt_message(encrypted_message)