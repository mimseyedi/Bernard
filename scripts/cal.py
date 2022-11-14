import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """With the cal command you can see the calendar!

Parameters:
-y Year view"""


def init():
    if len(sys.argv) == 1:
        subprocess.run(["cal"])
    elif len(sys.argv) == 2 and sys.argv[1] == "-y":
        subprocess.run(["cal", "-y"])
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")
    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
