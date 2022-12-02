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
        screen.print("Error: You must choose a file or directory!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the ren command, you can change the names of files or directories.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 3 and sys.argv[1] != "-h":
        current_path, new_path = Path(os.getcwd(), sys.argv[1]), Path(os.getcwd(), sys.argv[2])
        if current_path != new_path:
            if current_path.exists():
                if current_path.is_dir():
                    if not new_path.exists():
                        Path.rename(current_path, new_path)
                        screen.print(f"Directory '{sys.argv[1]}' successfully renamed to '{sys.argv[2]}'!",
                                     style="green")
                    else:
                        screen.print(f"Error: A directory named '{sys.argv[2]} already exists!'", style="red")
                else:
                    if not new_path.exists():
                        Path.rename(current_path, new_path)
                        screen.print(f"File '{sys.argv[1]}' successfully renamed to '{sys.argv[2]}'!",
                                     style="green")
                    else:
                        screen.print(f"Error: A file named '{sys.argv[2]}' already exists!", style="red")
            else:
                screen.print(f"Error: '{current_path}' not found!", style="red")
        else:
            screen.print("are you kidding me? These two names are equal!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
