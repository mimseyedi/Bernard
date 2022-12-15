#importing modules
import sys
import os
import subprocess

try:
     import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
     import requests

try:
     import json
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
     import json

try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()






# Start-point.
     # API base URL
Url = "https://api.openweathermap.org/data/2.5/weather?"

     # City Name
print("inter your city name: ")
CITY = input()

     # Your API key
API_KEY = "b07a711bdf19e559aca44794573fe62e"

     # updating the URL
URL = Url + "q=" + CITY + "&appid=" + API_KEY

     # Sending HTTP request
response = requests.get(URL)

def init():
    # If the script is called alone.
    # Default weather.
    if len(sys.argv) == 1:

     # retrieving data in the json format
     data = response.json()

     # take the main dict block
     main = data['main']

     # getting temperature
     temperature = main['temp']
     # getting feel like
     temp_feel_like = main['feels_like']
     # getting the humidity
     humidity = main['humidity']
     # getting the pressure
     pressure = main['pressure']

     # weather report
     weather_report = data['weather']
     # wind report
     wind_report = data['wind']

     print(f"{CITY:-^35}")
     print(f"City ID: {data['id']}")
     print(f"Temperature: {temperature}")
     print(f"Feel Like: {temp_feel_like}")
     print(f"Humidity: {humidity}")
     print(f"Pressure: {pressure}")
     print(f"Weather Report: {weather_report[0]['description']}")
     print(f"Wind Speed: {wind_report['speed']}")
     print(f"Time Zone: {data['timezone']}")

     guide_message = "By using the weather command, you can watch the latest news of the weather in every city you want."

     # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
     screen.print(guide_message, style="green")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()