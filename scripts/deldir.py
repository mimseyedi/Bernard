import os
import sys
import shutil
import subprocess
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """With the deldir command, you can remove a directory in the current location.

Parameters:
-f force to remove full directory"""


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a directory!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        dir_path = Path(os.getcwd(), sys.argv[1])
        if dir_path.exists():
            if dir_path.is_dir():
                if len(os.listdir(dir_path)) <= 0:
                    os.rmdir(dir_path)
                    screen.print(f"'{sys.argv[1]}' directory successfully removed!", style="green")
                else:
                    screen.print(f"Error: '{sys.argv[1]}' directory is full!", style="red")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[1]}' directory not found!", style="red")

    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        dir_path = Path(os.getcwd(), sys.argv[2])
        if dir_path.exists():
            if dir_path.is_dir():
                shutil.rmtree(dir_path)
                screen.print(f"'{sys.argv[2]}' directory successfully removed!", style="green")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[2]}' directory not found!", style="red")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
