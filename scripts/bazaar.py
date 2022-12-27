import os
import sys
import subprocess
try:
    import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
    import requests
try:
    from bs4 import BeautifulSoup
except ImportError as package:
    subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"], stdout=subprocess.DEVNULL)
    from bs4 import BeautifulSoup
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


def fix_price(price: str):
    digits = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5',
              '۶': '6', '۷': '7', '۸': '8', '۹': '9', '٫': ''}

    english_price, status = '', False
    for items in price.split():
        for digit in items:
            if digit in digits.keys():
                english_price += digits[digit]
            else:
                break
        english_price += " "

    final_price = english_price.split()

    return int(final_price[0]) if final_price else float('inf')



def search_in_bazaar(item: str, count: int=10, best_price: bool=False):
    try:
        request = requests.get(f"https://torob.com/search/?query={item}")
        soup = BeautifulSoup(request.text, "html.parser")

        links = soup.find_all("a", class_="jsx-2834913897", href=True)
        if len(links) > 0:
            titles = soup.find_all("h2", class_="jsx-2834913897 name")

            prices = []
            for item in links:
                item_request = requests.get(f"https://torob.com{item['href']}")
                price_soup = BeautifulSoup(item_request.text, "html.parser")
                price = price_soup.find("div", class_="jsx-478367150 price")
                prices.append(price.text)

            int_prices = []
            for p in prices:
                int_prices.append(fix_price(p))

            min_price, min_index = int_prices[0], 0
            for index in range(len(int_prices)):
                if int_prices[index] < min_price:
                    min_price = int_prices[index]
                    min_index = index

            if best_price:
                for _ in range(os.get_terminal_size()[0]):
                    print('-', end='')
                screen.print(f"Title: {titles[min_index].text}")
                string_price = "{:,}".format(fix_price(prices[min_index]))
                screen.print(f"  └── Price: {string_price} Toman", style="red")
                screen.print(f"  └── Link: https://torob.com{links[min_index]['href']}", style="yellow")
            else:
                for index in range(count):
                    for _ in range(os.get_terminal_size()[0]):
                        print('-', end='')
                    screen.print(f"Title: {titles[index].text}")
                    string_price = "{:,}".format(fix_price(prices[index]))
                    screen.print(f"  └── Price: {string_price} Toman", style="red")
                    screen.print(f"  └── Link: https://torob.com{links[index]['href']}", style="yellow")

            for _ in range(os.get_terminal_size()[0]):
                print('-', end='')
            print()
        else:
            screen.print("Error: Your request is not available in the market!", style="red")

    except requests.exceptions.ConnectionError:
        screen.print("Error: No internet connection!", style="red")


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        pass

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    elif len(sys.argv) >= 2 and sys.argv[1] not in ["-h", "-c", "-bp"]:
        search_in_bazaar(sys.argv[1:])

    elif len(sys.argv) >= 4 and sys.argv[1] == "-c":
        if sys.argv[2].isdigit():
            search_in_bazaar(sys.argv[3:], count=int(sys.argv[2]))
        else:
            screen.print("Error: You must use a number for the third parameter!", style="red")

    elif len(sys.argv) >= 3 and sys.argv[1] == "-bp":
        search_in_bazaar(sys.argv[2:], best_price=True)

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
