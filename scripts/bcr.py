import os
import sys
import subprocess
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


# Get the main path.
path_of_file = Path(__file__)
base_path = path_of_file.parent.parent
scripts_path = path_of_file.parent
BCS_path = Path(base_path, "BCS")


guide_message = """The bcr command allows you to run Bernard Commands Script files.

Parameters:
-x run saved scripts in BCS directory
-d run without break
-xd run saved scripts in BCS directory without break"""


def command_reader(bcs_file_path, debug_mode=True):
    with open(bcs_file_path, "r") as bcs_file:
        bcs = list(map(lambda x: x.strip(), bcs_file.readlines()))

    scripts = [script[:-3] for script in os.listdir(scripts_path) if script.endswith(".py")]

    for command in bcs:
        if command.split()[0] in scripts:
            command, run_list = command.split(), [sys.executable]
            for index in range(len(command)):
                if index == 0:
                    run_list.append(Path(scripts_path, command[index] + ".py").__str__())
                else:
                    run_list.append(command[index])

            output = subprocess.run(run_list, capture_output=True).stdout.decode("UTF-8").strip()

            if output.startswith("Error:"):
                screen.print('(' + ' '.join(command) + ')', style="yellow")
                screen.print('  └──' + output, style="red")
                if debug_mode:
                    break
            else:
                subprocess.run(run_list)
        else:
            screen.print('(' + command.split()[0] + ')', style="yellow")
            screen.print(f"  └──Error: Script '{command.split()[0]}' not found!", style="red")
            if debug_mode:
                break


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a Bernard Commands Script!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        BCS_file_path = Path(os.getcwd(), sys.argv[1])
        if BCS_file_path.exists():
            if BCS_file_path.is_file():
                if sys.argv[1].endswith(".bcs"):
                    command_reader(BCS_file_path)
                else:
                    screen.print("Error: You must select a Bernard Commands Script file!", style="red")
            else:
                screen.print("Error: You must select a file!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[1]}' not found!", style="red")

    elif len(sys.argv) == 3 and sys.argv[1] == "-x":
        if BCS_path.exists():
            if Path(BCS_path, sys.argv[2]).exists():
                if Path(BCS_path, sys.argv[2]).is_file():
                    if sys.argv[2].endswith(".bcs"):
                        command_reader(Path(BCS_path, sys.argv[2]))
                    else:
                        screen.print("Error: You must select a Bernard Commands Script file!", style="red")
                else:
                    screen.print("Error: You must select a file!", style="red")
            else:
                screen.print(f"Error: '{sys.argv[2]}' not found!", style="red")
        else:
            screen.print("Error: BCS directory not found!", style="red")

    elif len(sys.argv) == 3 and sys.argv[1] == "-d":
        BCS_file_path = Path(os.getcwd(), sys.argv[2])
        if BCS_file_path.exists():
            if BCS_file_path.is_file():
                if sys.argv[2].endswith(".bcs"):
                    command_reader(BCS_file_path, debug_mode=False)
                else:
                    screen.print("Error: You must select a Bernard Commands Script file!", style="red")
            else:
                screen.print("Error: You must select a file!", style="red")
        else:
            screen.print(f"Error: '{sys.argv[2]}' not found!", style="red")

    elif len(sys.argv) == 3 and sys.argv[1] == "-xd":
        if BCS_path.exists():
            if Path(BCS_path, sys.argv[2]).exists():
                if Path(BCS_path, sys.argv[2]).is_file():
                    if sys.argv[2].endswith(".bcs"):
                        command_reader(Path(BCS_path, sys.argv[2]), debug_mode=False)
                    else:
                        screen.print("Error: You must select a Bernard Commands Script file!", style="red")
                else:
                    screen.print("Error: You must select a file!", style="red")
            else:
                screen.print(f"Error: '{sys.argv[2]}' not found!", style="red")
        else:
            screen.print("Error: BCS directory not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
