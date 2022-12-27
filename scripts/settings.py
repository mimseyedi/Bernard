import os
import sys
import json
import hashlib
from pathlib import Path
from getpass import getpass
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


guide_message = """With the settings command you can change some settings of bernard!

Parameters:
-cp change password
-ch change home path"""


# Get the main path.
path_of_file = Path(__file__)
base_path = path_of_file.parent.parent
# Reading settings file.
with open(Path(base_path, "settings.json"), "r") as settings_file:
    settings = json.load(settings_file)


# User authentication function.
def authentication(hashed_password: str):
    return True if hashed_password == settings["password"] else False


# Hash function.
def convert_to_sha(string: str):
    sha_256 = hashlib.sha256()
    sha_256.update(str(string).encode("UTF-8"))
    hashed_string = sha_256.hexdigest()
    return hashed_string


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: Using parameters please!", style="red")

    # If the script is called with the -cp parameter.
    # Change password.
    elif len(sys.argv) == 2 and sys.argv[1] == "-cp":
        current_password = getpass("Enter current password: ")
        hashed_password = convert_to_sha(current_password)

        authenticated = authentication(hashed_password)
        if authenticated:
            new_password = getpass("Enter new password: ")
            confirm_password = getpass("Confirm new password: ")
            if new_password == confirm_password:
                with open(Path(base_path, "settings.json"), "w") as settings_file:
                    new_hashed_password = convert_to_sha(new_password)
                    settings["password"] = new_hashed_password
                    json.dump(settings, settings_file)

                screen.print("Password successfully changed!", style="green")
            else:
                screen.print("Error: Passwords are not the same!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    # If the script is called with the -ch parameter.
    # Change home path.
    elif len(sys.argv) == 2 and sys.argv[1] == "-ch":
        user_password = getpass("Enter password: ")
        hashed_password = convert_to_sha(user_password)

        authenticated = authentication(hashed_password)
        if authenticated:
            new_path = input("Enter new home path: ")
            new_path = Path(os.getcwd(), new_path)
            if new_path.exists() and new_path.is_dir():
                with open(Path(base_path, "settings.json"), "w") as settings_file:
                    settings["path_settings"]["home_path"] = f"{new_path}"
                    json.dump(settings, settings_file)

                screen.print("Home path successfully changed!", style="green")
            else:
                screen.print("Error: Path not found!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
