import os
import sys
import json
import shutil
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


guide_message = """With the hand command, you can keep files or directories in memory and select them to move.

Parameters:
get will be select current directory
    <file> <file> <file> ...
drop paste the selected all files
     paste with index of file
-w hand washing -> clean the memory!
-c remove one path by index
-z undo drop action"""


def add_last_drop(actions):
    hand["last_drop"].append(actions)
    with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
        json.dump(hand, hand_file)


def rem_last_drop():
    with open(f"/{scripts_path}/.hand_memory.json", "r") as hand_file:
        hand = json.load(hand_file)

    hand["last_drop"].clear()
    with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
        json.dump(hand, hand_file)


def init():
    global hand, scripts_path
    hand = {"items": [], "last_drop": []}
    path_of_file = os.path.abspath(__file__).split("/")
    scripts_path = '/'.join(path_of_file[1:-1])

    if not os.path.exists(f"/{scripts_path}/.hand_memory.json"):
        with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
            json.dump(hand, hand_file)
    else:
        with open(f"/{scripts_path}/.hand_memory.json", "r") as hand_file:
            hand = json.load(hand_file)

    for index, item in enumerate(hand["items"]):
        if not os.path.exists(item):
            hand["items"].remove(item)
    with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
        json.dump(hand, hand_file)

    if len(sys.argv) == 1:
        with open(f"/{scripts_path}/.hand_memory.json", "r") as hand_file:
            hand = json.load(hand_file)

        if len(hand["items"]) > 0:
            for index, item in enumerate(hand["items"]):
                if os.path.isfile(item):
                    screen.print(f"{index+1} - f - {item}")
                else:
                    screen.print(f"{index + 1} - d - {item}")
        else:
            screen.print("Message: Hand is empty!", style="yellow")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) == 2 and sys.argv[1] == "get":
        if os.getcwd() not in hand["items"]:
            hand["items"].append(os.getcwd())
            with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
                json.dump(hand, hand_file)
            screen.print(f"The hand successfully caught '{os.getcwd()}'", style="green")
        else:
            screen.print(f"Error: '{os.getcwd()}' already in the hand!", style="red")

    elif len(sys.argv) > 2 and sys.argv[1] == "get":
        for item in sys.argv[2:]:
            if os.path.exists(f"{os.getcwd()}/{item}"):
                if f"{os.getcwd()}/{item}" not in hand["items"]:
                    hand["items"].append(f"{os.getcwd()}/{item}")
                    screen.print(f"The hand successfully caught '{os.getcwd()}/{item}'", style="green")
                else:
                    screen.print(f"Error: '{os.getcwd()}/{item}' already in the hand!", style="red")
            else:
                screen.print(f"Error: '{os.getcwd()}/{item}' not found!", style="red")

        with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
            json.dump(hand, hand_file)

    elif len(sys.argv) == 2 and sys.argv[1] == "drop":
        last_action = []
        for item in hand["items"]:
            if os.path.isfile(item):
                if os.path.exists(f"{os.getcwd()}/{item.split('/')[-1]}"):
                    screen.print(f"Error: '{item.split('/')[-1]}' already exists!", style="red")
                else:
                    shutil.copyfile(item, f"{os.getcwd()}/{item.split('/')[-1]}")
                    screen.print(f"'{os.getcwd()}/{item.split('/')[-1]}' was copied successfully!", style="green")
                    last_action.append(f"{os.getcwd()}/{item.split('/')[-1]}")
            else:
                if os.path.exists(f"{os.getcwd()}/{item.split('/')[-1]}"):
                    screen.print(f"Error: '{item.split('/')[-1]}' already exists!", style="red")
                else:
                    shutil.copytree(item, f"{os.getcwd()}/{item.split('/')[-1]}")
                    screen.print(f"'{os.getcwd()}/{item.split('/')[-1]}' was copied successfully!", style="green")
                    last_action.append(f"{os.getcwd()}/{item.split('/')[-1]}")

        if len(last_action) > 0:
            add_last_drop(last_action)

    elif len(sys.argv) >= 3 and sys.argv[1] == "drop":
        indexes = sys.argv[2:]

        last_action = []
        for index in indexes:
            if index.isdigit():
                index = int(index) - 1
                if os.path.isfile(hand['items'][index]):
                    if os.path.exists(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}"):
                        screen.print(f"Error: '{os.getcwd()}/{hand['items'][index].split('/')[-1]}' already exists!",
                                     style="red")
                    else:
                        shutil.copyfile(hand['items'][index], f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}")
                        screen.print(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]} was copied successfully!",
                                      style="green")
                        last_action.append(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}")
                else:
                    if os.path.exists(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}"):
                        screen.print(f"Error: '{os.getcwd()}/{hand['items'][index].split('/')[-1]}' already exists!",
                                     style="red")
                    else:
                        shutil.copytree(hand['items'][index], f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}")
                        screen.print(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]} was copied successfully!",
                            style="green")
                        last_action.append(f"{os.getcwd()}/{hand['items'][index].split('/')[-1]}")
            else:
                screen.print(f"Error: Index is not a digit!", style="red")

        if len(last_action) > 0:
            add_last_drop(last_action)

    elif len(sys.argv) == 2 and sys.argv[1] == "-w":
        if len(hand["items"]) > 0:
            hand["items"].clear()
            with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
                json.dump(hand, hand_file)
            screen.print(f"The Hand washed successfully", style="green")
        else:
            screen.print("Message: Hand is empty!", style="yellow")

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

        for item in hand["items"]:
            if item in garbages:
                hand["items"].remove(item)
                screen.print(f"'{item}' removed successfully", style="green")

        with open(f"/{scripts_path}/.hand_memory.json", "w") as hand_file:
            json.dump(hand, hand_file)

    elif len(sys.argv) == 2 and sys.argv[1] == "-z":
        if len(hand["last_drop"]) > 0:
            for item in hand["last_drop"][-1]:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        os.remove(item)
                    else:
                        shutil.rmtree(item)
            screen.print("return to the previous position was applied", style="green")

        if len(hand["last_drop"]) == 0:
            screen.print("Error: The required action was not found", style="red")

        rem_last_drop()

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
