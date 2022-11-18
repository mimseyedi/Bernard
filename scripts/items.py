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


guide_message = """With the items command, you can see all items in directories.

Parameters:
-a show all items include hidden files
"""


# A function to display two columns of items in dir.
def show_items(items: list):
    max_length = 0
    for item in items:
        max_length = len(item) if len(item) > max_length else max_length

    index = 0
    while index < len(items):
        space = " " * (max_length - len(items[index]))
        screen.print(items[index], end=f"{space} \t")
        if index + 1 < len(items):
            screen.print(items[index + 1])
        index += 2

    if len(items) % 2 != 0: print()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        # Take all items in current directory.
        items = os.listdir(os.getcwd())
        # Removing hidden files.
        for item in items:
            if item.startswith("."):
                items.remove(item)
        # Sorting items by alphabet.
        show_items(sorted(items))

    # If the script is called with the -a parameter.
    # Show all items include hidden files.
    elif len(sys.argv) == 2 and sys.argv[1] == "-a":
        items = os.listdir(os.getcwd())
        show_items(sorted(items))

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
