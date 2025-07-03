import random
import string

def generate_password(length=12, use_letters=True, use_digits=True, use_symbols=True):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Error: No character sets selected."

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

try:
    length = int(input("Enter password length: "))
    use_letters = input("Include letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    password = generate_password(length, use_letters, use_digits, use_symbols)
    print("Generated password:", password)

except ValueError:
    print("Please enter a valid number for password length.")