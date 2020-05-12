class Encryptor():

   def __init__(self, name, public_key, private_key):
       self.name = name
       self.public_key = public_key
       self.private_key = private_key
       self.full_key = None
      
   def generate_partial_key(self, public_key2):
       partial_key = self.public_key ** self.private_key
       partial_key = partial_key % public_key2

       return partial_key
  
   def generate_full_key(self, partial_key_r, public_key2):
       full_key = partial_key_r ** self.private_key
       full_key = full_key % public_key2
       self.full_key = full_key

       return full_key
  
   def encrypt_message(self, message):
       encrypted_message = ""
       key = self.full_key
       for c in message:
           encrypted_message += chr(ord(c) ^ key)

       return encrypted_message
  
   def decrypt_message(self, encrypted_message):
       decrypted_message = ""
       key = self.full_key
       for c in encrypted_message:
           decrypted_message += chr(ord(c) ^ key)

       return decrypted_message