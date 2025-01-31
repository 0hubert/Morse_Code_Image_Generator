# Dictionary containing Morse Code mappings
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', ' ': ' ',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'
}

# Create reverse dictionary for morse to text conversion
MORSE_TO_TEXT = {value: key for key, value in MORSE_CODE_DICT.items()}

from PIL import Image, ImageDraw
import random
import os

# Constants for image generation
DOT_WIDTH = 30
DASH_WIDTH = 90
SYMBOL_HEIGHT = 30
SPACE_WIDTH = 30
WORD_SPACE_WIDTH = 90
BACKGROUND_COLOR = (255, 255, 255)  # White

def generate_random_color():
    """Generate a random RGB color"""
    return (random.randint(0, 255), 
            random.randint(0, 255), 
            random.randint(0, 255))

def create_morse_image(morse_code, letter_colors):
    """Create an image from morse code with colored symbols"""
    # Calculate image dimensions
    width = 0
    morse_words = morse_code.split('  ')
    
    # Calculate total width
    for i, word in enumerate(morse_words):
        symbols = word.split()
        for symbol in symbols:
            for char in symbol:
                width += DOT_WIDTH if char == '.' else DASH_WIDTH
            width += SPACE_WIDTH  # Space between letters
        if i < len(morse_words) - 1:
            width += WORD_SPACE_WIDTH  # Space between words
    
    # Create image with white background
    img = Image.new('RGB', (width, SYMBOL_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Current x position
    x = 0
    
    # Draw morse code
    for i, word in enumerate(morse_words):
        symbols = word.split()
        for symbol in symbols:
            original_letter = MORSE_TO_TEXT.get(symbol, ' ')
            color = letter_colors.get(original_letter, (0, 0, 0))
            
            for char in symbol:
                if char == '.':
                    draw.rectangle([x, 0, x + DOT_WIDTH, SYMBOL_HEIGHT], 
                                 fill=color)
                    x += DOT_WIDTH
                elif char == '-':
                    draw.rectangle([x, 0, x + DASH_WIDTH, SYMBOL_HEIGHT], 
                                 fill=color)
                    x += DASH_WIDTH
            x += SPACE_WIDTH  # Add space between letters
        
        if i < len(morse_words) - 1:
            x += WORD_SPACE_WIDTH  # Add space between words
    
    return img

def text_to_morse(text):
    """Convert text to Morse Code"""
    morse_text = ''
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_text += MORSE_CODE_DICT[char] + ' '
        else:
            morse_text += char + ' '
    return morse_text.strip()

def morse_to_text(morse_code):
    """Convert Morse Code to text"""
    text = ''
    morse_words = morse_code.split('  ')
    
    for morse_word in morse_words:
        morse_chars = morse_word.split()
        for morse_char in morse_chars:
            if morse_char in MORSE_TO_TEXT:
                text += MORSE_TO_TEXT[morse_char]
        text += ' '
    
    return text.strip()

# New function to save the image
def save_image(img, filepath):
    """Save the generated image to the specified filepath"""
    img.save(filepath)

def upload_image(filepath):
    """Upload an image and return its RGB data"""
    img = Image.open(filepath)
    rgb_data = list(img.getdata())  # Get RGB data
    return rgb_data

def rgb_to_code(rgb_data):
    """Convert RGB data to English alphabet code"""
    # Example conversion logic (you can customize this)
    code = ''
    for r, g, b in rgb_data:
        # Convert each RGB triplet to a character
        # This example uses a simple mapping to ensure a wider range of characters
        code += chr((r % 26) + 65)  # Map R to A-Z
        code += chr((g % 26) + 65)  # Map G to A-Z
        code += chr((b % 26) + 65)  # Map B to A-Z
    return code

# Create a mapping from letters to RGB values
def create_rgb_mapping():
    mapping = {}
    for i in range(26):  # For letters A-Z
        # Assign a unique RGB value for each letter
        mapping[chr(i + 65)] = (i * 10, i * 10, i * 10)  # Example: grayscale mapping
    return mapping

# Convert text to RGB
def text_to_rgb(text, rgb_mapping):
    rgb_data = []
    for char in text.upper():
        if char in rgb_mapping:
            rgb_data.append(rgb_mapping[char])
        else:
            rgb_data.append((0, 0, 0))  # Default for unknown characters (black)
    return rgb_data

# Convert RGB back to text
def rgb_to_text(rgb_data, rgb_mapping):
    reverse_mapping = {v: k for k, v in rgb_mapping.items()}
    text = ''
    for rgb in rgb_data:
        text += reverse_mapping.get(rgb, '?')  # Use '?' for unknown RGB values
    return text

def main():
    print("Welcome to the RGB Converter!")
    print("Enter '1' for Text to RGB")
    print("Enter '2' for RGB to Text from an image file")
    print("Enter 'quit' to exit the program")
    
    rgb_mapping = create_rgb_mapping()  # Create the RGB mapping

    while True:
        choice = input("\nEnter your choice (1/2/quit): ")
        
        if choice.lower() == 'quit':
            print("Thanks for using the RGB Converter!")
            break
            
        elif choice == '1':
            text = input("Enter the text to convert to RGB: ")
            rgb_result = text_to_rgb(text, rgb_mapping)
            print("\nRGB Data:")
            print(rgb_result)
            
        elif choice == '2':
            image_path = input("Enter the path to the image file (e.g., \\morse_images\\encoded_five.png): ")
            
            # Check if the file exists
            if os.path.isfile(image_path):
                rgb_data = upload_image(image_path)  # Upload and get RGB data
                text_result = rgb_to_text(rgb_data, rgb_mapping)  # Convert RGB data to text
                print("\nDecoded Text:")
                print(text_result)
            else:
                print(f"Error: The file '{image_path}' does not exist. Please check the path and try again.")
            
        else:
            print("Invalid choice! Please enter 1, 2, or 'quit'")

if __name__ == "__main__":
    main()
