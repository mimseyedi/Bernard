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


def init():
    if len(sys.argv) == 1:
        items = os.listdir(os.getcwd())

        for item in items:
            if item.startswith("."):
                items.remove(item)

        show_items(sorted(items))

    elif len(sys.argv) == 2 and sys.argv[1] == "-a":
        items = os.listdir(os.getcwd())
        show_items(sorted(items))

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
