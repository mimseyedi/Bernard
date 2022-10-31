import os
import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a file!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the delf command, you can remove a file.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if os.path.exists(f'{os.getcwd()}/{sys.argv[1]}'):
            if os.path.isfile(f'{os.getcwd()}/{sys.argv[1]}'):
                os.remove(f'{os.getcwd()}/{sys.argv[1]}')
                screen.print(f"'{sys.argv[1]}' file successfully removed!", style="green")
            else:
                screen.print("Error: You must choose a file!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[1]}' file not found!", style="red")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
