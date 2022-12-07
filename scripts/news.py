import subprocess
import sys

try:
     import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
     import requests

try:
     from bs4 import BeautifulSoup
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
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

# default news
        URL = ("https://www.shahrekhabar.com/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1")
        page = requests.get(URL)
        soap= BeautifulSoup(page.text,"html.parser")
        titles=soap.find_all("a",class_="alink nlinkb1",target="_blank",href=True)

        screen.print("tech news for default")

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")
# tech news
    elif len(sys.argv) == 2 and sys.argv[1] == "-tech":
        URL = ("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%81%D9%86%D8%A7%D9%88%D8%B1%DB%8C")
        page = requests.get(URL)
        soap = BeautifulSoup(page.text, "html.parser")
        titles = soap.find_all("a", class_="alink nlinkb1", target="_blank", href=True)

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")

# sport news
    elif len(sys.argv) == 2 and sys.argv[1] == "-sport":
        URL = ("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C")
        page = requests.get(URL)
        soap = BeautifulSoup(page.text, "html.parser")
        titles = soap.find_all("a", class_="alink nlinkb1", target="_blank", href=True)

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")

# politics news
    elif len(sys.argv) == 2 and sys.argv[1] == "-politics":
        URL = ("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C")
        page = requests.get(URL)
        soap = BeautifulSoup(page.text, "html.parser")
        titles = soap.find_all("a", class_="alink nlinkb1", target="_blank", href=True)

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")

# economic news
    elif len(sys.argv) == 2 and sys.argv[1] == "-eco":
        URL = ("https://www.shahrekhabar.com/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%DB%8C")
        page = requests.get(URL)
        soap = BeautifulSoup(page.text, "html.parser")
        titles = soap.find_all("a", class_="alink nlinkb1", target="_blank", href=True)

        for title in titles:
            screen.print(f"Title: {title.text}")
            screen.print(f"link:{title['href']}\n")

#hints for user to use this scripts
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
         screen.print('show the last news', style="green")
         screen.print('To read Last news only type: news', style="green")
         screen.print('To read tech news type: news -tech', style="green")
         screen.print('To read sport news type: news -sport', style="green")
         screen.print('To read politics news type: news -politics', style="green")
         screen.print('To read economic news type: news -eco', style="green")
    else:
         screen.print("Error: Unknown parameters!", style="red")
    pass

#executable main part
if __name__ == "__main__":
    init()
