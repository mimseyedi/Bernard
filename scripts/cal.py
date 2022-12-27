import sys
import subprocess
from datetime import datetime
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
finally:
    screen = Console()


guide_message = """With the cal command you can see the calendar!

Parameters:
-y Year view
-jfa Farsi Jalali Calendar
-jfa <Jalali month> -> example: cal -jfa khordad
-jfi Fingilish Jalali Calendar
-jfi <Jalali month> -> example: cal -jfi mehr"""


class JalaliCalendar:
    def __init__(self, color: str='def', today_style: str='highlight'):
        """
        By using this module, you can easily access the Jalali calendar.
        In this module, external functions are used to change the Gregorian date to
        Jalali, the link of which is mentioned in the file.

        Github repo: https://github.com/mimseyedi/Jcal

        :param color: Jalali calendar color: ['def', 'gray', 'red', 'blue', 'green', 'yellow', 'pink']
        :param today: Jalali calendar today style: ['highlight', '_line', 'blink'] -> default: highlight
        """

        self.__color = color
        self.__today_style = today_style

        self.__colors_ansi_code = {"def": "\033[0m", "gray": "\033[90m", "red": "\033[91m",
                                   "blue": "\033[96m", "green": "\033[92m", "yellow": "\033[93m",
                                   "pink": "\033[95m"}

        self.__styles_ansi_code = {"highlight": "\033[100m", "_line": "\033[4m", "blink": "\033[5m"}

        if self.__color in self.__colors_ansi_code.keys():
            self.__color = self.__colors_ansi_code[self.__color]
        else:
            raise ValueError("This color is not defined for Jalali calendar. Please use the colors listed.")

        if self.__today_style in self.__styles_ansi_code.keys():
            self.__today_style = self.__styles_ansi_code[self.__today_style]
        else:
            raise ValueError("This style is not defined for Jalali calendar. Please use the styles mentioned.")


    def __jalali_to_gregorian(self, jy: int, jm: int, jd: int) -> list:
        """
        The function to convert the Jalali date to Gregorian is taken from the following link:
        https://jdf.scr.ir/jdf/python

        :param jy: Jalali year: int
        :param jm: Jalali month: int
        :param jd: Jalali day: int
        :return: list[int] -> [gregorian_year, gregorian_month, gregorian_day]
        """

        jy += 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd

        if (jm < 7):
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186

        gy = 400 * (days // 146097)
        days %= 146097
        if (days > 36524):
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
            if (days >= 365):
                days += 1

        gy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
        gd = days + 1

        if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            kab = 29
        else:
            kab = 28
        sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0

        while (gm < 13 and gd > sal_a[gm]):
            gd -= sal_a[gm]
            gm += 1

        return [gy, gm, gd]


    def __gregorian_to_jalali(self, gy: int, gm: int, gd: int) -> list:
        """
        The function to convert the Gregorian date to Jalali is taken from the following link:
        https://jdf.scr.ir/jdf/python

        :param gy: Gregorian year: int
        :param gm: Gregorian month: int
        :param gd: Gregorian day: int
        :return: list[int] -> [jalali_year, jalali_month, jalali_day]
        """

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


    def print_calendar(self, month:str ='now', lang: str='farsi') -> None:
        """
        Printing Jalali calendar according to the current date or month entry and highlighting the current day.
        The printed calendar can be changed by specifying the color value and today.

        :param month: Jalali calendar months -> ['farvardin', 'ordibehesht', 'khordad',
                                                 'tir', 'mordad', 'shahrivar',
                                                 'mehr', 'aban', 'azar',
                                                 'dey', 'bahman', 'esfand']
        :param lang: Printing Jalali calendar in two forms -> ['farsi', 'fingilish'] -> def: 'farsi'
        :return: None
        """

        jalali_months = ['farvardin', 'ordibehesht', 'khordad',
                         'tir', 'mordad', 'shahrivar',
                         'mehr', 'aban', 'azar',
                         'dey', 'bahman', 'esfand']

        jalali_months_farsi = ['فروردین', 'اردیبهشت', 'خرداد',
                               'تیر', 'مرداد', 'شهریور',
                               'مهر', 'آبان', 'آذر',
                               'دی', 'بهمن', 'اسفند']

        farsi_numbers = {'0': ' ۰', '1': ' ۱', '2': ' ۲', '3': ' ۳', '4': ' ۴',
                         '5': ' ۵', '6': ' ۶', '7': ' ۷', '8': ' ۸', '9': ' ۹',
                         '10': '۱۰', '11': '۱۱', '12': '۱۲', '13': '۱۳', '14': '۱۴',
                         '15': '۱۵', '16': '۱۶', '17': '۱۷', '18': '۱۸', '19': '۱۹',
                         '20': '۲۰', '21': '۲۱', '22': '۲۲', '23': '۲۳', '24': '۲۴',
                         '25': '۲۵', '26': '۲۶', '27': '۲۷', '28': '۲۸', '29': '۲۹',
                         '30': '۳۰', '31': '۳۱'}

        jalali_days_farsi = ['۲ش', '۳ش', '۴ش', '۵ش', 'جم', 'شن', '۱ش']
        days_after_current_day_farsi = {'۲ش': 5, '۳ش': 4, '۴ش': 3, '۵ش': 2, 'جم': 1, 'شن': 7, '۱ش': 6}

        jalali_days = ['2s', '3s', '4s', '5s', 'jo', 'sh', '1s']
        days_after_current_day = {'2s': 5, '3s': 4, '4s': 3, '5s': 2, 'jo': 1, 'sh': 7, '1s': 6}

        days_space_to_print_first_day = {'2s': 14, '3s': 11, '4s': 8, '5s': 5, 'jo': 2, 'sh': 20, '1s': 17}

        g_year, g_month, g_day = datetime.now().year, datetime.now().month, datetime.now().day
        j_year, j_month, j_day = self.__gregorian_to_jalali(g_year, g_month, g_day)

        if lang.lower() not in ['farsi', 'fingilish']:
            raise ValueError(f"The '{lang.lower()}' language is not defined for Jalali calendar.\n" +
                             "Please choose between 'farsi' and 'fingilish'.")

        if month == 'now' or month in jalali_months:
            current_year = j_year

            if month.lower() == "now":
                current_month = jalali_months[j_month - 1]
            elif month.lower() in jalali_months:
                current_month = month.lower()

            if lang.lower() == "farsi":
                farsi_year = ''.join([farsi_numbers[number] for number in str(current_year)]).replace(" ", '')
                month_title = f'{self.__color}{farsi_year} {jalali_months_farsi[jalali_months.index(current_month)]}'
                month_title_space = ((20 // 2) + len(month_title) // 2) - len(month_title) + 3

            elif lang.lower() == "fingilish":
                month_title = f'{self.__color}{current_month.capitalize()} {current_year}'
                month_title_space = ((20 // 2) + len(month_title) // 2) - len(month_title) + 3

            print(" " * month_title_space + month_title)
            for _ in range(20):
                print("—", end='')
            print()

            if lang.lower() == "farsi":
                print("شن ۱ش ۲ش ۳ش ۴ش ۵ش جم")
            elif lang.lower() == "fingilish":
                print("sh 1s 2s 3s 4s 5s jo")

            if month.lower() == 'now':
                first_day_of_month_in_g = self.__jalali_to_gregorian(j_year, j_month, 1)
            elif month.lower() in jalali_months:
                first_day_of_month_in_g = self.__jalali_to_gregorian(current_year,
                                                                     jalali_months.index(month.lower()) + 1, 1)

            if lang.lower() == "farsi":
                j_weekday = jalali_days_farsi[datetime(first_day_of_month_in_g[0],
                                                       first_day_of_month_in_g[1],
                                                       first_day_of_month_in_g[2]).weekday()]

            elif lang.lower() == "fingilish":
                j_weekday = jalali_days[datetime(first_day_of_month_in_g[0],
                                                 first_day_of_month_in_g[1],
                                                 first_day_of_month_in_g[2]).weekday()]

                space_to_print_first_day = 20 - days_space_to_print_first_day[j_weekday]

            first_months = jalali_months[:6]
            second_months = jalali_months[6:11]
            esfand = jalali_months[-1]

            if current_month in first_months:
                month_days = 31
            elif current_month in second_months:
                month_days = 30
            else:
                month_days = 29

            if lang.lower() == "farsi":
                current_date = 1
                first_day_to_print = days_after_current_day_farsi[j_weekday]
                last_line_space = {0: 18, 1: 5, 2: 8, 3: 11, 4: 14, 5: 17, 6: 20}

                for i in range(first_day_to_print, current_date - 1, -1):
                    print(f'{farsi_numbers[str(i)]}', end=' ')
                    current_date += 1
                print()

                while current_date <= month_days:
                    c = 6
                    if current_date + 6 > month_days:
                        c = c - ((current_date + 6) - month_days)
                    for i in range(current_date + c, current_date - 1, -1):
                        if current_date > month_days:
                            break
                        if i == month_days:
                            if i != current_date:
                                space = 20 - last_line_space[i - current_date]
                                if i == j_day and jalali_months.index(current_month) + 1 == j_month:
                                    print(f"{self.__today_style}{farsi_numbers[str(i)]}\033[0m", end=' ')
                                else:
                                    print(" " * space + f"{self.__color}{farsi_numbers[str(i)]}", end=' ')
                            else:
                                if i == j_day and jalali_months.index(current_month) + 1 == j_month:
                                    print(f"{self.__today_style}{farsi_numbers[str(i)]}\033[0m", end=' ')
                                else:
                                    print(" " * 18 + f"{self.__color}{farsi_numbers[str(i)]}", end=' ')
                        else:
                            if i == j_day and jalali_months.index(current_month) + 1 == j_month:
                                print(f"{self.__today_style}{farsi_numbers[str(i)]}\033[0m", end=' ')
                            else:
                                print(f"{self.__color}{farsi_numbers[str(i)]}", end=' ')
                        current_date += 1
                    print("\033[0m")

            elif lang.lower() == "fingilish":
                current_date = 1

                print(" " * space_to_print_first_day, end='')

                for date in range(current_date, days_after_current_day[j_weekday] + 1):
                    print(f' {current_date}', end=' ')
                    current_date += 1
                print()

                while current_date <= month_days:
                    for _ in range(7):
                        if current_date > month_days:
                            break
                        if current_date < 10:
                            if current_date == j_day and jalali_months.index(current_month) + 1 == j_month:
                                print(f" {self.__today_style}{current_date}\033[0m", end=' ')
                            else:
                                print(f" {self.__color}{current_date}", end=' ')
                        else:
                            if current_date == j_day and jalali_months.index(current_month) + 1 == j_month:
                                print(f"{self.__today_style}{current_date}\033[0m", end=' ')
                            else:
                                print(f"{self.__color}{current_date}", end=' ')
                        current_date += 1
                    print("\033[0m")

        else:
            raise ValueError("The entered Jalali month is not correct. Your choice should be from the Jalali months!")


# Start-point.
def init():
    # Jalali months name.
    jalali_months = ['farvardin', 'ordibehesht', 'khordad',
                     'tir', 'mordad', 'shahrivar',
                     'mehr', 'aban', 'azar',
                     'dey', 'bahman', 'esfand']

    # If the script is called alone.
    # By default, the calendar is printed monthly.
    if len(sys.argv) == 1:
        # Using 'cal' command from Unix terminal.
        subprocess.run(["cal"])

    # If the script is called with the -y parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-y":
        subprocess.run(["cal", "-y"])

    # If the script is called with the -jfa parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-jfa":
        jalali_calendar = JalaliCalendar()
        jalali_calendar.print_calendar()

    # If the script is called with the -jfa parameter and Jalali month.
    # Pattern: cal -jfa khordad
    elif len(sys.argv) == 3 and sys.argv[1] == '-jfa':
        if sys.argv[2] in jalali_months:
            jalali_calendar = JalaliCalendar()
            jalali_calendar.print_calendar(month=sys.argv[2])
        else:
            screen.print("Error: The entered Jalali month is not correct.", style='red')


    # If the script is called with the -jfi parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-jfi":
        jalali_calendar = JalaliCalendar()
        jalali_calendar.print_calendar(lang='fingilish')

    # If the script is called with the -jfi parameter and Jalali month.
    # Pattern: cal -jfi khordad
    elif len(sys.argv) == 3 and sys.argv[1] == '-jfi':
        if sys.argv[2] in jalali_months:
            jalali_calendar = JalaliCalendar()
            jalali_calendar.print_calendar(month=sys.argv[2], lang='fingilish')
        else:
            screen.print("Error: The entered Jalali month is not correct.", style='red')

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
