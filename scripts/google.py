import sys
import webbrowser
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()
try:
    import bs4
except ImportError as package:
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"], stdout=subprocess.DEVNULL)
try:
    import googlesearch
except ImportError as package:
    subprocess.run([sys.executable, "-m", "pip", "install", "google"], stdout=subprocess.DEVNULL)
finally:
    import googlesearch


guide_message = """With the google command, you can experience a quick search in Google!

Parameters:
-c set count of results -> example: google -c 5 <query>
-o open first link in browser
-t open top 5 links in browser"""


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must enter a query!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except ("-h", "-c", "-o", "-t").
    # Pattern: google What is Python?
    elif len(sys.argv) >= 2 and sys.argv[1] not in ["-h", "-c", "-o", "-t"]:
        query = ' '.join(sys.argv[1:])
        for link in googlesearch.search(query, tld="co.in", num=10, stop=10, pause=2):
            screen.print(link)

    # If the script is called with the -c parameter.
    # It will display the number of links entered.
    # Pattern: google -c 7 What is Python?
    elif len(sys.argv) >= 4 and sys.argv[1] == "-c":
        if sys.argv[2].isdigit():
            query, count = ' '.join(sys.argv[3:]), int(sys.argv[2])
            for link in googlesearch.search(query, tld="co.in", num=count, stop=count, pause=2):
                screen.print(link)
        else:
            screen.print("Error: third parameter must be a digit!", style="red")

    # If the script is called with the -o parameter.
    # Open first link.
    elif len(sys.argv) >= 3 and sys.argv[1] == "-o":
        query = ' '.join(sys.argv[2:])
        link = googlesearch.search(query, tld="co.in", num=1, stop=1, pause=2)
        webbrowser.open(list(link)[0])

    # If the script is called with the -t parameter.
    # Open top 5 links.
    elif len(sys.argv) >= 3 and sys.argv[1] == "-t":
        query = ' '.join(sys.argv[2:])
        for link in googlesearch.search(query, tld="co.in", num=5, stop=5, pause=2):
            webbrowser.open(link)

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
