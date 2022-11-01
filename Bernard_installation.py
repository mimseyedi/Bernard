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
import json
import hashlib
import requests
import subprocess
from getpass import getpass
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def installation_operation():
    home_path = input("Please enter home path: ")
    if os.path.exists(home_path):
        if os.path.isdir(home_path):
            if home_path in os.listdir():
                home_path = f"{os.getcwd()}/{home_path}"

            user_password = getpass("Please enter a new password: ")
            confirm_password = getpass("Please confirm password: ")

            if user_password == confirm_password:
                os.mkdir("Bernard")
                os.chdir(f"{os.getcwd()}/Bernard")
                os.mkdir("scripts")

                sha_256 = hashlib.sha256()
                sha_256.update(str(password).encode('UTF-8'))
                hashed_password = sha_256.hexdigest()

                settings = {"path_settings": {"scripts_path": f"{os.getcwd()}/scripts",
                                              "home_path": home_path,
                                              "root_path": os.getcwd()},
                            "password": hashed_password}

                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file)
                screen.print("(### The settings file was successfully installed!)", style="green")

                request_to_repo = requests.get(
                    "https://raw.githubusercontent.com/mimseyedi/Bernard/master/bernard.py")
                with open("Bernard.py", "w") as bernard_file:
                    bernard_file.write(request_to_repo.text)
                screen.print("(### The root file was successfully installed!)", style="green")

                scripts = ["cal.py", "clear.py", "date.py", "deldir.py", "delf.py", "gcc.py",
                           "hash.py", "install.py", "items.py", "map.py", "newdir.py",
                           "newf.py", "py.py", "roll.py", "settings.py", "system.py",
                           "time.py", "timer.py", "uninstall.py", "update.py", "void.py"]

                for script in scripts:
                    request_scripts = requests.get(
                        f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{script}")
                    with open(f"scripts/{script}", "w") as script_file:
                        script_file.write(request_scripts.text)
                    screen.print(f"(### The {script} file was successfully installed!)", style="green")

                    dep_packages = ["prompt_toolkit", "rich"]
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
        if os.path.exists(f"{os.getcwd()}/Bernard") and os.path.isdir(f"{os.getcwd()}/Bernard"):
            screen.print("Error: A directory named Bernard already exists in this path", style="red")
        else:
            installation_operation()
    else:
        install_path = input("Enter custom location: ")

        if os.path.exists(install_path):
            if os.path.isdir(install_path):
                if install_path in os.listdir():
                    install_path = f"{os.getcwd()}/{install_path}"
                if os.path.exists(f"{install_path}/Bernard") and os.path.isdir(f"{install_path}/Bernard"):
                    screen.print("Error: A directory named Bernard already exists in this path", style="red")
                else:
                    installation_operation()
            else:
                screen.print("Error: You must select a directory!", style="red")
        else:
            screen.print("Error: Location not found!", style="red")


if __name__ == "__main__":
    init()
