"""
Bernard Version 1.0

Bernard is an assistant and application to customize the terminal to do the tasks you need,
which can be run on all bash Unix shells. Bernard consists of a script reader and a directory of scripts.
With the help of script reader, Bernard can read and execute smaller programs by Python interpreter.
In this way, it will be easier to develop Bernard by writing small and separate programs.

Bernard is open source under the MIT license and you can easily use it
and make any changes you like and share it with others.

Bernard github repository:
https://github.com/mimseyedi/Bernard
"""


import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import ANSI, HTML
    from prompt_toolkit.shortcuts import CompleteStyle, confirm
    from prompt_toolkit.completion import WordCompleter, Completer, Completion
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.16"], stdout=subprocess.DEVNULL)
finally:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import ANSI, HTML
    from prompt_toolkit.shortcuts import CompleteStyle, confirm
    from prompt_toolkit.completion import WordCompleter, Completer, Completion


# Calculate file size in KB, MB, GB.
def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.0f %s" % (size, x)
        size /= 1024.0


# Completer class for show all items in directories.
class ItemsInCurrentDirCompleter(Completer):
    def get_completions(self, document, complete_event):
        items = []
        """Delete hidden files so that they are not displayed in the suggested menu
           guide: In Unix systems, hidden file names start with a dot."""
        for item in os.listdir(os.getcwd()):
            if not item.startswith("."):
                """Modifying the names of files or directories where spaces are used.
                   To modify these names, a backslash should be used before each space so that 
                   they are correctly selected by the terminal."""
                items.append(item)

        # Descriptions of the items are included in this dictionary.
        meta_dict = {}
        for item in items:
            item_path = Path(os.getcwd(), item)
            # If is directory:
            if item_path.is_dir():
                meta_dict[item] = HTML(f"<style bg='#C0C0C0' color='#008000'>Type(Directory) - {convert_bytes(os.path.getsize(item_path))} - {len(os.listdir(item_path))} items</style>")
            # If is file:
            else:
                meta_dict[item] = HTML(f"<style bg='#C0C0C0' color='#008000'>Type(File) - {convert_bytes(os.path.getsize(item_path))}</style>")

        word = document.get_word_before_cursor()
        for item in items:
            if item.startswith(word):
                display = item
                yield Completion(item, start_position=-len(word),
                                 display=display, display_meta=meta_dict.get(item),)


# Start-point.
def init():
    # Preparing the program by cleaning the screen.
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

    # Reading settings file.
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
        scripts_path = settings["path_settings"]["scripts_path"]
        home_path = settings["path_settings"]["home_path"]

    # Change the home path to what is set in the settings file.
    os.chdir(home_path)

    # Creating an input receiver and allocating memory for it.
    season = PromptSession(history=InMemoryHistory())

    # The main loop starts here.
    while True:
        # Getting the name of the last directory and the items inside it.
        current_dir = Path(os.getcwd()).name

        # Here the main input of the user is taken.
        cmd_input = season.prompt(ANSI(f'\x1b[32m➜ \x1b[36;1m{current_dir}:\x1b[0m '),
                                  completer=ItemsInCurrentDirCompleter(),
                                  complete_style=CompleteStyle.MULTI_COLUMN).lstrip().split()

        # Commands are checked only if they contain content.
        if len(cmd_input) > 0:
            """Since the input is received as a list of strings, its first index will be checked.
               As an example, it is checked whether the first index that contains the main command or the name of the 
               script that wants to be executed includes the internal commands of home, goto and back or not?
               These commands are internal scripts that should be managed here according to their functionality."""

            if cmd_input[0] not in ["home", "goto", "back", "exit"]:
                # If the called command was not from internal scripts, it will go to the scripts directory and execute the called script.
                main_command = cmd_input[0] + '.py'
                # Separate parameters of called scripts.
                parameters = ' '.join(cmd_input[1:])

                script_path = Path(scripts_path, main_command)
                
                if script_path.exists():
                    os.system(f'{sys.executable} {script_path} {parameters}')
                else:
                    # Display a message if the desired script is not found.
                    screen.print(f"Error: '{main_command[:-3]}' command not found!", style="red")

            # Internal home script.
            elif cmd_input[0] == "home":
                if len(cmd_input) == 1:
                    os.chdir(home_path)
                # -h parameter to display help.
                elif len(cmd_input) == 2 and cmd_input[1] == "-h":
                    screen.print("With the home command, you can goto home location.", style="green")
                else:
                    sceen.print("Error: Unknown parameters!", style="red")

            # Internal goto script.
            elif cmd_input[0] == "goto":
                if len(cmd_input) == 1:
                    screen.print("Error: You must choose a path!", style="red")
                # -h parameter to display help.
                elif len(cmd_input) == 2 and cmd_input[1] == "-h":
                    screen.print("With the goto command, you can change path location and move between directories.",
                                  style="green")
                elif len(cmd_input) == 2 and cmd_input[1] != "-h":
                    destination = Path(os.getcwd(), cmd_input[1])
                    if destination.exists():
                        if destination.is_dir():
                            os.chdir(destination)
                        else:
                            screen.print("Error: you must select a directory!", style="red")
                    else:
                        screen.print("Error: path not found!", style="red")

            # Internal back script.
            elif cmd_input[0] == "back":
                if len(cmd_input) == 1:
                    os.chdir("..")
                # -h parameter to display help.
                elif len(cmd_input) == 2 and cmd_input[1] == "-h":
                    screen.print("With the back command, you can change path location and back to last path.",
                                  style="green")
                else:
                    screen.print("Error: Unknown parameters!", style="red")

            # Exit command to quit the program and break the main loop.
            elif cmd_input[0] == 'exit':
                answer = confirm("Do you really want to exit?")
                if answer:
                    # Preparing the program by cleaning the screen.
                    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
                    break


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
