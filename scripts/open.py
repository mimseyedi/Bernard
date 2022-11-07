import os
import sys
import subprocess
import webbrowser
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    screen = Console()


def is_url(url):
    domains = (".com", ".ir", ".org", ".me", ".net", ".co", ".xyz")
    if "http://" in url or "https://" in url or "www." in url or url.endswith(domains):
        return True
    return False


def fix_url(url):
    if not url.startswith(("http://", "https://")):
        if url.startswith("www."):
            return "https://" + url
        else:
            return "https://www." + url
    return url


def init():
    if len(sys.argv) == 1:
        screen.print("Error: You must enter something to open!", style="red")

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print("With the open command, you can open files or URLs with default or custom programs", style="green")

    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        if is_url(sys.argv[1]):
            webbrowser.open(fix_url(sys.argv[1]))
        else:
            subprocess.call(["open", sys.argv[1]])

    elif len(sys.argv) == 3 and sys.argv[1] != "-h":
        if is_url(sys.argv[1]):
            webbrowser.open(fix_url(sys.argv[1]))
        else:
            subprocess.call(["open", "-a", sys.argv[2], sys.argv[1]])

    else:
        screen.print("Error: Unknown parameters!", style="red")


if __name__ == "__main__":
    init()
