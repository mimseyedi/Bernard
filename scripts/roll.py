import sys
import random
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """The roll command allows you to generate one or more random numbers.

Parameters:
-r start-point end-point -> exmaple: roll -r 1 20
-i returns a random number between 0 and 1
-m returns some random number -> exmaple: roll -m 10 20 3
-s shuffle the list -> exmaple: roll -s Sara Jax John Mary ..."""


def init():
    if len(sys.argv) == 1:
        screen.print(random.randint(1, 100))

    elif len(sys.argv) == 2 and sys.argv[1] == "-i":
        screen.print(random.random())

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) == 4 and sys.argv[1] == "-r":
        if sys.argv[2].isdigit() and sys.argv[3].isdigit():
            screen.print(random.randint(int(sys.argv[2]), int(sys.argv[3])))
        else:
            screen.print("Error: Your entries must digits!", style="red")

    elif len(sys.argv) == 5 and sys.argv[1] == "-m":
        if sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit():
            screen.print(random.choices(range(int(sys.argv[2]), int(sys.argv[3])), k=int(sys.argv[4])))
        else:
            screen.print("Error: Your entries must digits!", style="red")

    elif len(sys.argv) >= 2 and sys.argv[1] == "-s":
        entries_list = sys.argv[2:]
        random.shuffle(entries_list)
        screen.print(', '.join(entries_list))

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
