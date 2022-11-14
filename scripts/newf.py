import os
import sys
import subprocess
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a name for your file!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the newf command, you can create a file.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        file_path = Path(os.getcwd(), sys.argv[1])
        if file_path.exists():
            screen.print("Error: There is a file with this name!", style="red")
        else:
            with open(file_path, "w") as _: pass
            screen.print(f"'{file_path.name}' file successfully created.", style='green')

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
