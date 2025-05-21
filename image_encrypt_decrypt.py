from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Function to load image and convert to bytes
def image_to_bytes(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

# Function to save bytes as an image file
def bytes_to_image(image_bytes, output_path):
    with open(output_path, 'wb') as f:
        f.write(image_bytes)

# Generate a random 32-byte (256-bit) AES key
def generate_key():
    return os.urandom(32)

# Encrypt data using AES in CBC mode
def encrypt(data, key):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to multiple of 16 bytes
    padding_length = 16 - (len(data) % 16)
    data += bytes([padding_length]) * padding_length

    encrypted = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted  # Prepend IV for use in decryption

# Decrypt data using AES in CBC mode
def decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    encrypted = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

    # Remove padding
    padding_length = decrypted_padded[-1]
    return decrypted_padded[:-padding_length]

def main():
    key = generate_key()
    print("Encryption key (save this safely):", key.hex())

    original_image_path = 'sample.jpg'  # Change if your image name is different
    encrypted_image_path = 'encrypted_image.bin'
    decrypted_image_path = 'decrypted_sample.jpg'

    # Read image bytes
    image_data = image_to_bytes(original_image_path)

    # Encrypt image bytes
    encrypted_data = encrypt(image_data, key)
    with open(encrypted_image_path, 'wb') as f:
        f.write(encrypted_data)

    print(f"Image encrypted and saved as {encrypted_image_path}")

    # Decrypt the image bytes
    with open(encrypted_image_path, 'rb') as f:
        encrypted_content = f.read()

    decrypted_data = decrypt(encrypted_content, key)
    bytes_to_image(decrypted_data, decrypted_image_path)

    print(f"Image decrypted and saved as {decrypted_image_path}")

if __name__ == "__main__":
    main()