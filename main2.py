from PIL import Image
import numpy as np
import os

# Create a dictionary mapping letters to RGB codes
letter_to_rgb = {
    'A': (255, 0, 0),   # Red
    'B': (0, 255, 0),   # Green
    'C': (0, 0, 255),   # Blue
    'D': (255, 255, 0), # Yellow
    'E': (255, 0, 255), # Magenta
    'F': (0, 255, 255), # Cyan
    'G': (192, 192, 192), # Silver
    'H': (128, 0, 0),   # Maroon
    'I': (128, 128, 0), # Olive
    'J': (0, 128, 0),   # Dark Green
    'K': (128, 0, 128), # Purple
    'L': (0, 0, 128),   # Navy
    'M': (255, 165, 0), # Orange
    'N': (255, 192, 203), # Pink
    'O': (255, 255, 255), # White
    'P': (0, 0, 0),     # Black
    # Add more letters as needed
}

# Reverse dictionary for decoding
rgb_to_letter = {v: k for k, v in letter_to_rgb.items()}

def text_to_image(text):
    # Convert text to RGB codes
    rgb_values = [letter_to_rgb.get(char.upper(), (0, 0, 0)) for char in text]  # Default to black for unknown chars
    width = len(rgb_values)
    height = 1  # Single row for simplicity
    image = Image.new('RGB', (width, height))
    image.putdata(rgb_values)
    image.save('encoded_message_001.png')

def image_to_text(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    text = ''.join(rgb_to_letter.get(tuple(pixel), '?') for pixel in pixels.reshape(-1, 3))
    return text

def main():
    user_input = input("Enter text to encode: ")
    text_to_image(user_input)
    print("Image saved as 'encoded_message_001.png'.")

    upload_choice = input("Do you want to upload an image to decode? (yes/no): ")
    if upload_choice.lower() == 'yes':
        image_path = input("Enter the path of the image: ")
        if os.path.exists(image_path):
            decoded_text = image_to_text(image_path)
            print("Decoded text:", decoded_text)
        else:
            print("Image not found.")
    else:
        print("Exiting program.")

if __name__ == "__main__":
    main()
