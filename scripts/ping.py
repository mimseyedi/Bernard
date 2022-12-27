import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


guide_message = """Send ICMP ECHO_REQUEST packets to network hosts

Parameters:
-c packets count -> example: ping -c 10 4.2.2.4"""


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a Network!", style="red")

    # If the script is called with any parameter except -h.
    # Passing parameters to ping command switches.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if sys.argv[1].split('.')[0].isdigit():
            subprocess.run(['ping', '-c', '5', sys.argv[1]])
        else:
            screen.print("Error: Unknown parameters!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -c parameter.
    # Pattern: ping -c 10 4.2.2.4
    elif len(sys.argv) == 4 and sys.argv[1] == "-c":
        subprocess.run(['ping', '-c', sys.argv[2], sys.argv[3]])

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
