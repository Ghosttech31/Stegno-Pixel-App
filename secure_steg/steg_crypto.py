from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    """Generate a Fernet key based on a password."""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message: str, password: str) -> bytes:
    """Encrypt the message using a password."""
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes, password: str) -> str:
    """Decrypt the message using a password."""
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()
from PIL import Image

def embed_message_in_image(image_path: str, message: bytes, output_path: str):
    """Embed encrypted message into an image using LSB."""
    img = Image.open(image_path)
    binary_message = ''.join(format(byte, '08b') for byte in message) + '1111111111111110'  # End marker
    data = iter(img.getdata())

    new_pixels = []
    for i in range(0, len(binary_message), 3):
        pixel = list(next(data))
        for j in range(3):
            if i + j < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[i + j])
        new_pixels.append(tuple(pixel))

    # Fill rest of the image
    for pixel in data:
        new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_path)

def extract_message_from_image(image_path: str) -> bytes:
    """Extract hidden message from image using LSB."""
    img = Image.open(image_path)
    binary_data = ''
    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)

    # Split into 8-bit chunks
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message_bytes = []
    for byte in all_bytes:
        if byte == '11111110':  # End marker
            break
        message_bytes.append(int(byte, 2))
    
    return bytes(message_bytes)
