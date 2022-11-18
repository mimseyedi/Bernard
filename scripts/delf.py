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


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a file!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the delf command, you can remove a file.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # The current path is combined with the input parameter (expected to be a file name).
        file_path = Path(os.getcwd(), sys.argv[1])
        # It is checked that this path exists.
        if file_path.exists():
            # It is checked that the entry must be a file.
            if file_path.is_file():
                # Delete file.
                os.remove(file_path)
                screen.print(f"'{file_path.name}' file successfully removed!", style="green")
            else:
                screen.print("Error: You must choose a file!", style="red")
        else:
            screen.print(f"Error: '{file_path.name}' file not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
