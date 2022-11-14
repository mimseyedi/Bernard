import os
import sys
import json
import hashlib
from getpass import getpass
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """With the settings command you can change some settings of bernard!

Parameters:
-cp change password
-ch change home path"""


path_of_file = os.path.abspath(__file__).split("/")
base_path = '/'.join(path_of_file[1:-2])
with open(f"/{base_path}/settings.json", "r") as settings_file:
    settings = json.load(settings_file)


def authentication(hashed_password: str):
    return True if hashed_password == settings["password"] else False


def convert_to_sha(string: str):
    sha_256 = hashlib.sha256()
    sha_256.update(str(string).encode("UTF-8"))
    hashed_string = sha_256.hexdigest()
    return hashed_string


def init():
    if len(sys.argv) == 1:
        screen.print("Error: Using parameters please!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-cp":
        current_password = getpass("Enter current password: ")
        hashed_password = convert_to_sha(current_password)

        authenticated = authentication(hashed_password)
        if authenticated:
            new_password = getpass("Enter new password: ")
            confirm_password = getpass("Confirm new password: ")
            if new_password == confirm_password:
                with open(f"/{base_path}/settings.json", "w") as settings_file:
                    new_hashed_password = convert_to_sha(new_password)
                    settings["password"] = new_hashed_password
                    json.dump(settings, settings_file)

                screen.print("Password successfully changed!", style="green")
            else:
                screen.print("Error: Passwords are not the same!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-ch":
        user_password = getpass("Enter password: ")
        hashed_password = convert_to_sha(user_password)

        authenticated = authentication(hashed_password)
        if authenticated:
            new_path = input("Enter new home path: ")
            if os.path.exists(new_path) and os.path.isdir(new_path):
                if new_path in os.listdir():
                    new_path = f"{os.getcwd()}/{new_path}"
                with open(f"/{base_path}/settings.json", "w") as settings_file:
                    settings["path_settings"]["home_path"] = new_path
                    json.dump(settings, settings_file)

                screen.print("Home path successfully changed!", style="green")
            else:
                screen.print("Error: Path not found!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
