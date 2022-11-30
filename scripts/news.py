import subprocess

import requests
import sys
from bs4 import BeautifulSoup
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()

#my code lol
def init():
    if len(sys.argv) == 1:
        URL = ("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%81%D9%86%D8%A7%D9%88%D8%B1%DB%8C")
        page = requests.get(URL)
        soap= BeautifulSoup(page.text,"html.parser")
        titles=soap.find_all("a",class_="alink nlinkb1",target="_blank",href=True)

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")

#defualt part
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
         screen.print('show the last news', style="green")
    else:
         screen.print("Error: Unknown parameters!", style="red")
    pass

#executable main part
if __name__ == "__main__":
    init()
