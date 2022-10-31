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
        screen.print("With the update command, you can update scripts from Bernard's repository.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if os.path.exists(f"/{scripts_path}/{sys.argv[1]}.py"):
            request_script = requests.get(
                f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[1]}.py")
            if request_script.status_code != 404:
                with open(f"/{scripts_path}/{sys.argv[1]}.py", "r") as current_file:
                    current_script = current_file.read()

                if current_script == request_script.text:
                    screen.print(f"Error: No updates found for '{sys.argv[1]}' script!", style="red")
                else:
                    os.remove(f"/{scripts_path}/{sys.argv[1]}.py")
                    with open(f"/{scripts_path}/{sys.argv[1]}.py", "w") as updated_script:
                        updated_script.write(request_script.text)
                        screen.print(f"'{sys.argv[1]}' script was successfully updated!", style="green")
            else:
                screen.print(f"Error: '{sys.argv[1]}' script not found!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[1]}' script not installed!", style="red")


if __name__ == "__main__":
    init()
