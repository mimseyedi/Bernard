import os
import sys
import json
import shutil
from pathlib import Path
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


guide_message = """With the hand command, you can keep files or directories in memory and select them to move.

Parameters:
get will be select current directory
    <file> <file> <file> ...
drop paste the selected all files
     paste with index of file
-w hand washing -> clean the memory!
-c remove one path by index"""


# Start-point.
def init():
    # Get the main path and creating hand dict.
    global hand, scripts_path
    hand = {"items": []}
    path_of_file = Path(__file__)
    scripts_path = path_of_file.parent

    # If the hand memory file exists, it will read it, otherwise it will create it.
    if not Path(scripts_path, ".hand_memory.json").exists():
        with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
            json.dump(hand, hand_file)
    else:
        with open(Path(scripts_path, ".hand_memory.json"), "r") as hand_file:
            hand = json.load(hand_file)

    # Files or directories that do not exist will be deleted.
    # This operation is to control the items that are deleted after saving.
    for index, item in enumerate(hand["items"]):
        if not os.path.exists(item):
            hand["items"].remove(item)
    with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
        json.dump(hand, hand_file)

    # If the script is called alone.
    if len(sys.argv) == 1:
        with open(Path(scripts_path, ".hand_memory.json"), "r") as hand_file:
            hand = json.load(hand_file)

        # Display the contents of the hand along with the index and their type.
        if len(hand["items"]) > 0:
            for index, item in enumerate(hand["items"]):
                if os.path.isfile(item):
                    screen.print(f"{index+1} - f - {item}")
                else:
                    screen.print(f"{index + 1} - d - {item}")
        else:
            screen.print("Message: Hand is empty!", style="yellow")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the get parameter.
    # To get the entire contents of the current directory.
    # Pattern: hand get
    elif len(sys.argv) == 2 and sys.argv[1] == "get":
        if os.getcwd() not in hand["items"]:
            hand["items"].append(os.getcwd())
            with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
                json.dump(hand, hand_file)
            screen.print(f"The hand successfully caught '{os.getcwd()}'", style="green")
        else:
            screen.print(f"Error: '{os.getcwd()}' already in the hand!", style="red")

    # If the script is called with the get parameter.
    # To get the items individually.
    # hand get <item> <item> <item> ...
    elif len(sys.argv) > 2 and sys.argv[1] == "get":
        for item in sys.argv[2:]:
            item = Path(item)
            if Path(os.getcwd(), item.name).exists():
                if f"{Path(os.getcwd(), item.name)}" not in hand["items"]:
                    hand["items"].append(f"{Path(os.getcwd(), item.name)}")
                    screen.print(f"The hand successfully caught '{Path(os.getcwd(), item.name)}'", style="green")
                else:
                    screen.print(f"Error: '{Path(os.getcwd(), item.name)}' already in the hand!", style="red")
            else:
                screen.print(f"Error: '{Path(os.getcwd(), item.name)}' not found!", style="red")

        with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
            json.dump(hand, hand_file)

    # If the script is called with the drop parameter.
    # To copy all the contents inside the hand.
    # Pattern: hand drop
    elif len(sys.argv) == 2 and sys.argv[1] == "drop":
        for item in hand["items"]:
            item = Path(item)
            if item.is_file():
                if Path(os.getcwd(), item.name).exists():
                    screen.print(f"Error: '{item.name}' already exists!", style="red")
                else:
                    shutil.copyfile(item, item.name)
                    screen.print(f"'{item}' was copied successfully!", style="green")
            else:
                if Path(os.getcwd(), item.name).exists():
                    screen.print(f"Error: '{item.name}' already exists!", style="red")
                else:
                    shutil.copytree(item, item.name)
                    screen.print(f"'{item}' was copied successfully!", style="green")

    # If the script is called with the drop parameter.
    # To copy the contents inside the photo individually by index.
    # Pattern: hand drop 1 3 7 8 ...
    elif len(sys.argv) >= 3 and sys.argv[1] == "drop":
        indexes = sys.argv[2:]
        for index in indexes:
            if index.isdigit():
                index = int(index) - 1
                item = Path(hand["items"][index])
                if item.is_file():
                    if Path(os.getcwd(), item.name).exists():
                        screen.print(f"Error: '{item.name}' already exists!", style="red")
                    else:
                        shutil.copyfile(item, item.name)
                        screen.print(f"'{item.name}' was copied successfully!", style="green")
                else:
                    if Path(os.getcwd(), item.name).exists():
                        screen.print(f"Error: '{item.name}' already exists!", style="red")
                    else:
                        shutil.copytree(item, item.name)
                        screen.print(f"'{item.name}' was copied successfully!", style="green")
            else:
                screen.print(f"Error: Index is not a digit!", style="red")

    # If the script is called with the -w parameter.
    # Clearing all the contents inside the hand.
    elif len(sys.argv) == 2 and sys.argv[1] == "-w":
        if len(hand["items"]) > 0:
            hand["items"].clear()
            with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
                json.dump(hand, hand_file)
            screen.print(f"The Hand washed successfully", style="green")
        else:
            screen.print("Message: Hand is empty!", style="yellow")

    # If the script is called with the -c parameter.
    # Delete the contents of the hand individually by index.
    # Pattern: hand -c 1 3 4 ...
    elif len(sys.argv) >= 3 and sys.argv[1] == "-c":
        garbages = []
        for index in sys.argv[2:]:
            if index.isdigit():
                index = int(index)
                if index <= len(hand["items"]):
                    garbages.append(hand["items"][index - 1])
                else:
                    screen.print(f"Error: Index out of range!", style="red")
            else:
                screen.print(f"Error: Index is not a digit!", style="red")


        for item in garbages:
            if item in hand["items"]:
                hand["items"].remove(item)
                screen.print(f"'{item}' removed successfully", style="green")

        with open(Path(scripts_path, ".hand_memory.json"), "w") as hand_file:
            json.dump(hand, hand_file)

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
