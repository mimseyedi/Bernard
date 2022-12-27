import sys
import datetime
import subprocess
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


guide_message = """With the date command you can see the date!

Parameters:
-j Jalali date"""


# The function E6 to convert the Gregorian date to Jalali is taken from the following link:
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


# Start-point.
def init():
    # If the script is called alone.
    # By default, the Gregorian date will be displayed!
    if len(sys.argv) == 1:
        now = datetime.datetime.today()
        screen.print(f"{now.day}/{now.month}/{now.year}")

    # If the script is called with the -j parameter.
    # Convert Gregorian date to Jalali.
    elif len(sys.argv) == 2 and sys.argv[1] == "-j":
        now = datetime.datetime.today()
        jalali_y, jalali_m, jalali_d = gregorian_to_jalali(now.year, now.month, now.day)
        screen.print(f"{jalali_y}/{jalali_m}/{jalali_d}")

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
