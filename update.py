import os
import subprocess
import shutil
from pathlib import Path

class color:
    HEADER: str = '\033[95m'
    IMPORTANT: str = '\33[35m'
    NOTICE: str = '\033[33m'
    OKBLUE: str = '\033[94m'
    OKGREEN: str = '\033[92m'
    WARNING: str = '\033[93m'
    RED: str = '\033[91m'
    END: str = '\033[0m'
    UNDERLINE: str = '\033[4m'
    LOGGING: str = '\33[34m'

botdrPrompt: str = ("BotDr ~# ")

botdrlogo: str = (color.OKGREEN + '''
    ____        __     ____      
   / __ )____  / /_   / __ \_____
  / __  / __ \/ __/  / / / / ___/
 / /_/ / /_/ / /_   / /_/ / /    
/_____/\____/\__/  /_____/_/  
''' + color.END)


def clearScr() -> None:
    os.system('clear')
   
   
def dec(string: str) -> str:
    length_string: int = (44 - len(string)) // 2     # 34
    decor: str = str((length_string * '-') + string + (length_string * '-') + '\n')
    return decor    
    
print(botdrlogo)
print(dec(color.RED + 'Update' + color.END))


dir: bool = os.path.isdir('BotDr')
if dir:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BotDr')
    shutil.rmtree(path)

subprocess.call("git clone https://github.com/botfg/BotDr.git", shell=True)


with open("version.txt") as file_handler:
    for line in file_handler:
        version_current: str = line
file_handler.close()

with open("BotDr/version.txt") as file_handler:
    for line in file_handler:
        version_next: str = line
file_handler.close()

if float(version_next) <= float(version_current):
    print('\nlatest version installed ' + str(version_current))
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BotDr')
    shutil.rmtree(path)
    while True:
        print('Q)-Go back\n')
        uc = input(botdrPrompt)
        if uc == 'Q':
           os.system("python3 dr.py")
           break
        else:
            pass
elif float(version_next) > float(version_current):
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Update' + color.END))
    print('current version: ' + version_current)
    print('new version: ' + version_next)
    while True:
        print('changes: https://github.com/botfg/BotDr/blob/master/CHANGELOG.md\n')
        print('1)--update')
        print("2)--don't update\n")
        uc: str = input(botdrPrompt)
        if uc == '1':
            current_dit: str = os.getcwd()
            print(current_dit)
            for path in Path(current_dit + '/BotDr').iterdir():
                if path.is_file():
                    shutil.copy(str(path), str(current_dit))
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BotDr')
            shutil.rmtree(path)
            print('installation complete')
            os.system("python3 dr.py")
            break
        elif uc == '2' or 'Q':
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BotDr')
            shutil.rmtree(path)
            os.system("python3 dr.py")
            break
        else:
            pass
