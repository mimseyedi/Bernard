import os
import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


guide_message = """With the items command, you can see all items in directories.

Parameters:
-c show clean items
-n count all items
-nc count clean items"""


def show_items(items: list):
    max_length = 0
    for item in items:
        max_length = len(item) if len(item) > max_length else max_length

    end_point = len(items) if max_length % 2 == 0 else len(items) - 1

    index = 0
    while index < end_point:
        space = " " * (max_length - len(items[index]))
        screen.print(items[index], end=f"{space} \t")
        screen.print(items[index + 1])
        index += 2

    if len(items) % 2 != 0:
        screen.print(items[-1])


def init():
    if len(sys.argv) == 1:
        items = os.listdir(os.getcwd())

        for item in items:
            if item.startswith("."):
                items.remove(item)

        show_items(items)

    elif len(sys.argv) == 2 and sys.argv[1] == "-a":
        items = os.listdir(os.getcwd())
        show_items(items)

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
