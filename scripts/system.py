import os
import sys
import json
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    path_of_file = os.path.abspath(__file__).split("/")
    root_path = '/'.join(path_of_file[1:-2])

    if len(sys.argv) == 1:
        with open(f"/{root_path}/settings.json", "r") as settings_file:
            settings = json.load(settings_file)

        screen.print("System Name :", os.uname()[0], style='bold green')
        screen.print("Node Name :", os.uname()[1], style='bold green')
        screen.print("Kernel Release :", os.uname()[2], style='bold green')
        screen.print("Os-Version :", os.uname()[3], style='bold green')
        screen.print("Architecture :", os.uname()[4], style='bold green')
        screen.print(f"Root Path: {settings['path_settings']['root_path']}", style="bold green")
        screen.print(f"Scripts Path: {settings['path_settings']['scripts_path']}", style="bold green")
        screen.print(f"Home Path: {settings['path_settings']['home_path']}", style="bold green")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the system command you can see system and bernard information!", style="green")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
