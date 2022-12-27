import os
import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        subprocess.run([sys.executable])

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the py command, you can compile Python3 codes and access to Python3 shell.", style="green")

    # If the script is called with any parameter except -h.
    # Passing parameters to python command switches.
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        py_arg = " ".join(sys.argv[1:])
        os.system(f"{sys.executable} {py_arg}")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
