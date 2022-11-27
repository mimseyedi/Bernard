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
finally:
    import requests
try:
    from bs4 import BeautifulSoup
except ImportError as package:
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"], stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, "-m", "pip", "install", "lxml"], stdout=subprocess.DEVNULL)
finally:
    from bs4 import BeautifulSoup
try:
    from clint.textui import progress
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "clint"], stdout=subprocess.DEVNULL)
finally:
    from clint.textui import progress
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


# Get the main path.
path_of_file = Path(__file__)
base_path = path_of_file.parent.parent
scripts_path = path_of_file.parent
# Reading settings file.
with open(Path(base_path, "settings.json"), "r") as settings_file:
    settings = json.load(settings_file)


guide_message = """With the scripts command, you can perform and manage tasks related to scripts.

Parameters:
scripts -> show all scripts installed
install -> scripts install <script_name>
uninstall -> scripts uninstall <script_name>
update -> scripts update <script_name>
-u -> show available updates
-n -> show new scripts"""


# User authentication function.
def authentication(password):
    sha_256 = hashlib.sha256()
    sha_256.update(str(password).encode("UTF-8"))
    hashed_password = sha_256.hexdigest()
    return True if hashed_password == settings["password"] else False


# A function to download scripts.
def download_script(url, script_name):
    script = requests.get(url, stream=True)
    with open(Path(scripts_path, f"{script_name}.py"), "wb") as script_file:
        total_length = int(script.headers.get('content-length'))
        for chunk in progress.bar(script.iter_content(chunk_size=1024),
                                  expected_size=(total_length / 1024) + 1):
            if chunk:
                script_file.write(chunk)
                script_file.flush()


