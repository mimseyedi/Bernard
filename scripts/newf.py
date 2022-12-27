import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from getpass import getpass
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


# Get the root path.
root_path = Path(__file__).parent.parent


# Check root directory.
def is_root(path):
    return True if str(root_path) in str(path) else False


# User authentication function.
def authentication(password):
    # Reading settings file.
    with open(Path(root_path, "settings.json"), "r") as settings_file:
        settings = json.load(settings_file)

    sha_256 = hashlib.sha256()
    sha_256.update(str(password).encode("UTF-8"))
    hashed_password = sha_256.hexdigest()
    return True if hashed_password == settings["password"] else False


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a name for your file!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the newf command, you can create a file.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # The current path is combined with the input parameter (expected to be a file name).
        file_path = Path(os.getcwd(), sys.argv[1])
        # It is checked that this file exists.
        if file_path.exists():
            screen.print("Error: There is a file with this name!", style="red")
        else:
            if is_root(file_path):
                user_password = getpass("Enter password: ")
                if authentication(user_password):
                    with open(file_path, "w") as _: pass
                    screen.print(f"'{file_path.name}' file successfully created.", style='green')
                else:
                    screen.print("Error: Authentication failed!", style="red")
            else:
                # Make a file.
                with open(file_path, "w") as _: pass
                screen.print(f"'{file_path.name}' file successfully created.", style='green')

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
