import os
import sys
import subprocess
try:
    import googletrans
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "googletrans==3.1.0a0"], stdout=subprocess.DEVNULL)
finally:
    translator = googletrans.Translator()
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


guide_message = """With the trans command, you can translate words into different natural languages or receive a complete file with the translated output.

Parameters:
trans <word> <language> -> exmaple: trans hello persian
-d detect language
-f read file to translate
-fo translate file with .txt output
"""


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must enter something to translate!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) == 3 and sys.argv[1] not in ["-h", "-d", "-f", "-fo"]:
        try:
            translated_word = translator.translate(text=sys.argv[1], dest=sys.argv[2]).text
            screen.print(translated_word, style="green")
        except ValueError:
            screen.print("Error: Invalid destination language!", style="red")

    elif len(sys.argv) == 3 and sys.argv[1] == "-d":
        language = translator.detect(sys.argv[2]).lang
        screen.print(f"Language is {language}", style="green")

    elif len(sys.argv) == 4 and sys.argv[1] == "-f":
        file = f"{os.getcwd()}/{sys.argv[2]}" if sys.argv[2] in os.listdir() else sys.argv[2]
        if os.path.exists(file):
            if os.path.isfile(file):
                if file.endswith(".txt"):
                    with open(file, "r") as t_file:
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

    elif len(sys.argv) == 5 and sys.argv[1] == "-fo":
        file = f"{os.getcwd()}/{sys.argv[2]}" if sys.argv[2] in os.listdir() else sys.argv[2]
        if os.path.exists(file):
            if os.path.isfile(file):
                if file.endswith(".txt"):
                    with open(file, "r") as t_file:
                        try:
                            translated_text = translator.translate(text=t_file.read(), dest=sys.argv[3]).text
                            if not os.path.exists(f"{os.getcwd()}/{sys.argv[4]}"):
                                if sys.argv[4].endswith(".txt"):
                                    with open(f"{os.getcwd()}/{sys.argv[4]}", "w") as dest_file:
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

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
