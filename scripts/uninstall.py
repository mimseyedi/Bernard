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
    path_of_file = os.path.abspath(__file__).split("/")
    scripts_path = '/'.join(path_of_file[1:-1])

    if len(sys.argv) == 1:
        screen.print("Error: You must write a script name!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the uninstall command, you can uninstall programs or scripts stored in "
                      "scripts directory.", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if os.path.exists(f"/{scripts_path}/{sys.argv[1]}.py"):
            ask_to_uninstall = input("Are you sure? (y/n): ").lower()
            if ask_to_uninstall == "y":
                os.remove(f"/{scripts_path}/{sys.argv[1]}.py")
                screen.print(f"'{sys.argv[1]}' script was successfully uninstalled!", style="green")
        else:
            screen.print(f"Error: '{sys.argv[1]}' script not found!", style="red")


if __name__ == "__main__":
    init()
