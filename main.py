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

def main():
    print("Welcome to the Morse Code Converter!")
    print("Enter '1' for Text to Morse Code (with colored image)")
    print("Enter '2' for Morse Code to Text")
    print("Enter 'quit' to exit the program")
    
    # Create 'morse_images' directory if it doesn't exist
    if not os.path.exists('morse_images'):
        os.makedirs('morse_images')
    
    while True:
        choice = input("\nEnter your choice (1/2/quit): ")
        
        if choice.lower() == 'quit':
            print("Thanks for using the Morse Code Converter!")
            break
            
        elif choice == '1':
            text = input("Enter the text to convert to Morse Code: ")
            morse_result = text_to_morse(text)
            print("\nMorse Code:")
            print(morse_result)
            
            # Generate random colors for each unique letter
            letter_colors = {letter: generate_random_color() 
                           for letter in set(text.upper())}
            
            # Create and save the image
            img = create_morse_image(morse_result, letter_colors)
            image_path = f'morse_images/morse_{text.replace(" ", "_")}.png'
            img.save(image_path)
            print(f"\nImage saved as: {image_path}")
            
            # Print color legend
            print("\nColor Legend:")
            for letter, color in letter_colors.items():
                if letter != ' ':
                    print(f"Letter '{letter}': RGB{color}")
            
        elif choice == '2':
            print("Note: Use single space between letters and double space between words")
            morse = input("Enter the Morse Code to convert to text: ")
            text_result = morse_to_text(morse)
            print("\nText:")
            print(text_result)
            
        else:
            print("Invalid choice! Please enter 1, 2, or 'quit'")

if __name__ == "__main__":
    main()
