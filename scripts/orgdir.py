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


guide_message = """With the orgdir command, you can organize and sort your directories in two classic or custom ways.

Parameters:
-c classic way -> example: orgdir -c
-x custom way -> exmaple: orgdir -x .pdf Doc"""


# A function to check the availability of the file with the selected suffix.
def check_files(suffix):
    for item in os.scandir():
        if item.name.endswith(suffix) and not item.is_dir():
            return True
    return False


# A function to categorize files in a classic way.
def pick_files(files):
    categories = {'DOCUMENTS': ['.pdf', '.txt', '.csv', '.rtf', '.docx'],
                  'AUDIO': ['.m4a', '.m4b', '.mp3', '.wav'],
                  'VIDEOS': ['.mov', '.avi', '.mp4'],
                  'IMAGES': ['.jpeg', '.jpg', '.png', '.gif'],
                  'CODES': ['.c', '.cpp', '.py', '.js', '.cs', '.php', '.html', '.css', '.json'],
                  'COMPRESSED': ['.rar', '.zip']}

    for category, suffixes in categories.items():
        for suffix in suffixes:
            if suffix == files:
                return category

    return 'MISC'


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must using parameters!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -c parameter.
    # Organize the directory in the classical way.
    elif len(sys.argv) == 2 and sys.argv[1] == "-c":
        current_items = os.listdir()
        for item in os.scandir():
            if item.is_dir(): continue

            file_path = Path(item)
            file_type = file_path.suffix.lower()
            directory = pick_files(file_type)
            dir_path = Path(directory)

            if not dir_path.is_dir(): dir_path.mkdir()

            file_path.rename(dir_path.joinpath(file_path))

        if current_items != os.listdir():
            screen.print("The organizing operation was successfully completed!", style="green")
        else:
            screen.print("Error: This is an organized directory without the need to organize!", style="red")

    # Directory organization by manual method.
    # Pattern: orgdir -x .py Python
    elif len(sys.argv) == 4 and sys.argv[1] == "-x":
        if check_files(sys.argv[2]):
            for item in os.scandir():
                if item.is_dir() or not item.name.endswith(sys.argv[2]):
                    continue

                file_path = Path(item)
                dir_path = Path(sys.argv[3])

                if not dir_path.is_dir(): dir_path.mkdir()

                file_path.rename(dir_path.joinpath(file_path))

            screen.print("The organizing operation was successfully completed!", style="green")
            screen.print(f"All '{sys.argv[2]}' files move to '{sys.argv[3]}' directory!", style="green")
        else:
            screen.print("Error: No files with the specified suffix were found to organize!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
