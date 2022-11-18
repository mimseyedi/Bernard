import os
import sys
import subprocess
from pathlib import Path
try:
    from rich.console import Console
    from rich.syntax import Syntax
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    from rich.syntax import Syntax
    screen = Console()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a file to read!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the read command, you can read the files that are in text form, and they are highlighted in relation to their extension!",
                     style="green")

    # If the script is called with any parameter except -h.
    # Reading text form files by the extensions listed in the dictionary.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        file_path = Path(os.getcwd(), sys.argv[1])
        if file_path.exists():
            if file_path.is_file():
                language = {".c": "c", ".h": "c", ".cpp": "c++", ".hpp": "c++",
                            ".cs": "c#", ".css": "css", ".dart": "dart", ".go": "go",
                            ".html": "html", ".htm": "html", ".xhtml": "html", ".java": "java",
                            ".js": "js", ".jl": "julia", ".kt": "kotlin", ".m": "matlab",
                            ".php": "php", ".py": "python", ".rs": "rust", ".scss": "scss",
                            ".sql": "sql", ".swift": "swift", ".ts": "ts", ".vb": "vbnet",
                            ".xml": "xml", ".txt": "txt"}
                try:
                    with open(file_path, "r") as open_file:
                        screen.print(Syntax(open_file.read(), language[file_path.suffix],
                                            theme='monokai', line_numbers=True))
                except UnicodeDecodeError:
                    screen.print(f"Error: Cant read this file! -> '{file_path.name}'", style="red")
                except KeyError:
                    screen.print(f"Error: Cant read this file! -> '{file_path.name}'", style="red")
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
