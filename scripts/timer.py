import sys
import time
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select end-point time!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("A simple timer to count time", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # Is it checked if the input is a number?
        if sys.argv[1].isdigit():
            start_point = 1
            while start_point <= int(sys.argv[1]):
                print(f"\033[92m{start_point}\033[0m", "\r", end="", flush=True)
                time.sleep(1)
                start_point += 1
            screen.print("Times up!", style="green")
        else:
            screen.print("Error: You must enter a digit!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()