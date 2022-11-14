import os
import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print(os.getcwd())
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the map command you can see your current directory or location!", style="green")
    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
