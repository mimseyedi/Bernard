import os
import sys
import json
import subprocess
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


# Start-point.
def init():
    # Get the main path.
    path_of_file = Path(__file__)
    base_path = path_of_file.parent.parent

    # If the script is called alone.
    if len(sys.argv) == 1:
        # Reading the settings file.
        with open(Path(base_path, "settings.json"), "r") as settings_file:
            settings = json.load(settings_file)

        screen.print("System Name :", os.uname()[0], style='bold green')
        screen.print("Node Name :", os.uname()[1], style='bold green')
        screen.print("Kernel Release :", os.uname()[2], style='bold green')
        screen.print("Os-Version :", os.uname()[3], style='bold green')
        screen.print("Architecture :", os.uname()[4], style='bold green')
        screen.print(f"Root Path: {settings['path_settings']['root_path']}", style="bold green")
        screen.print(f"Scripts Path: {settings['path_settings']['scripts_path']}", style="bold green")
        screen.print(f"Home Path: {settings['path_settings']['home_path']}", style="bold green")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the system command you can see system and bernard information!", style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
