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
        screen.print("Error: You must choose a name for directory!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the newdir command, you can create a directory in the current location.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if os.path.exists(f'{os.getcwd()}/{sys.argv[1]}'):
            screen.print("Error: There is a directory with this name!", style="red")
        else:
            os.mkdir(f'{os.getcwd()}/{sys.argv[1]}')
            screen.print(f"'{sys.argv[1]}' directory successfully created.", style='green')

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
