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


def init():
    if len(sys.argv) == 1:
        subprocess.run(["gcc"])
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the gcc command, you can compile C codes.", style="green")
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        gcc_arg = " ".join(sys.argv[1:])
        os.system(f"gcc {gcc_arg}")


if __name__ == "__main__":
    init()
