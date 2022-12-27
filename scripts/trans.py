import os
import sys
import subprocess
from pathlib import Path
try:
    import googletrans
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "googletrans==3.1.0a0"], stdout=subprocess.DEVNULL)
    import googletrans
finally:
    translator = googletrans.Translator()
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


guide_message = """With the trans command, you can translate words into different natural languages or receive a complete file with the translated output.

Parameters:
trans <word> <language> -> exmaple: trans hello persian
-d detect language
-f read file to translate
-fo translate file with .txt output
"""


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must enter something to translate!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except ("-h", "-d", "-f", "-fo").
    elif len(sys.argv) == 3 and sys.argv[1] not in ["-h", "-d", "-f", "-fo"]:
        try:
            translated_word = translator.translate(text=sys.argv[1], dest=sys.argv[2]).text
            screen.print(translated_word, style="green")
        except ValueError:
            screen.print("Error: Invalid destination language!", style="red")

    # If the script is called with the -d parameter.
    # Language recognition.
    elif len(sys.argv) == 3 and sys.argv[1] == "-d":
        language = translator.detect(sys.argv[2]).lang
        screen.print(f"Language is {language}", style="green")

    # If the script is called with the -f parameter.
    # Translate a file and display the translated text.
    elif len(sys.argv) == 4 and sys.argv[1] == "-f":
        file_path = Path(os.getcwd(), sys.argv[2])
        if file_path.exists():
            if file_path.is_file():
                if file_path.suffix == ".txt":
                    with open(file_path, "r") as t_file:
                        try:
                            translated_text = translator.translate(text=t_file.read(), dest=sys.argv[3]).text
                            screen.print(translated_text)
                        except ValueError:
                            screen.print("Error: Invalid destination language!", style="red")
                else:
                    screen.print("Error: You must select a .txt file!", style="red")
            else:
                screen.print("Error: You must select a file!", style="red")
        else:
            screen.print("Error: File can not found!", style="red")

    # If the script is called with the -fo parameter.
    # Translate a file and save the translated text in a new file.
    # Pattern: trans -fo file1.txt persian file2.txt
    elif len(sys.argv) == 5 and sys.argv[1] == "-fo":
        file_path = Path(os.getcwd(), sys.argv[2])
        if file_path.exists():
            if file_path.is_file():
                if file_path.suffix == ".txt":
                    with open(file_path, "r") as t_file:
                        try:
                            translated_text = translator.translate(text=t_file.read(), dest=sys.argv[3]).text
                            if not Path(os.getcwd(), sys.argv[4]).exists():
                                if sys.argv[4].endswith(".txt"):
                                    with open(Path(os.getcwd(), sys.argv[4]), "w") as dest_file:
                                        dest_file.write(translated_text)
                                        screen.print(f"The '{sys.argv[2]}' was successfully translated in the '{sys.argv[4]}'",
                                                     style="green")
                                else:
                                    screen.print("Error: The destination file must be .txt type!", style="red")
                            else:
                                screen.print("Error: A file with this name already exists!", style="red")
                        except ValueError:
                            screen.print("Error: Invalid destination language!", style="red")
                else:
                    screen.print("Error: You must select a .txt file!", style="red")
            else:
                screen.print("Error: You must select a file!", style="red")
        else:
            screen.print("Error: File can not found!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
