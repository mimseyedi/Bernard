import sys
import warnings
import webbrowser
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()
try:
    import wikipedia
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "wikipedia"], stdout=subprocess.DEVNULL)
    import wikipedia


guide_message = """With the wiki command, you can access to Wikipedia information about things.

Parameters:
-f full information
-s short information
-o open wikipedia page in browser"""


# A function to search and access information available in Wikipedia on the selected topic.
def get_summary(subject, sentence="full"):
    warnings.filterwarnings("ignore")
    if sentence == "full":
        try:
            return wikipedia.summary(subject)
        except wikipedia.exceptions.WikipediaException:
            suggest = wikipedia.search(subject)
            if len(suggest) > 0:
                return "cant find the subject in wikipedia!\ndid you mean?", suggest
            return "cant find the subject in wikipedia!"
    try:
        return wikipedia.summary(subject, sentences=int(sentence))
    except wikipedia.exceptions.WikipediaException:
        suggest = wikipedia.search(subject)
        if len(suggest) > 0:
            return "cant find the subject in wikipedia!\ndid you mean?", suggest
        return "cant find the subject in wikipedia!"


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: you must enter a subject!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with the -o parameter.
    # Open the Wikipedia page link.
    elif len(sys.argv) >= 2 and sys.argv[1] == "-o":
        result = wikipedia.search(' '.join(sys.argv[2:]))
        if len(result) > 0:
            wiki_page = wikipedia.WikipediaPage(result[0]).url
            webbrowser.open(wiki_page)
        else:
            screen.print("Error: cant find the subject in wikipedia!", style="red")


    # If the script is called with the -f parameter.
    # View full topic information on Wikipedia.
    elif len(sys.argv) >= 3 and sys.argv[1] == "-f":
        result = get_summary(' '.join(sys.argv[2:]))
        if type(result) == tuple:
            screen.print(f"Error: {result[0]}", style="red")
            screen.print('\n'.join(result[1]), style="green")
        else:
            if result == "cant find the subject in wikipedia!":
                screen.print(f"Error: {result}", style="red")
            else:
                screen.print(result)

    # If the script is called with the -s parameter.
    # View short topic information on Wikipedia.
    elif len(sys.argv) >= 3 and sys.argv[1] == '-s':
        result = get_summary(' '.join(sys.argv[2:]), 2)
        if type(result) == tuple:
            screen.print(f"Error: {result[0]}", style="red")
            screen.print('\n'.join(result[1]), style="green")
        else:
            if result == "cant find the subject in wikipedia!":
                screen.print(f"Error: {result}", style="red")
            else:
                screen.print(result)

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
