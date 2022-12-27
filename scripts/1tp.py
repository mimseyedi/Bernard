import sys
import subprocess
from random import randint
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


guide_message = """With the 1tp command, you can generate disposable pads for encryption and sending messages.

Parameters:
-e encrypt the message -> example: 1tp -e I love Python!
-d dectypt the message"""


# Start-point.
def init():
    alphabet = "abcdefghijklnmopqrstuvwxyz"
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must using parameters!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -e parameter.
    # Pattern: 1tp -e <message>
    elif len(sys.argv) >= 3 and sys.argv[1] == "-e":
        string, cypher, key = ' '.join(sys.argv[2:]), '', list()
        for letter in string:
            letter = letter.lower()
            if letter.isalpha():
                random_item = randint(0, 25)
                key.append(str(random_item))
                letter_index = alphabet.find(letter)
                try:
                    cypher += alphabet[letter_index + int(key[-1])]
                except IndexError:
                    cypher += alphabet[(letter_index + int(key[-1])) % len(alphabet)]
            elif letter == " ":
                key.append("$")
                cypher += "$"
            else:
                key.append(letter)
                cypher += letter

        screen.print(f"Cypher: {cypher}", style="green")
        screen.print("  └── Key:", ' '.join(key), style="blue")

    # If the script is called with the -d parameter.
    # Pattern: 1tp -d
    elif len(sys.argv) == 2 and sys.argv[1] == "-d":
        cypher = input("Enter Cypher: ")
        key = input("Enter Key: ").split()

        message = str()
        for index in range(len(cypher)):
            if cypher[index].isalpha():
                letter_index = alphabet.find(cypher[index])
                try:
                    message += alphabet[letter_index - int(key[index])]
                except IndexError:
                    message += alphabet[(letter_index - int(key[index])) % len(alphabet)]
            elif cypher[index] == "$":
                message += " "
            else:
                message += cypher[index]

        screen.print(message, style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()