import colorama
from colorama import init
from colorama import Fore
import datetime

init()

class Log:
    """docstring for logger."""

    def __init__(self, Format='%d%.%m%.%y% %h%:%m% %stat% >> %message%', Colors={'INFO': 'CYAN', 'DEBUG': 'YELLOW', 'ERROR': 'RED', 'WARNING': 'LIGHTRED'}):
        self.format = Format
        self.colors = Colors


    global format
    def settings(self,Format='%d%.%m%.%y% %h%:%m% %stat% >> %message%', Colors={'INFO': 'CYAN', 'DEBUG': 'YELLOW', 'ERROR': 'RED', 'WARNING': 'LIGHTRED'}):
        self.format = Format.lower()
        Colors = {k.upper(): Colors[k] for k in Colors}
        if 'INFO' not in Colors:
            Colors['INFO'] = 'CYAN'
        if 'DEBUG' not in Colors:
            Colors['DEBUG'] = 'YELLOW'
        if 'ERROR' not in Colors:
            Colors['ERROR'] = 'RED'
        if 'WARNING' not in Colors:
            Colors['WARNING'] = 'LIGHTRED'
        self.colors = Colors


    def info(self, message, shell:bool=True, file=None):
        year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
        hour, minute, second = datetime.datetime.now().time().hour, datetime.datetime.now().time().minute, datetime.datetime.now().time().second
        output = self.format.replace('%d%', str(day)).replace('%m%', str(month)).replace('%y%', str(year)).replace(
            '%h%', str(hour)).replace('%m%', str(minute)).replace('%s%', str(second)).replace('%stat%',
                                                                                              '[INFO]').replace(
            '%message%', str(message))

        if shell == True:
            if self.colors['INFO'].upper() == 'CYAN':
                print(colorama.Fore.CYAN + output)
            elif self.colors['INFO'].upper() == 'RED':
                print(colorama.Fore.RED + output)
            elif self.colors['INFO'].upper() == 'BLUE':
                print(colorama.Fore.BLUE + output)
            elif self.colors['INFO'].upper() == 'BLACK':
                print(colorama.Fore.BLACK + output)
            elif self.colors['INFO'].upper() == 'GREEN':
                print(colorama.Fore.GREEN + output)
            elif self.colors['INFO'].upper() == 'LIGHTBLACK':
                print(colorama.Fore.LIGHTBLACK_EX + output)
            elif self.colors['INFO'].upper() == 'MAGENTA':
                print(colorama.Fore.MAGENTA + output)
            elif self.colors['INFO'].upper() == 'RESET':
                print(colorama.Fore.RESET + output)
            elif self.colors['INFO'].upper() == 'WHITE':
                print(colorama.Fore.WHITE + output)
            elif self.colors['INFO'].upper() == 'YELLOW':
                print(colorama.Fore.YELLOW + output)
            elif self.colors['INFO'].upper() == 'LIGHTBLUE':
                print(colorama.Fore.LIGHTBLUE_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTCYAN':
                print(colorama.Fore.LIGHTCYAN_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTGREEN':
                print(colorama.Fore.LIGHTGREEN_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTMAGENTA':
                print(colorama.Fore.LIGHTMAGENTA_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTRED':
                print(colorama.Fore.LIGHTRED_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTWHITE':
                print(colorama.Fore.LIGHTWHITE_EX + output)
            elif self.colors['INFO'].upper() == 'LIGHTYELLOW':
                print(colorama.Fore.LIGHTYELLOW_EX + output)
            else:
                print(colorama.Fore.CYAN + output)

        if file != None:
            with open(file, "a") as f:
                f.write(output + '\n')


    def debug(self, message, shell:bool=True, file=None):
        year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
        hour, minute, second = datetime.datetime.now().time().hour, datetime.datetime.now().time().minute, datetime.datetime.now().time().second
        output = self.format.replace('%d%', str(day)).replace('%m%', str(month)).replace('%y%', str(year)).replace('%h%', str(hour)).replace('%m%', str(minute)).replace('%s%', str(second)).replace('%stat%', '[DEBUG]').replace('%message%', str(message))

        if shell == True:
            if self.colors['DEBUG'].upper() == 'CYAN':
                print(colorama.Fore.CYAN + output)
            elif self.colors['DEBUG'].upper() == 'RED':
                print(colorama.Fore.RED + output)
            elif self.colors['DEBUG'].upper() == 'BLUE':
                print(colorama.Fore.BLUE + output)
            elif self.colors['DEBUG'].upper() == 'BLACK':
                print(colorama.Fore.BLACK + output)
            elif self.colors['DEBUG'].upper() == 'GREEN':
                print(colorama.Fore.GREEN + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTBLACK':
                print(colorama.Fore.LIGHTBLACK_EX + output)
            elif self.colors['DEBUG'].upper() == 'MAGENTA':
                print(colorama.Fore.MAGENTA + output)
            elif self.colors['DEBUG'].upper() == 'RESET':
                print(colorama.Fore.RESET + output)
            elif self.colors['DEBUG'].upper() == 'WHITE':
                print(colorama.Fore.WHITE + output)
            elif self.colors['DEBUG'].upper() == 'YELLOW':
                print(colorama.Fore.YELLOW + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTBLUE':
                print(colorama.Fore.LIGHTBLUE_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTCYAN':
                print(colorama.Fore.LIGHTCYAN_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTGREEN':
                print(colorama.Fore.LIGHTGREEN_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTMAGENTA':
                print(colorama.Fore.LIGHTMAGENTA_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTRED':
                print(colorama.Fore.LIGHTRED_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTWHITE':
                print(colorama.Fore.LIGHTWHITE_EX + output)
            elif self.colors['DEBUG'].upper() == 'LIGHTYELLOW':
                print(colorama.Fore.LIGHTYELLOW_EX + output)
            else:
                print(colorama.Fore.CYAN + output)

        if file != None:
            with open(file,"a") as f:
                f.write(output + '\n')


    def error(self, message, shell:bool=True, file=None):
        year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
        hour, minute, second = datetime.datetime.now().time().hour, datetime.datetime.now().time().minute, datetime.datetime.now().time().second
        output = self.format.replace('%d%', str(day)).replace('%m%', str(month)).replace('%y%', str(year)).replace('%h%', str(hour)).replace('%m%', str(minute)).replace('%s%', str(second)).replace('%stat%', '[ERROR]').replace('%message%', str(message))

        if shell == True:
            if self.colors['ERROR'].upper() == 'CYAN':
                print(colorama.Fore.CYAN + output)
            elif self.colors['ERROR'].upper() == 'RED':
                print(colorama.Fore.RED + output)
            elif self.colors['ERROR'].upper() == 'BLUE':
                print(colorama.Fore.BLUE + output)
            elif self.colors['ERROR'].upper() == 'BLACK':
                print(colorama.Fore.BLACK + output)
            elif self.colors['ERROR'].upper() == 'GREEN':
                print(colorama.Fore.GREEN + output)
            elif self.colors['ERROR'].upper() == 'LIGHTBLACK':
                print(colorama.Fore.LIGHTBLACK_EX + output)
            elif self.colors['ERROR'].upper() == 'MAGENTA':
                print(colorama.Fore.MAGENTA + output)
            elif self.colors['ERROR'].upper() == 'RESET':
                print(colorama.Fore.RESET + output)
            elif self.colors['ERROR'].upper() == 'WHITE':
                print(colorama.Fore.WHITE + output)
            elif self.colors['ERROR'].upper() == 'YELLOW':
                print(colorama.Fore.YELLOW + output)
            elif self.colors['ERROR'].upper() == 'LIGHTBLUE':
                print(colorama.Fore.LIGHTBLUE_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTCYAN':
                print(colorama.Fore.LIGHTCYAN_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTGREEN':
                print(colorama.Fore.LIGHTGREEN_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTMAGENTA':
                print(colorama.Fore.LIGHTMAGENTA_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTRED':
                print(colorama.Fore.LIGHTRED_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTWHITE':
                print(colorama.Fore.LIGHTWHITE_EX + output)
            elif self.colors['ERROR'].upper() == 'LIGHTYELLOW':
                print(colorama.Fore.LIGHTYELLOW_EX + output)
            else:
                print(colorama.Fore.CYAN + output)

        if file != None:
            with open(file,"a") as f:
                f.write(output + '\n')


    def warning(self, message, shell:bool=True, file=None):
        year, month, day = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
        hour, minute, second = datetime.datetime.now().time().hour, datetime.datetime.now().time().minute, datetime.datetime.now().time().second
        output = self.format.replace('%d%', str(day)).replace('%m%', str(month)).replace('%y%', str(year)).replace(
            '%h%', str(hour)).replace('%m%', str(minute)).replace('%s%', str(second)).replace('%stat%',
                                                                                              '[WARNING]').replace(
            '%message%', str(message))

        if shell == True:
            if self.colors['WARNING'].upper() == 'CYAN':
                print(colorama.Fore.CYAN + output)
            elif self.colors['WARNING'].upper() == 'RED':
                print(colorama.Fore.RED + output)
            elif self.colors['WARNING'].upper() == 'BLUE':
                print(colorama.Fore.BLUE + output)
            elif self.colors['WARNING'].upper() == 'BLACK':
                print(colorama.Fore.BLACK + output)
            elif self.colors['WARNING'].upper() == 'GREEN':
                print(colorama.Fore.GREEN + output)
            elif self.colors['WARNING'].upper() == 'LIGHTBLACK':
                print(colorama.Fore.LIGHTBLACK_EX + output)
            elif self.colors['WARNING'].upper() == 'MAGENTA':
                print(colorama.Fore.MAGENTA + output)
            elif self.colors['WARNING'].upper() == 'RESET':
                print(colorama.Fore.RESET + output)
            elif self.colors['WARNING'].upper() == 'WHITE':
                print(colorama.Fore.WHITE + output)
            elif self.colors['WARNING'].upper() == 'YELLOW':
                print(colorama.Fore.YELLOW + output)
            elif self.colors['WARNING'].upper() == 'LIGHTBLUE':
                print(colorama.Fore.LIGHTBLUE_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTCYAN':
                print(colorama.Fore.LIGHTCYAN_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTGREEN':
                print(colorama.Fore.LIGHTGREEN_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTMAGENTA':
                print(colorama.Fore.LIGHTMAGENTA_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTRED':
                print(colorama.Fore.LIGHTRED_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTWHITE':
                print(colorama.Fore.LIGHTWHITE_EX + output)
            elif self.colors['WARNING'].upper() == 'LIGHTYELLOW':
                print(colorama.Fore.LIGHTYELLOW_EX + output)
            else:
                print(colorama.Fore.CYAN + output)

        if file != None:
            with open(file, "a") as f:
                f.write(output + '\n')