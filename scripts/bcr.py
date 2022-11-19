import os
import sys
import subprocess
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


# Get the main path.
path_of_file = Path(__file__)
base_path = path_of_file.parent.parent
scripts_path = path_of_file.parent
BCS_path = Path(base_path, "BCS")


guide_message = """
"""


def command_reader(bcs_file_path):
    with open(bcs_file_path, "r") as bcs_file:
        bcs = list(map(lambda x: x.strip(), bcs_file.readlines()))

    scripts = [script[:-3] for script in os.listdir(scripts_path) if script.endswith(".py")]

    for command in bcs:
        if command.split()[0] in scripts:
            command, run_list = command.split(), ["python"]
            for index in range(len(command)):
                if index == 0: run_list.append(Path(scripts_path, command[index] + ".py").__str__())
                else:
                    run_list.append(command[index])

            output = subprocess.run(run_list, capture_output=True).stdout.decode("UTF-8").strip()

            if output.startswith("Error:"):
                screen.print(output, style="red")
                break
            else:
                subprocess.run(run_list)
        else:
            screen.print(f"Error: Script '{command.split()[0]}' not found!", style="red")
            break


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a Bernard Command Script!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if BCS_path.exists():
            if Path(BCS_path, sys.argv[1]).exists():
                if Path(BCS_path, sys.argv[1]).is_file():
                    if sys.argv[1].endswith(".bcs"):
                        command_reader(Path(BCS_path, sys.argv[1]))
                    else:
                        screen.print("Error: You must select a Bernard Command Script file!", style="red")
                else:
                    screen.print("Error: You must select a file!", style="red")
            else:
                screen.print(f"Error: '{sys.argv[1]}' not found!", style="red")
        else:
            screen.print("Error: BCS directory not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
