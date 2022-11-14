import sys
import time
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
        screen.print("Error: You must select end-point time!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("A simple timer to count time", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if sys.argv[1].isdigit():
            start_point = 1
            while start_point <= int(sys.argv[1]):
                print(f"\033[92m{start_point}\033[0m", "\r", end="", flush=True)
                time.sleep(1)
                start_point += 1
            screen.print("Times up!", style="green")
        else:
            screen.print("Error: You must enter a digit!", style="red")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()