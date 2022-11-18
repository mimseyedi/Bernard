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
    from rich.console import Console
    screen = Console()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        # Using the command 'clear' or 'cls' according to the type of operating system.
        subprocess.call('clear' if os.name == 'posix' else 'cls')
        while True:
            for row in range(os.get_terminal_size()[1]):
                for col in range(os.get_terminal_size()[0]):
                    rv = random.randint(1, 5)
                    # Color the characters.
                    if rv == 1:
                        # $ sign will be gray.
                        print('\033[90m$\033[92m', end='')
                    elif rv == 2:
                        # Number nine will be gray.
                        print('\033[90m9\033[92m', end='')
                    elif rv == 3:
                        # ? sign will be gray.
                        print('\033[90m?\033[92m', end='')
                    elif rv == 4:
                        # Number zero will be green.
                        print('\033[92m0\033[92m', end='')
                    else:
                        # Number one will be green.
                        print('\033[92m1\033[92m', end='')
                print()
            time.sleep(0.1)
            subprocess.call('clear' if os.name == 'posix' else 'cls')

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("Do you want hide your screen? like matrix?", style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