# Start-point.
def init():
    # If the script is called alone.
    # Display the scripts installed in the system in two columns.
    if len(sys.argv) == 1:
        scripts = sorted(os.listdir(scripts_path))
        max_length = 0
        for item in scripts:
            if item.endswith(".py"):
                max_length = len(item) if len(item) > max_length else max_length
            else:
                scripts.remove(item)

        screen.print(f"[{len(scripts)} Installed scripts]: ", style="bold yellow")

        index = 0
        while index < len(scripts):
            space = " " * (max_length - len(scripts[index]))
            screen.print(scripts[index][:-3], end=f"{space} \t\t\t", style="green")
            if index + 1 < len(scripts):
                screen.print(scripts[index + 1][:-3], style="green")
            index += 2

        if len(scripts) % 2 != 0: print()

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -n parameter.
    # Check new scripts in Bernard repo.
    elif len(sys.argv) == 2 and sys.argv[1] == "-n":
        installed_scripts = sorted(os.listdir(scripts_path))
        request = requests.get("https://github.com/mimseyedi/Bernard/tree/master/scripts")
        soup = BeautifulSoup(request.text, "lxml")

        items = soup.findAll("div", class_="flex-auto min-width-0 col-md-2 mr-3")
        repo_scripts = [item.text.strip() for item in items if item.text.strip().endswith(".py")]
        new_scripts = [repo_script for repo_script in repo_scripts if repo_script not in installed_scripts]

        if len(new_scripts) > 0:
            max_length = 0
            for item in new_scripts:
                max_length = len(item) if len(item) > max_length else max_length

            screen.print(f"{len(new_scripts)} New scripts are not installed: ", style="bold yellow")

            index = 0
            while index < len(new_scripts):
                space = " " * (max_length - len(new_scripts[index]))
                screen.print(new_scripts[index][:-3], end=f"{space} \t\t\t", style="green")
                if index + 1 < len(new_scripts):
                    screen.print(new_scripts[index + 1][:-3], style="green")
                index += 2
            if len(new_scripts) % 2 != 0: print()
        else:
            screen.print(f"Error: No new script found that is not installed!", style="red")

    # If the script is called with the -u parameter.
    # Check for available updates.
    elif len(sys.argv) == 2 and sys.argv[1] == "-u":
        scripts = sorted(os.listdir(scripts_path))
        available_updates = list()

        for script in scripts:
            if script.endswith(".py"):
                request = requests.get(
                    f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{script}")
                if request.status_code == 200:
                    with open(Path(scripts_path, script), "r") as current_file:
                        current_script = current_file.read()

                    if current_script != request.text:
                        available_updates.append(script)

        if len(available_updates) > 0:
            max_length = 0
            for item in available_updates:
                max_length = len(item) if len(item) > max_length else max_length

            screen.print(f"{len(available_updates)} Available updates: ", style="bold yellow")

            index = 0
            while index < len(available_updates):
                space = " " * (max_length - len(available_updates[index]))
                screen.print(available_updates[index][:-3], end=f"{space} \t\t\t", style="green")
                if index + 1 < len(available_updates):
                    screen.print(available_updates[index + 1][:-3], style="green")
                index += 2
            if len(available_updates) % 2 != 0: print()
        else:
            screen.print(f"Error: No updates found for scripts!", style="red")

    # If the script is called with the install parameter.
    # installing scripts from Bernard repo.
    # Pattern: scripts install orgdir
    elif len(sys.argv) == 3 and sys.argv[1] == "install":
        script_path = Path(scripts_path, f"{sys.argv[2]}.py")
        user_password = getpass("Enter password: ")
        if authentication(user_password):
            request = requests.get(f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[2]}.py")
            if request.status_code == 200:
                if not script_path.exists():
                    download_script(
                        f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[2]}.py",
                        script_name=sys.argv[2])

                    screen.print(f"The '{sys.argv[2]}' script was successfully installed!", style="green")
                else:
                    screen.print(f"Error: '{sys.argv[2]}' script already exists!", style="red")

            elif request.status_code == 404:
                screen.print(f"Error: '{sys.argv[2]}' script not found!", style="red")
            else:
                screen.print(f"Error: No internet connection!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    # If the script is called with the uninstall parameter.
    # Uninstalling scripts.
    # Pattern: scripts uninstall timer
    elif len(sys.argv) == 3 and sys.argv[1] == "uninstall":
        script_path = Path(scripts_path, f"{sys.argv[2]}.py")
        user_password = getpass("Enter password: ")
        if authentication(user_password):
            if script_path.exists():
                ask_to_uninstall = input("Are you sure? (y/n): ").lower()
                if ask_to_uninstall == "y":
                    os.remove(script_path)
                    screen.print(f"'{sys.argv[2]}' script was successfully uninstalled!", style="green")
            else:
                screen.print(f"Error: '{sys.argv[2]}' script not found!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    # If the script is called with the update parameter.
    # Updating scripts from Bernard repo.
    # Pattern: scripts update hand
    elif len(sys.argv) == 3 and sys.argv[1] == "update":
        script_path = Path(scripts_path, f"{sys.argv[2]}.py")
        user_password = getpass("Enter password: ")
        if authentication(user_password):
            if script_path.exists():
                request = requests.get(f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[2]}.py")
                if request.status_code == 200:
                    with open(script_path, "r") as current_file:
                        current_script = current_file.read()

                    if current_script != request.text:
                        os.remove(script_path)
                        download_script(
                            f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[2]}.py",
                            script_name=sys.argv[2])

                        screen.print(f"'{sys.argv[2]}' script was successfully updated!", style="green")
                    else:
                        screen.print(f"Error: No updates found for '{sys.argv[2]}' script!", style="red")

                elif request.status_code == 404:
                    screen.print(f"Error: '{sys.argv[2]}' script not found!", style="red")
                else:
                    screen.print(f"Error: No internet connection!", style="red")
            else:
                screen.print(f"Error: '{sys.argv[1]}' script not installed!", style="red")
        else:
            screen.print("Error: Authentication failed!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
