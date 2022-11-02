import sys
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


guide_message = """Send ICMP ECHO_REQUEST packets to network hosts

Parameters:
-c packets count -> example: ping -c 10 4.2.2.4"""


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must select a Network!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if sys.argv[1].split('.')[0].isdigit():
            subprocess.run(['ping', '-c', '5', sys.argv[1]])
        else:
            screen.print("Error: Unknown parameters!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) == 4 and sys.argv[1] == "-c":
        subprocess.run(['ping', '-c', sys.argv[2], sys.argv[3]])

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
