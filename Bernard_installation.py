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
finally:
    from rich.console import Console
    screen = Console()


def installation_operation():
    home_path = input("Please enter home path: ")
    home_path = Path(os.getcwd(), home_path)
    if home_path.exists():
        if home_path.is_dir():
            user_password = getpass("Please enter a new password: ")
            confirm_password = getpass("Please confirm password: ")

            if user_password == confirm_password:
                os.mkdir("Bernard")
                os.chdir(Path(os.getcwd(), "Bernard"))
                os.mkdir("scripts")

                sha_256 = hashlib.sha256()
                sha_256.update(str(user_password).encode('UTF-8'))
                hashed_password = sha_256.hexdigest()

                settings = {"path_settings": {"scripts_path": f"{Path(os.getcwd(), 'scripts')}",
                                              "home_path": f"{home_path}",
                                              "root_path": f"{os.getcwd()}",
                            "password": hashed_password}}

                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file)
                screen.print("(### The settings file was successfully installed!)", style="green")

                request_to_repo = requests.get(
                    "https://raw.githubusercontent.com/mimseyedi/Bernard/master/Bernard.py")
                with open("Bernard.py", "w") as bernard_file:
                    bernard_file.write(request_to_repo.text)
                screen.print("(### The root file was successfully installed!)", style="green")

                scripts = ["cal.py", "clear.py", "date.py", "deldir.py", "delf.py", "gcc.py",
                           "google.py", "hand.py", "hash.py", "items.py", "map.py", "newdir.py",
                           "newf.py", "open.py", "orgdir.py", "ping.py", "py.py", "read.py",
                           "roll.py", "scripts.py", "settings.py", "sort.py", "system.py",
                           "time.py", "timer.py", "trans.py", "tree.py", "void.py", "wiki.py"]

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

                    screen.print(f"(### The {script} file was successfully installed!)", style="green")

                dep_packages = ["prompt-toolkit==3.0.16", "rich"]
                for package in dep_packages:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL)

                screen.print("### Bernard was successfully installed!", style="bold green")
            else:
                screen.print("Error: Passwords are not the same!", style="red")
        else:
            screen.print("Error: You must select a directory!", style="red")
    else:
        screen.print("Error: Location not found!", style="red")


def init():
    subprocess.run(["clear"])

    screen.print("Welcome to Bernard installation\n", style="bold green")
    screen.print("Please enter your installation path\n1-Current location\n2-Custom location")

    opt_inst_path = input("Choose a option (1/2): ")

    if opt_inst_path == '1':
        if Path(os.getcwd(), "Bernard").exists() and Path(os.getcwd(), "Bernard").is_dir():
            screen.print("Error: A directory named Bernard already exists in this path", style="red")
        else:
            installation_operation()
    else:
        install_path = input("Enter custom location: ")
        install_path = Path(install_path)

        if install_path.exists():
            if install_path.is_dir():
                if install_path in os.listdir():
                    install_path = f"{Path(os.getcwd(), install_path)}"
                if Path(os.getcwd(), install_path, "Bernard").exists() and Path(os.getcwd(), install_path, "Bernard").is_dir():
                    screen.print("Error: A directory named Bernard already exists in this path", style="red")
                else:
                    installation_operation()
            else:
                screen.print("Error: You must select a directory!", style="red")
        else:
            screen.print("Error: Path not found!", style="red")


if __name__ == "__main__":
    init()
