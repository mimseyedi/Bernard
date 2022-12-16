#importing modules
import sys
import subprocess

try:
     import calendar
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
     import calendar

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
guide_message = "By using the weather command, you can watch the latest news of the weather in every city you want."
API_KEY = "b07a711bdf19e559aca44794573fe62e"
forcast_url = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + API_KEY

def init():
 try:
    # If the script is called alone.
    # Default weather.
    if len(sys.argv) == 1:
        # Asks the user for the city or zip code to be queried
        forcast_url = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + API_KEY
        while True:

                    city = input('Please input the city name: ')
                    # Appends the city to the api call
                    forcast_url += '&q=' + city
                    break

        # Stores the Json response
        json_data = requests.get(forcast_url).json()

        location_data = {
            'city': json_data['city']['name'],
            'country': json_data['city']['country']
        }

        screen.print('\n{city}, {country}'.format(**location_data), style="blue")

        # The current date we are iterating through
        current_date = ''

        # Iterates through the array of dictionaries named list in json_data
        for item in json_data['list']:

            # Time of the weather data received, partitioned into 3 hour blocks
            time = item['dt_txt']

            # Split the time into date and hour [2018-04-15 06:00:00]
            next_date, hour = time.split(' ')

            # Stores the current date and prints it once
            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                date = {'y': year, 'm': month, 'd': day}
                screen.print('\n{m}/{d}/{y}'.format(**date), style="blue")

            # Grabs the first 2 integers from our HH:MM:SS string to get the hours
            hour = int(hour[:2])

            # Sets the AM (ante meridiem) or PM (post meridiem) period
            if hour < 12:
                if hour == 0:
                    hour = 12
                meridiem = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                meridiem = 'PM'

            # Prints the hours [HH:MM AM/PM]
            screen.print('\n%i:00 %s' % (hour, meridiem))

            # Temperature is measured in Kelvin
            temperature = item['main']['temp']

            # Weather condition
            description = item['weather'][0]['description'],

            # Prints the description as well as the temperature in Celcius and Farenheit
            screen.print('Weather condition: %s' % description, style="blue")
            screen.print('Celcius: {:.2f}'.format(temperature - 273.15), style="blue")


     # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
     screen.print(guide_message, style="green")

    # If none of these.
 except:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()