import os
import sys
import json
import datetime
import subprocess
try:
     import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
     import requests
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()


# A message for guidance and how to use the script.
guide_message = """By using the weather command, you can watch the latest news of the weather in every city you want.

Parameters:
weather <city> -> example: weather Tehran
-w weekly weather -> example: weather -w New York
"""


# Global variables:
API_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "b07a711bdf19e559aca44794573fe62e"
FORCAST_URL = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + API_KEY


# The function to convert the Gregorian date to Jalali is taken from the following link:
# https://jdf.scr.ir/jdf/python
def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    if (gm > 2): gy2 = gy + 1
    else: gy2 = gy

    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461

    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365

    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)

    return [jy, jm, jd]


def get_todays_weather(city: str):
    API_URL_MATCH = API_URL + "q=" + city + "&appid=" + API_KEY

    request = requests.get(API_URL_MATCH)
    data = request.json()

    if data["cod"] == 200:
        main_data = data["main"]

        screen.print(f"Weather condition of '{city}' city:", style="yellow")

        now = datetime.datetime.today()
        jalali_y, jalali_m, jalali_d = gregorian_to_jalali(now.year, now.month, now.day)

        screen.print(f"   └── G: {now.month}/{now.day}/{now.year} - J: {jalali_y}/{jalali_m}/{jalali_d}", style="yellow")
        screen.print(f"       ├── Temperature: {main_data['temp'] - 273.15}", style="yellow")
        screen.print(f"       ├── Feels Like: {main_data['feels_like'] - 273.15}", style="yellow")
        screen.print(f"       ├── Humidity: {main_data['humidity']}", style="yellow")
        screen.print(f"       └── Pressure: {main_data['pressure']}", style="yellow")

    elif data["cod"] == '404':
        screen.print(f"Error: '{city.capitalize()}' city not found!", style="red")

    elif data["cod"] == '503':
        screen.print("Error: No internet connection!", style="red")

    else:
        screen.print("Error: The API is currently unavailable!", style="red")


def get_weekly_weather(city: str):
    FORCAST_URL_MATCH = FORCAST_URL + '&q=' + city

    request = requests.get(FORCAST_URL_MATCH)
    data = request.json()

    if data["cod"] == '200':
        screen.print(f"Weather condition of {city} this week:")

        current_date = str()

        for item in data['list']:
            time = item['dt_txt']
            next_date, hour = time.split(' ')

            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                jalali_y, jalali_m, jalali_d = gregorian_to_jalali(int(year), int(month), int(day))
                screen.print(f'\nG: {month}/{day}/{year} - J: {jalali_y}/{jalali_m}/{jalali_d}', style="yellow")

            hour = int(hour[:2])

            if hour < 12:
                if hour == 0:
                    hour = 12
                meridiem = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                meridiem = 'PM'

            screen.print(f'   ├── {hour}:00 {meridiem}', style="yellow")

            temperature = item['main']['temp']
            description = item['weather'][0]['description'],

            screen.print(f'   │    ├── Weather condition: {description[0]}', style="yellow")
            screen.print( '   │    └── Celcius: {:.2f}°'.format(temperature - 273.15), style="yellow")

    elif data["cod"] == '404':
        screen.print(f"Error: '{city.capitalize()}' city not found!", style="red")

    elif data["cod"] == '503':
        screen.print("Error: No internet connection!", style="red")

    else:
        screen.print("Error: The API is currently unavailable!", style="red")


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a city!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h and -w.
    # Pattern: weather Tehran
    #          weather New York
    elif len(sys.argv) <= 3 and sys.argv[1] not in  ["-h", "-w"]:
        get_todays_weather(city=' '.join(sys.argv[1:]))

    # If the script is called with the -w parameter.
    # Pattern: weather -w Tehran
    #          weather -w Los Angeles
    elif len(sys.argv) >= 3 and sys.argv[1] == "-w":
        get_weekly_weather(city=' '.join(sys.argv[2:]))

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()
