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


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must choose a directory!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # The current path is combined with the input parameter (expected to be a directory name).
        dir_path = Path(os.getcwd(), sys.argv[1])
        # It is checked that this path exists.
        if dir_path.exists():
            # It is checked that the entry must be a directory.
            if dir_path.is_dir():
                # Check if the directory is empty?
                if len(os.listdir(dir_path)) <= 0:
                    # If the directory is empty, it will be deleted.
                    os.rmdir(dir_path)
                    screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
                else:
                    screen.print(f"Error: '{sys.argv[1]}' directory is full!", style="red")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{dir_path.name}' directory not found!", style="red")

    # If the script is called with the -f parameter.
    # Force delete a full directory.
    # Pattern: deldir -f <directory>
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        # The current path is combined with the input parameter (expected to be a directory name).
        dir_path = Path(os.getcwd(), sys.argv[2])
        # It is checked that this path exists.
        if dir_path.exists():
            # It is checked that the entry must be a directory.
            if dir_path.is_dir():
                # Delete directory.
                shutil.rmtree(dir_path)
                screen.print(f"'{dir_path.name}' directory successfully removed!", style="green")
            else:
                screen.print("Error: You must choose a directory!", style="red")
        else:
            screen.print(f"Error: '{dir_path.name}' directory not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
