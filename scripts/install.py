import os
import sys
import subprocess
try:
    import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
try:
    from clint.textui import progress
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "clint"], stdout=subprocess.DEVNULL)
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
                screen.print(f"Error: '{sys.argv[1]}' script already exists!", style="red")
            else:
                downloading_script = requests.get(
                    f"https://raw.githubusercontent.com/mimseyedi/Bernard/master/scripts/{sys.argv[1]}.py", stream=True)
                with open(f"/{scripts_path}/{sys.argv[1]}.py", "wb") as script_file:
                    total_length = int(downloading_script.headers.get('content-length'))
                    for chunk in progress.bar(downloading_script.iter_content(chunk_size=1024),
                                              expected_size=(total_length / 1024) + 1):
                        if chunk:
                            script_file.write(chunk)
                            script_file.flush()

                screen.print(f"The '{sys.argv[1]}' script was successfully installed!", style="green")
        else:
            screen.print(f"Error: '{sys.argv[1]}' script not found!", style="red")


if __name__ == "__main__":
    init()