import os
import sys
import time
import random
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def init():
    if len(sys.argv) == 1:
        subprocess.run(["clear"])
        while True:
            for row in range(os.get_terminal_size()[1]):
                for col in range(os.get_terminal_size()[0]):
                    rv = random.randint(1, 5)
                    if rv == 1:
                        print('\033[0m$\033[92m', end='')
                    elif rv == 2:
                        print('\033[0m9\033[92m', end='')
                    elif rv == 3:
                        print('\033[0m?\033[92m', end='')
                    elif rv == 4:
                        print('\033[92m0\033[92m', end='')
                    else:
                        print('\033[92m1\033[92m', end='')
                print()
            time.sleep(0.1)
            subprocess.run(["clear"])

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("Do you want hide your screen? like matrix?", style="green")

    else:
        screen.print("Error: Unknown parameters!", style="red")

if __name__ == "__main__":
    init()
