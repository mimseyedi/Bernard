import sys
import hashlib
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must enter an input!", style="red")
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("You can convert an input to sha256 with the hash command.", style="green")
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        sha_256 = hashlib.sha256()
        sha_256.update(str(sys.argv[1]).encode('UTF-8'))
        hash_output = sha_256.hexdigest()
        screen.print(hash_output)


if __name__ == "__main__":
    init()
