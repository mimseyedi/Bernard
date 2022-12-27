"""
Bernard Installation Version 1.0

#How it's work?
    1-Enter installation path
    2-Enter home path
    3-Enter user password

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
import hashlib
import subprocess
from pathlib import Path
from getpass import getpass
try:
    import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
    import requests
try:
    from clint.textui import progress
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "clint"], stdout=subprocess.DEVNULL)
    from clint.textui import progress
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.completion import PathCompleter
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.16"], stdout=subprocess.DEVNULL)
    from prompt_toolkit import prompt
    from prompt_toolkit.validation import Validator
    from prompt_toolkit.completion import PathCompleter


def check_internet_connection():
    try:
        request = requests.get("https://github.com/mimseyedi/Bernard", timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


def path_validation(path: str):
    _path = Path(os.getcwd(), path)
    if _path.exists() and _path.is_dir():
        return _path


def password_validation(confirm_password: str):
    if confirm_password == user_password:
        return confirm_password


def installation_operation():
    if check_internet_connection():
        path_validator = Validator.from_callable(
            path_validation,
            error_message='The selected path must already exist and also be a directory!',
            move_cursor_to_end=True)

        home_path = prompt("Please enter home path: ", validator=path_validator,
                           validate_while_typing=False, completer=PathCompleter())

        global user_password
        user_password = prompt("Please enter a new password: ", is_password=True)

        pass_validator = Validator.from_callable(
            password_validation,
            error_message='Passwords are not the same!',
            move_cursor_to_end=True)

        confirm_password = prompt("Please confirm password: ", validator=pass_validator,
                                  validate_while_typing=True, is_password=True)

        os.mkdir("Bernard")
        os.chdir(Path(os.getcwd(), "Bernard"))
        os.mkdir("scripts")
        os.mkdir("BCS")
        os.mkdir("LICENSES")

        sha_256 = hashlib.sha256()
        sha_256.update(str(user_password).encode('UTF-8'))
        hashed_password = sha_256.hexdigest()

        settings = {"path_settings": {"scripts_path": f"{Path(os.getcwd(), 'scripts')}",
                                      "home_path": f"{home_path}",
                                      "root_path": f"{os.getcwd()}"},
                    "password": hashed_password}

        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file)
        screen.print("(Installation message: The settings file was successfully installed!)", style="green")

        license_request = requests.get("https://raw.githubusercontent.com/mimseyedi/Bernard/master/LICENSES/LICENSE")
        with open("LICENSES/LICENSE", "w", encoding="utf-8") as license_file:
            license_file.write(license_request.text)

        request_to_repo = requests.get(
            "https://raw.githubusercontent.com/mimseyedi/Bernard/master/Bernard.py")
        with open("Bernard.py", "w", encoding="utf-8") as bernard_file:
            bernard_file.write(request_to_repo.text)
        screen.print("(Installation message: The root file was successfully installed!)", style="green")

        scripts = ["bcr.py", "cal.py", "calcul.py", "clear.py", "date.py", "deldir.py", "delf.py",
                   "hand.py", "hash.py", "items.py", "map.py", "newdir.py", "newf.py",
                   "open.py", "orgdir.py", "py.py", "pytor.py", "read.py", "ren.py"
                   "roll.py", "scripts.py", "settings.py", "sort.py", "system.py",
                   "time.py", "timer.py", "tree.py", "void.py"]

        for script in scripts:
            request_scripts = requests.get(
                f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{script}", stream=True)
            with open(f"scripts/{script}", "wb") as script_file:
                total_length = int(request_scripts.headers.get('content-length'))
                for chunk in progress.bar(request_scripts.iter_content(chunk_size=1024),
                                          expected_size=(total_length / 1024) + 1):
                    if chunk:
                        script_file.write(chunk)
                        script_file.flush()

            screen.print(f"(Installation message: The {script} file was successfully installed!)", style="green")

        dep_packages = ["prompt-toolkit==3.0.16", "rich", "requests", "beautifulsoup4"]
        for package in dep_packages:
            subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL)

        screen.print("Installation message: Bernard was successfully installed!", style="bold green")

    else:
        screen.print("Error: You are not connected to the Internet! Please check your internet connection.", style="red")


def init():
    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

    screen.print("Welcome to Bernard installation\n", style="bold green")
    screen.print("Please enter your installation path\n1-Current location\n2-Custom location")

    opt_inst_path = input("Choose a option (1/2): ")

    if opt_inst_path == '1':
        if Path(os.getcwd(), "Bernard").exists() and Path(os.getcwd(), "Bernard").is_dir():
            screen.print("Error: A directory named Bernard already exists in this path", style="red")
        else:
            installation_operation()
    else:
        path_validator = Validator.from_callable(
            path_validation,
            error_message='The selected path must already exist and also be a directory!',
            move_cursor_to_end=True)

        install_path = prompt("Enter custom location: ", validator=path_validator,
                              validate_while_typing=False, completer=PathCompleter())

        if Path(install_path, "Bernard").exists() and Path(install_path, "Bernard").is_dir():
            screen.print("Error: A directory named Bernard already exists in this path", style="red")
        else:
            os.chdir(install_path)
            installation_operation()


if __name__ == "__main__":
    init()
