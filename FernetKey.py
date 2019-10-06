from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
print(cipher_key)