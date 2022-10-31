import sys
import datetime
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        now = datetime.datetime.now()
        screen.print(now.strftime('%I:%M %p'))
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the time command you can see the time!", style="green")
    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
