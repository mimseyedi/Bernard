import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must enter inputs!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the sort command you can sort numbers or letters.", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) >= 2 and sys.argv[1] != "-h":
        digit_type = True

        # Check all inputs is digit or not.
        for inp in sys.argv[1:]:
            if not inp.isdigit():
                digit_type = False

        # If all inputs is digit -> sorting by numbers.
        if digit_type:
            inputs_list = map(str, sorted(map(int, sys.argv[1:])))
            screen.print(', '.join(inputs_list))
        else:
            # Sorting by alphabet.
            screen.print(', '.join(sorted(sys.argv[1:])))


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
