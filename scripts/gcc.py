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


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        # Using 'gcc': GNU Compiler Collection command from Unix terminal.
        # https://gcc.gnu.org/
        subprocess.run(["gcc"])

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the gcc command, you can compile C codes.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        # Passing parameters to gcc command switches.
        gcc_arg = " ".join(sys.argv[1:])
        os.system(f"gcc {gcc_arg}")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
