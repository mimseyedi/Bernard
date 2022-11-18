import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """With the cal command you can see the calendar!

Parameters:
-y Year view"""


# Start-point.
def init():
    # If the script is called alone.
    # By default, the calendar is printed monthly.
    if len(sys.argv) == 1:
        # Using 'cal' command from Unix terminal.
        subprocess.run(["cal"])

    # If the script is called with the -y parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-y":
        subprocess.run(["cal", "-y"])

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
