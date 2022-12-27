import os
import sys
import time
import subprocess
from random import randint
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.shortcuts import confirm
    from prompt_toolkit.formatted_text import ANSI
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.shortcuts import button_dialog
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.16"], stdout=subprocess.DEVNULL)
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.shortcuts import confirm
    from prompt_toolkit.formatted_text import ANSI
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.shortcuts import button_dialog
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


# A message for guidance and how to use the script.
guide_message = """This is version of the classic letter guessing game called Hangman. 
You are shown a set of blank letters that match a word or phrase and you have to guess what these letters are to reveal the hidden word."""

# Variables that hold the size of the terminal window to fit in the middle of the screen.
newline, space = os.get_terminal_size()[1] // 3 - 4, os.get_terminal_size()[0] // 2 - 5

# List of words.
words_list = ['MOUSE', 'TRAIN', 'BICYCLE', 'ENGINE', 'BRIDGE', 'THEATER', 'CHURCH', 'POCKET', 'PRESIDENT', 'PERSON',
              'PRIEST', 'REPORTER', 'HEAVEN', 'WEDDING', 'ELECTION', 'CONTRACT', 'INSTRUMENT', 'BATHROOM', 'GARDEN',
              'CAMERA', 'SHOULDER', 'DISEASE', 'OCEAN', 'BEACH', 'ELECTRIC', 'PROGRAM', 'DIAMOND', 'TEMPERATURE',
              'PATTERN', 'STRAIGHT', 'SUMMER', 'HANGMAN', 'EXPENSIVE', 'SHALLOW', 'FAMOUS', 'BEDROOM', 'MANAGER',
              'SOCCER', 'RUSSIAN', 'NOVEL', 'ICECREAM', 'CREATIVE', 'HOLLYWOOD', 'RETURN', 'RANDOM', 'LOBSTER', "MAHSA"]


# A function to draw hangman.
def draw_hangman(step: int):
    if step == 1:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 2:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 3:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + " |     |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 4:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + "/|     |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 5:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + "/|\    |")
        print(" " * space + "       |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 6:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + "/|\    |")
        print(" " * space + "/      |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")

    elif step == 7:
        print("\n" * newline)
        print(" " * space + " +-----+")
        print(" " * space + " |     |")
        print(" " * space + " O     |")
        print(" " * space + "/|\    |")
        print(" " * space + "/ \    |")
        print(" " * space + "       |")
        print(" " * space + " =========\n")


# A function to draw a word in the form of a blank space (-).
def draw_hidden_word(word: str, word_array: list):
    space_needed = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7}
    screen.print("\n" + " " * (space - space_needed[len(word)]) + ' '.join(word_array))


# A function to filter the input in an acceptable form.
def word_validation(text):
    special_char = "?!@#$%^&*(){}[]'-_./\;:~<>`=\""
    if len(text) == 1 and not text.isdigit() and text not in special_char:
        return text


# A function to execute the final process.
def end_process(title: str, text: str):
    dialog_style = Style.from_dict({
        'dialog': 'bg:#101357',
        'dialog frame.label': 'bg:#007f4f #000000' if title == "Victory" else 'bg:#e50000 #000000',
        'dialog.body': 'bg:#007f4f #000000' if title == "Victory" else 'bg:#e50000 #000000',
        'dialog shadow': 'bg:#000000',
        'button.focused': 'bg:#101357',})

    ask_dialog = button_dialog(title=title, text=text,
                               buttons=[('Play Again', True),
                                        ('Exit', False)],
                               style=dialog_style).run()
    return ask_dialog


# Start-point.
def load_screen():
    # If the script is called alone.
    if len(sys.argv) == 1:
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

        print("\n" * newline)
        print('\033[5m' + ' ' * (space - 26) + '888')
        print(' ' * (space - 26) + '888')
        print(' ' * (space - 26) + '888')
        print(' ' * (space - 26) + '88888b.  8888b. 88888b.  .d88b. 88888b.d88b.  8888b. 88888b.')
        print(' ' * (space - 26) + '888 "88b    "88b888 "88bd88P"88b888 "888 "88b    "88b888 "88b')
        print(' ' * (space - 26) + '888  888.d888888888  888888  888888  888  888.d888888888  888')
        print(' ' * (space - 26) + '888  888888  888888  888Y88b 888888  888  888888  888888  888')
        print(' ' * (space - 26) + '888  888"Y888888888  888 "Y88888888  888  888"Y888888888  888')
        print(' ' * (space - 26) + '                            888')
        print(' ' * (space - 26) + '                       Y8b d88P')
        print(' ' * (space - 26) + '                        "Y88P"\n\n' + '\033[0m')

        time.sleep(3)
        init()

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# Main function.
def init():
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

    goal_word = words_list[randint(0, len(words_list) - 1)]
    victory, hangman_step, word_array = False, 1, ["-" for _ in goal_word]

    validator = Validator.from_callable(
        word_validation,
        error_message='You can only enter one letter of the English alphabet!',
        move_cursor_to_end=True)

    while hangman_step <= 7:
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
        draw_hangman(hangman_step)
        draw_hidden_word(goal_word, word_array)

        mistake = None

        guess = prompt("\n" + " " * (space) + "Guess: ",
                       validator=validator, validate_while_typing=True)

        for index, letter in enumerate(goal_word):
            if letter == guess.upper():
                word_array.pop(index)
                word_array.insert(index, letter)
                mistake = False
            else:
                if mistake == False: ...
                else:
                    mistake = True

        if mistake: hangman_step += 1

        if word_array.count("-") == 0:
            victory = True
            break

    if victory:
        last_state = end_process(title="Victory",
                                 text=f"Congratulations, you won!\nThe word is '{goal_word}'")
        if last_state: init()
        else:
            subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
            sys.exit()

    else:
        last_state = end_process(title="Game Over",
                                 text=f"Unfortunately, you lost!\nThe word is '{goal_word}'")
        if last_state: init()
        else:
            subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
            sys.exit()


# The starting point is set on the init function.
if __name__ == "__main__":
    load_screen()
