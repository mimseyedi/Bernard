import sys
import hashlib
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
        screen.print("Error: You must enter an input!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("You can convert an input to sha256 with the hash command.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        sha_256 = hashlib.sha256()
        sha_256.update(str(sys.argv[1]).encode('UTF-8'))
        hash_output = sha_256.hexdigest()
        screen.print(hash_output)


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
