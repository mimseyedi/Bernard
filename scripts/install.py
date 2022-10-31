import os
import sys
import subprocess
try:
    import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)

try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    path_of_file = os.path.abspath(__file__).split("/")
    scripts_path = '/'.join(path_of_file[1:-1])

    if len(sys.argv) == 1:
        screen.print("Error: You must write a script name!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the install command, you can download and install programs or scripts written in "
                      "Bernard's repository.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        request_script = requests.get(
            f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[1]}.py")
        if request_script.status_code != 404:
            if os.path.exists(f"/{scripts_path}/{sys.argv[1]}.py"):
                screen.print("Error: This script already exists!", style="red")
            else:
                with open(f"/{scripts_path}/{sys.argv[1]}.py", "w") as script_file:
                    script_file.write(request_script.text)
                screen.print(f"The '{sys.argv[1]}' script was successfully installed!", style="green")
        else:
            screen.print("Error: Script not found!", style="red")


if __name__ == "__main__":
    init()