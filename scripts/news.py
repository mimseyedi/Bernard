import os
import sys
import subprocess
try:
     import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
     import requests
try:
     from bs4 import BeautifulSoup
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"], stdout=subprocess.DEVNULL)
finally:
    from bs4 import BeautifulSoup
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


guide_message = """By using the news command, you can watch the latest news of the day in various topics.

Parameters:
-tech -> show the latest technology news
-sport -> show the latest sports news
-eco -> show the latest economic news
-politics -> show the latest political news"""


# Get news from https://www.shahrekhabar.com
def get_news(url: str, count=10):
    page = requests.get(url)
    soap = BeautifulSoup(page.text, "html.parser")
    titles = soap.find_all("a", class_="alink nlinkb1", target="_blank", href=True)

    for title in titles[:count]:
        for _ in range(os.get_terminal_size()[0]):
            print('-', end='')
        screen.print(f"Title: {title.text}")
        screen.print(f"  └──link: {title['href']}")
    for _ in range(os.get_terminal_size()[0]):
        print('-', end='')
    print()


# Start-point.
def init():
    # If the script is called alone.
    # Default news.
    if len(sys.argv) == 1:
        screen.print("Technology news as default:")
        get_news("https://www.shahrekhabar.com/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1")

    # Tech news.
    elif len(sys.argv) == 2 and sys.argv[1] == "-tech":
        get_news("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%81%D9%86%D8%A7%D9%88%D8%B1%DB%8C")

    # Sport news.
    elif len(sys.argv) == 2 and sys.argv[1] == "-sport":
        get_news("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C")

    # Politics news.
    elif len(sys.argv) == 2 and sys.argv[1] == "-politics":
        get_news("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C")

    # Economic news.
    elif len(sys.argv) == 2 and sys.argv[1] == "-eco":
        get_news("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%DB%8C")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
         screen.print(guide_message, style="green")

    # If none of these.
    else:
         screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
