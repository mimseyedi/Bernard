import os
import sys
import json
import shutil
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


guide_message = """With the deldir command, you can remove a directory in the current location.

Parameters:
-f force to remove full directory"""


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
        screen.print("Error: You must choose a directory!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # The current path is combined with the input parameter (expected to be a directory name).
        dir_path = Path(os.getcwd(), sys.argv[1])
        # It is checked that this path exists.
        if dir_path.exists():
            # It is checked that the entry must be a directory.
            if dir_path.is_dir():
                # Check if the directory is empty?
                if len(os.listdir(dir_path)) <= 0:
                    if is_root(dir_path):
                        user_password = getpass("Enter password: ")
                        if authentication(user_password):
                            os.rmdir(dir_path)
                            screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
                        else:
                            screen.print("Error: Authentication failed!", style="red")
                    else:
                        # If the directory is empty, it will be deleted.
                        os.rmdir(dir_path)
                        screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
                else:
                    screen.print(f"Error: '{sys.argv[1]}' directory is full!", style="red")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{dir_path.name}' directory not found!", style="red")

    # If the script is called with the -f parameter.
    # Force delete a full directory.
    # Pattern: deldir -f <directory>
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        # The current path is combined with the input parameter (expected to be a directory name).
        dir_path = Path(os.getcwd(), sys.argv[2])
        # It is checked that this path exists.
        if dir_path.exists():
            # It is checked that the entry must be a directory.
            if dir_path.is_dir():
                if is_root(dir_path):
                    user_password = getpass("Enter password: ")
                    if authentication(user_password):
                        shutil.rmtree(dir_path)
                        screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
                    else:
                        screen.print("Error: Authentication failed!", style="red")
                else:
                    # Delete directory.
                    shutil.rmtree(dir_path)
                    screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{dir_path.name}' directory not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
