import os
import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        subprocess.run([sys.executable])
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the py command, you can compile Python3 codes and access to Python3 shell.", style="green")
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        py_arg = " ".join(sys.argv[1:])
        os.system(f"{sys.executable} {py_arg}")


if __name__ == "__main__":
    init()
