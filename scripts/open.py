import sys
import platform
import subprocess
import webbrowser
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


# A function to detect whether the input is a url or not.
def is_url(url):
    domains = (".com", ".ir", ".org", ".me", ".net", ".co", ".xyz")
    if "http://" in url or "https://" in url or "www." in url or url.endswith(domains):
        return True
    return False


# A function to modify the url configuration.
def fix_url(url):
    if not url.startswith(("http://", "https://")):
        if url.startswith("www."):
            return "https://" + url
        else:
            return "https://www." + url
    return url


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must enter something to open!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the open command, you can open files or URLs with default or custom programs", style="green")

    # If the script is called with any parameter except -h.
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        # If input is url ->
        if is_url(sys.argv[1]):
            webbrowser.open(fix_url(sys.argv[1]))
        # Otherwise, it opens the file with the default program by the command associated with each of the operating systems.
        else:
            # macOS:
            if platform.system() == "Darwin":
                subprocess.call(["open", sys.argv[1]])
            # Linux:
            elif platform.system() == "Linux":
                subprocess.call(["xdg-open", sys.argv[1]])
            # Windows:
            elif platform.system() == "Windows":
                subprocess.call(["start", sys.argv[1]])

    # If the script is called with any parameter except -h.
    # The file will be opened on the Mac operating system by the imported program.
    elif len(sys.argv) == 3 and sys.argv[1] != "-h":
        if is_url(sys.argv[1]):
            webbrowser.open(fix_url(sys.argv[1]))
        else:
            subprocess.call(["open", "-a", sys.argv[2], sys.argv[1]])

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
