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
    from prompt_toolkit.completion import WordCompleter
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.16"], stdout=subprocess.DEVNULL)
finally:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.completion import WordCompleter


# Start-point.
def init():
    # Preparing the program by cleaning the screen.
    subprocess.call('clear' if os.name == 'posix' else 'cls')

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
        items = os.listdir(os.getcwd())

        """Delete hidden files so that they are not displayed in the suggested menu
           guide: In Unix systems, hidden file names start with a dot."""
        for item in items:
            if item.startswith("."):
                items.remove(item)

        """Modifying the names of files or directories where spaces are used.
           To modify these names, a backslash should be used before each space so that 
           they are correctly selected by the terminal."""
        items = map(lambda item: r'\ '.join(item.split(" ")), items)

        # An autocompleter is created to create a drop-down menu with the ability to select directory contents.
        autocompleter = WordCompleter(sorted(items), ignore_case=False)

        # Here the main input of the user is taken.
        cmd_input = season.prompt(f'➜ {current_dir}: ', completer=autocompleter).lstrip().split()

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
            elif cmd_input[0] == 'exit': break


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
