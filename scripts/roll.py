import sys
import random
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


guide_message = """The roll command allows you to generate one or more random numbers.

Parameters:
-r start-point end-point -> exmaple: roll -r 1 20
-i returns a random number between 0 and 1
-m returns some random number -> exmaple: roll -m 10 20 3
-s shuffle the list -> exmaple: roll -s Sara Jax John Mary ..."""


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        # Generating a random number between 1 and 100.
        screen.print(random.randint(1, 100))

    # If the script is called with the -i parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-i":
        # Generating a random number between 0 and 1.
        screen.print(random.random())

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -r parameter.
    # Generating a random number between 2 numbers.
    # Pattern: roll -r 1 20
    elif len(sys.argv) == 4 and sys.argv[1] == "-r":
        if sys.argv[2].isdigit() and sys.argv[3].isdigit():
            screen.print(random.randint(int(sys.argv[2]), int(sys.argv[3])))
        else:
            screen.print("Error: Your entries must digits!", style="red")

    # If the script is called with the -m parameter.
    # Generating a random number between two numbers with an arbitrary number.
    # Pattern: roll -m 1 20 3
    elif len(sys.argv) == 5 and sys.argv[1] == "-m":
        if sys.argv[2].isdigit() and sys.argv[3].isdigit() and sys.argv[4].isdigit():
            screen.print(random.choices(range(int(sys.argv[2]), int(sys.argv[3])), k=int(sys.argv[4])))
        else:
            screen.print("Error: Your entries must digits!", style="red")

    # If the script is called with the -s parameter.
    # Shuffling the inputs.
    # Pattern: roll -s 1 2 3 4 5 6 ...
    elif len(sys.argv) >= 2 and sys.argv[1] == "-s":
        entries_list = sys.argv[2:]
        random.shuffle(entries_list)
        screen.print(', '.join(entries_list))

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
