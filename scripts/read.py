import os
import sys
import subprocess
try:
    from rich.console import Console
    from rich.syntax import Syntax
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    from rich.syntax import Syntax
    screen = Console()


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must select a file to read!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the read command, you can read the files that are in text form, and they are highlighted in relation to their extension!",
                     style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        file = f"{os.getcwd()}/{sys.argv[1]}" if sys.argv[1] in os.listdir() else sys.argv[1]
        if os.path.exists(file):
            if os.path.isfile(file):
                language = {".c": "c", ".h": "c", ".cpp": "c++", ".hpp": "c++",
                            ".cs": "c#", ".css": "css", ".dart": "dart", ".go": "go",
                            ".html": "html", ".htm": "html", ".xhtml": "html", ".java": "java",
                            ".js": "js", ".jl": "julia", ".kt": "kotlin", ".m": "matlab",
                            ".php": "php", ".py": "python", ".rs": "rust", ".scss": "scss",
                            ".sql": "sql", ".swift": "swift", ".ts": "ts", ".vb": "vbnet",
                            ".xml": "xml", ".txt": "txt"}
                try:
                    with open(file, "r") as open_file:
                        screen.print(Syntax(open_file.read(), language[f".{file.split('.')[-1]}"],
                                            theme='monokai', line_numbers=True))
                except UnicodeDecodeError:
                    screen.print(f"Error: Cant read this file! -> '{sys.argv[1]}'", style="red")
                except KeyError:
                    screen.print(f"Error: Cant read this file! -> '{sys.argv[1]}'", style="red")
            else:
                screen.print("Error: You must select a file!", style="red")
        else:
            screen.print("Error: File can not found!", style="red")

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
