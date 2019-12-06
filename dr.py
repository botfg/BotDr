# ==============================================================================
# Copyright 2019 Nikolai Bartenev. Contacts: botfgbartenevfgzero76@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import calendar
import csv
import getpass
import os
import sys
from typing import Tuple, List, Set, Union
from datetime import date, datetime


import numpy
import pyAesCrypt
from pysqlcipher3 import dbapi2 as sqlite


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

def vhod() -> None:
    global account_name, account_pass, conn, cursor
    clearScr()
    print(botdrlogo)
    print('enter Q to go to the main menu\n')
    #print('---------------' + color.RED + 'Login' + color.END + '--------------\n')
    print(dec(color.RED + 'Login' + color.END))
    print(color.RED +'1' + color.END + ')--' + color.OKBLUE + 'sign up' + color.END)
    print(color.RED +'2' + color.END + ')--' + color.OKBLUE + 'sign in' + color.END)
    print(color.RED +'3' + color.END + ')--' + color.OKBLUE + 'exit\n' + color.END)
    u_a = input(botdrPrompt)
    if u_a == '3':
        clearScr()
        sys.exit()
    elif u_a == '1':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'sign up' + color.END))
        # check account_existence
        while True:
            account_name = input(color.OKBLUE + 'login: ' + color.END)
            if account_name == 'Q':
                vhod()
            elif len(account_name) < 3:
                print(color.RED + 'login length must be more than 3 characters' + color.END)
                continue
            x1: bool = os.path.isfile(account_name + '.db')
            if x1:
                print(color.RED + 'an account with that name already exists' + color.END)
            elif not x1:
                break
        # end check account_existence
        while True:
            password1: str = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
            if password1 == 'Q':
                vhod()
            elif password1 == account_name:
                print(color.RED + 'login cannot be a password' + color.END)
            else:
                break
        password2: str = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
        if password2 == 'Q':
            vhod()
        while True:
            if password1 == password2:
                account_pass = password1
                break
            elif password1 != password2:
                print(color.RED + 'different passwords' + color.END)
                password1: str = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                password2: str = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
                if password1 or password2 == 'Q':
                    vhod()
        while True:
            u_podtver: str = input(color.OKBLUE + '[Y/n] add ' + color.END + account_name + ': ')
            if u_podtver == 'n':
                vhod()
                break
            elif u_podtver == 'Y':
                # make users db
                name_db: str = account_name + '.db'
                cur_dir: str = os.getcwd()
                path_db: str = os.path.join(cur_dir, name_db)
                conn = sqlite.connect(path_db)
                cursor = conn.cursor()
                cursor.execute("PRAGMA key={}".format(account_pass))
                cursor.execute("""CREATE TABLE users
                    ( name text NOT NULL, bday datetime NOT NULL)
                        """)
                conn.commit()
                break
            else:
                print(color.RED + 'wrong command' + color.END)
    elif u_a == '2':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'sign in' + color.END))
        # check account_existence
        while True:
            account_name = input(color.OKBLUE + 'login: ' + color.END)
            if account_name == 'Q':
                vhod()
            x: bool = os.path.isfile(account_name + '.db')
            if x:
                break
            elif not x:
                print(color.RED +  'account with this name was not found' + color.END)
                if account_name == 'Q':
                    vhod()
        # end check account_existence
        name_db = account_name + '.db'
        cur_dir = os.getcwd()
        path_db = os.path.join(cur_dir, name_db)
        conn = sqlite.connect(path_db)
        cursor = conn.cursor()
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'sign in ' + color.END + account_name))
        while True:
            try:
                account_pass = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                if account_pass == 'Q':
                    vhod()
                cursor.execute("PRAGMA key={}".format(account_pass))
                cursor.execute('SELECT COUNT(name) FROM users')
            except:
                print(color.RED + 'wrong password' + color.END)
            else:
                break
    else:
        #print('wrong command')
        vhod()


def main() -> None:
    global account_name, account_pass, cursor, conn
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'options' + color.END))
    # soon dr
    cursor.execute("""select name, bday, cast (julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now') as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
    results: numpy.ndarray  = numpy.array(cursor.fetchall(), dtype=str)
    birth_in_mounth: int = 0
    now: datetime = datetime.now()
    mounth: int = calendar.monthrange(now.year, now.month)[1]
    for i in results:
        if (int(mounth) - int(i[2])) > int(i[2]):
            birth_in_mounth += 1
    print(color.RED + 'dr' + color.END + ')--' + color.OKBLUE +  'YIEW This month birthday: ' + color.END + str(birth_in_mounth))
    # end soon dr
    print(color.RED + '\n1' + color.END + ')--' + color.OKBLUE + 'ADD' + color.END)
    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'YIEW: ' + color.END + str(len(results)))
    print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'DELETE' + color.OKBLUE)
    print(color.RED + '4' + color.END + ')--' + color.OKBLUE + 'DELETE ALL' + color.END)
    print(color.RED + '5' + color.END + ')--' + color.OKBLUE + 'EDIT' + color.END)
    print(color.RED + '6' + color.END + ')--' + color.OKBLUE + 'STATISTICS' + color.END)
    print(color.RED + '7' + color.END + ')--' + color.OKBLUE + 'ACCOUNT ACTIONS' + color.END)
    print(color.RED + 'Q' + color.END + ')--' + color.OKBLUE + 'EXIT\n' + color.END)
    usercomand: str = input(botdrPrompt)
    clearScr()
    if usercomand == "dr":
        print(botdrlogo)
        print(dec(color.RED + 'Birthday in this month: ' + color.END + str(birth_in_mounth))) 
        cursor.execute("""select name, bday, cast (julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now') as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
        birth_in_mounth: int = 0
        now: datetime = datetime.now()
        mounth: int = calendar.monthrange(now.year, now.month)[1]
        for i in results:
            if (int(mounth) - int(i[2])) > int(i[2]):
                birth_in_mounth += 1
        for item in results:
            if int(item[2]) <= int(mounth):      
                print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
            while True:
                print(color.RED + 'Q)--GO BACK\n' + color.END)
                uc: str = input(botdrPrompt)
                if uc == 'Q':
                    main()
                    break
    elif usercomand == "1":  # 1-Add
        print(botdrlogo)
        print(dec(color.RED + 'Add' + color.END))
        while True:
            user_name: str = input(color.OKBLUE + 'Enter name: ' + color.END)
            if user_name == 'Q':
                main()
            # проверка на повторение
            cursor.execute("PRAGMA key={}".format(account_pass))
            sql: str = ('SELECT COUNT(name) FROM users WHERE name = ?')
            cursor.execute(sql, (user_name,))
            results: Tuple[int] = cursor.fetchone()
            lol: int = results[0]
            if lol == 0:
                break
            elif lol > 0:
                print(color.RED + 'Name already exists' + color.END)
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Add:' + color.END + user_name))
        date_birthday: str = input(color.OKBLUE + 'When is your birthday?' + color.END + '[YYYY.MM.DD]: ')
        if date_birthday == 'Q':
            main()
        while True:
            try:
                date_birthday: datetime.date = datetime.strptime(date_birthday, '%Y.%m.%d').date()
                if date_birthday == 'Q':
                    main()
            except ValueError:
                print('Incorrect date')
                date_birthday: str = input(color.OKBLUE + 'When is your birthday?' + color.END + '[YYYY.MM.DD]: ')
                if date_birthday == 'Q':
                    main()
            else:
                break
        while True:
            clearScr()
            print(botdrlogo)
            uc = input(color.OKBLUE + '[Y/n] add: ' + color.END + user_name + ' ' + str(date_birthday).replace('-', '.') + ": ")
            if uc == 'Y':
                cursor.execute("insert into users(name, bday) values (?, ?)", (user_name, date_birthday))
                conn.commit()
                break
            elif uc == 'n':
                main()
                break
            else:
                print(color.RED + 'Wrong command' + color.END)
        main()
    elif usercomand == '2':  # 2-view
        print(botdrlogo)
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute('SELECT name FROM users')
        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
        if not results.size:
            main()
        cursor.execute("""select name, bday, cast (julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now') as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
        print(dec(color.RED + 'View' + color.END))
        for item in results:
            print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
            print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
        while True:
            print(color.RED + 'Q)--GO BACK\n' + color.END)
            uc: str = input(botdrPrompt)
            if uc == 'Q':
                main()
                break
    elif usercomand == '4':  # 4-delete all person
        print(botdrlogo)
        print(dec(color.RED + 'Delete all' + color.END))
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute("""select name, bday, cast (julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now') as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
        if not results.size:
            main()
        elif results.size > 0:
            cursor.close
            while True:
                uc: str = input(color.OKBLUE + 'Delete all person? [Y/n]: ' + color.END)
                if uc == 'Y':
                    break
                elif uc == 'n':
                    main()
                else:
                    print(color.RED + 'Wrong command' + color.END)
            while True:
                account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                try:
                    conn.close
                    cursor.execute("PRAGMA key={}".format(account_pass))
                    cursor.execute('SELECT COUNT(name) FROM users')
                except:
                    print(color.RED + 'Wrong password' + color.END)
                else:
                    break
            cursor.execute('DELETE FROM users')
            cursor.execute('REINDEX users')
            conn.commit()
            main()
    elif usercomand == '3':  # 3-delete person
        print(botdrlogo)
        print(dec(color.RED + 'Delete' + color.END))
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute("""select name, bday, cast (julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now') as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
        if results.size:
            list_name: List[str] = list()
            for item in results:
                print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
                list_name.append(item[0])
            while True:
                uc: str = input(color.OKBLUE + 'Enter name to delete: ' + color.END)
                if uc == 'Q':
                    main()
                # проверка name на сущ
                if not (uc in list_name):
                    print(color.RED + 'Name not found' + color.END)
                elif uc in list_name:
                    break
                # конец проверки name
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Delete' + color.END))
            user_podtv: str = input(color.OKBLUE + 'Delete ' + uc + color.OKBLUE + ' ? [Y/n]: ' + color.END)
            if user_podtv == 'n':
                main()
            elif user_podtv == 'Y':
                while True:
                    try:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_name == 'Q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        break
            sql: str = ("""DELETE FROM users WHERE name = ?""")
            cursor.execute(sql, (uc,))
            conn.commit()
            main()
    elif usercomand == '5':  # 5-edit
        print(botdrlogo)
        print(dec(color.RED + 'Edit' + color.END))
        cursor.execute('select count(name) from users')
        results: Tuple[int] = cursor.fetchone()
        if results[0] > 0:
            while True:
                uc_name: str = input(color.OKBLUE + 'Enter name: ' + color.END)
                if uc_name == 'Q':
                    main()
                # проверка на повторение
                sql: str = ('SELECT COUNT(name) FROM users WHERE name = ?')
                cursor.execute(sql, (uc_name,))
                results: Tuple[int] = cursor.fetchone()
                lol: int = results[0]
                if lol == 0:
                    print(color.RED + 'Name not found' + color.END)
                elif lol == 1:
                    break
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Edit ' + color.END + uc_name))
            sql: str = ('SELECT * FROM users WHERE name = ?')
            cursor.execute(sql, (uc_name,))
            results: Tuple[str, int] = cursor.fetchone()
            print(color.OKBLUE + 'Name: ' + color.END + str(results[0]) + color.OKBLUE + ' birth date: ' + color.END + str(results[1]))
            while True:
                print(color.RED + '\n1' + color.END + ')--' + color.OKBLUE + 'Edit name' + color.END)
                print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Edit date' + color.END)
                uc: str = input(botdrPrompt)
                if uc == 'Q':
                    main()
                if uc == '1':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'Edit name ' + color.END + uc_name))
                    while True:
                        user_name: str = input(color.OKBLUE + 'Enter new name: ' + color.END)
                        if user_name == 'Q':
                            main()
                        # проверка на повторение
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        sql: str = ('SELECT COUNT(name) FROM users WHERE name = ?')
                        cursor.execute(sql, (user_name,))
                        results: Tuple[int] = cursor.fetchone()
                        lol: int = results[0]
                        if lol == 0:
                            break
                        elif lol > 0:
                            print(color.RED + 'Name already exists' + color.END)
                    while True:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_pass == 'Q':
                            main()
                        try:
                            conn.close
                            cursor.execute("PRAGMA key={}".format(account_pass))
                            cursor.execute('SELECT COUNT(name) FROM users')
                        except:
                            print(color.RED + 'Wrong password' + color.END)
                        else:
                            break
                    sql: str = ("""UPDATE users SET name = ? WHERE name = ?""")
                    cursor.execute(sql, (user_name, uc_name))
                    conn.commit()
                    break
                elif uc == '2':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'Edit date birth ' + color.END + uc_name))
                    while True:
                        date_birthday: str = input(color.OKBLUE + 'When is your birthday? [YYYY.MM.DD]: ' + color.END)
                        if date_birthday == 'Q':
                            main()
                        try:
                            date_birthday: datetime = datetime.strptime(date_birthday, '%Y.%m.%d').date()
                            if date_birthday == 'Q':
                                main()
                        except ValueError:
                            print(color.RED + 'Incorrect date' + color.END)
                        else:
                            break
                    while True:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_pass == 'Q':
                            main()
                        try:
                            conn.close
                            cursor.execute("PRAGMA key={}".format(account_pass))
                            cursor.execute('SELECT COUNT(name) FROM users')
                        except:
                            print(color.RED + 'wrong password' + color.END)
                        else:
                            break
                    sql: str = ("""UPDATE users SET bday = ? WHERE name = ?""")
                    cursor.execute(
                        sql, (date_birthday, uc_name))
                    conn.commit()
                    break
                elif uc == 'Q':
                    break
                else:
                    #print('Wrong command')
                    pass
        main()
    elif usercomand == '6':  # 6-statistics
        print(botdrlogo)
        print(dec(color.RED + 'Statistics' + color.END))
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute('select count(name) from users')
        results2: Tuple[int] = cursor.fetchone()
        if results2[0] > 0:
            today: datetime.date = date.today()
            year: datetime.date = today.year
            if year % 4 == 0:
                if year % 100 == 0 and year % 400 != 0:
                    year = 365
                else:
                    year = 366
            else:
                year = 365
            cursor.execute("""select cast (julianday(
                case
                    when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now', '+1 year')
                    else strftime('%Y-', 'now')
                end || strftime('%m-%d', bday)
            )-julianday('now') as int) as tillbday, cast (julianday(
                case
                    when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now') - strftime('%Y-', bday)
                    else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
                end
            ) as int) as year_after_bday from users order by tillbday""")
            results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
            dr_in_this_year: int = 0
            for i in results:
                if (year - int(i[0])) < int(i[0]):
                    dr_in_this_year += 1
            print(color.OKBLUE + 'total people: ' + color.END + str(results2[0]))
            mas_year: List[int] = list(int(i[1]) - 1 for i in results)
            avg: int = int(sum(mas_year)//len(mas_year))
            print(color.OKBLUE + 'average age: ' + color.END + str(avg))
            print(color.OKBLUE + 'birthdays this year: ' + color.END + str(dr_in_this_year))
            while True:
                print(color.RED + '\nQ)--GO BACK\n' + color.END)
                uc: str = input(botdrPrompt)
                if uc == 'Q':
                    main()
                    break
        elif results2[0] == 0:
            main()
    elif usercomand == '7':  # 7-account actions
        print(botdrlogo)
        print(dec(color.RED + 'Account actions' + color.END))
        while True:
            print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Delete account' + color.END)
            print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Change Password' + color.END)
            print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'Export/import csv' + color.END)
            print(color.RED + '4' + color.END + ')--' + color.OKBLUE + 'Sign out\n' + color.END)
            uc: str = input(botdrPrompt)
            if uc == '4':  # 4-sign out
                conn.close
                vhod()
                break
            elif uc == 'Q':
                break
            elif uc == '1':  # 1-delete account
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Delete account' + color.END))
                while True:
                    try:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_pass == 'Q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        break
                while True:
                    uc: str = input(color.OKBLUE + 'Delete this account? [Y/n]: ' + color.END)
                    if uc == 'n':
                        break
                    elif uc == 'Y':
                        cursor.close
                        conn.close
                        os.remove(account_name + '.db')
                        vhod()
                        main()
                    elif uc == 'Q':
                        break
                    else:
                        print(color.RED + 'Wrong command' + color.END)
            elif uc == '2':  # Change Password
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Change Password' + color.END))
                while True:
                    try:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_pass == 'Q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        break
                while True:
                    new_account_pass_1: str = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                    if new_account_pass_1 == 'Q':
                        main()
                    elif new_account_pass_1 == account_name:
                        print(color.RED + 'Login cannot be a password' + color.END)
                    else:
                        break
                new_account_pass_2: str = getpass.getpass(color.OKBLUE + 'Repeat new pass: ' + color.END)
                if new_account_pass_2 == 'Q':
                    main()
                while True:
                    if new_account_pass_1 and new_account_pass_2 == account_pass:
                        print(color.RED + 'Valid password entered' + color.END)
                        new_account_pass_1: str = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                        if new_account_pass_1 == 'Q':
                            main()
                        new_account_pass_2: str = getpass.getpass(color.OKBLUE + 'Repeat new password: ' + color.END)
                    elif new_account_pass_1 == new_account_pass_2:
                        account_pass = new_account_pass_1
                        break
                    else:
                        print(color.RED + 'Different passwords' + color.END)
                        new_account_pass_1: str = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                        if new_account_pass_1 == 'Q':
                            main()
                        new_account_pass_2: str = getpass.getpass(color.OKBLUE + 'Repeat new password: ' + color.END)
                cursor.execute('PRAGMA rekey={}'.format(account_pass))
                break
            elif uc == '3':  # export and import csv
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Export and import csv' + color.END))
                while True:
                    try:
                        account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                        if account_pass == 'Q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        break
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Export and import csv' + color.END))
                while True:
                    print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Export' + color.END)
                    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Import\n' + color.END)
                    uc: str = input(botdrPrompt)
                    if uc == 'Q':
                        main()
                    elif uc == '1': # export
                        cursor.execute("select name, bday from users")
                        results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
                        if results.size == 0:
                            main()
                            break
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Export csv' + color.END))
                        while True:
                            uc: str = input(color.OKBLUE + 'Encrypt export file? [Y/n]: ' + color.END)
                            if uc == 'Q':
                                main()
                            elif uc == 'n':
                                while True:
                                    name_export: str = input(color.OKBLUE + 'Enter name export file: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break  
                                with open(name_export + '.csv', "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                csv_file.close()
                                main()
                            elif uc == 'Y':
                                while True:
                                    password_1: str = getpass.getpass(color.OKBLUE + 'Enter password for export file: ' + color.END)
                                    if password_1 == 'Q':
                                        main()
                                    password_2: str = getpass.getpass(color.OKBLUE + 'Repeat password for export file: ' + color.END)
                                    if password_2 == 'Q':
                                        main()
                                    if str(password_1) == str(password_2):
                                        password = str(password_2)
                                        break
                                    else:
                                        print(color.RED + 'Different password' + color.END)
                                while True:
                                    name_export: str = input(color.OKBLUE + 'Enter name export file: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break
                                cursor.execute("select name, bday from users")
                                results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
                                if results.size == 0:
                                    print(color.RED + 'No person' + color.END)
                                    main()
                                file: str = (name_export + '.csv')
                                with open(file, "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                csv_file.close()
                                buffer_size1: int = 512 * 2048
                                pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size1)
                                os.remove(file)
                                main()
                            else:
                                print(color.RED + 'Wrong command' + color.END)
                    elif uc == '2': # import
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Import csv' + color.END))
                        uc: str = input(color.OKBLUE + 'Is the file encrypted? [Y/n]: ' + color.END)
                        if uc == 'Q':
                            main
                        elif uc == 'n':
                            while True: # проверка файла на существование
                                file: str = input(color.OKBLUE + 'Enter csv file: ' + color.END)
                                if file == 'Q':
                                    main()
                                x1: bool = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv'):
                                        break
                                    elif not file.endswith('.csv'):
                                        print(color.RED + 'This is not a csv file' + color.END)
                                if not x1:
                                    print(color.RED + 'File missing' + color.END)
                            cursor.execute("select name, bday from users")
                            results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
                            with open(file, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv: List[str] = list()
                                for row in reader:
                                    if len(row) == 2:
                                        if row[0] in results:
                                            incorrect_import_csv.append(row)
                                            continue
                                        try:
                                            date_birthday: datetime = datetime.strptime(row[1], '%Y-%m-%d').date()
                                        except ValueError:
                                            incorrect_import_csv.append(row)
                                        else:
                                            cursor.execute("insert into users(name, bday) values (?, ?)", (row[0], date_birthday))
                                    else:
                                        incorrect_import_csv.append(row)
                            conn.commit()
                            with open(account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                writer = csv.writer(csv_file, delimiter=',')
                                for line in incorrect_import_csv:
                                    writer.writerow(line)
                            f_obj.close()
                            csv_file.close()
                            main()
                        elif uc == 'Y':
                            while True: # проверка файла на существование
                                file: str = input(color.OKBLUE + 'Enter csv file: ' + color.END)
                                if file == 'Q':
                                    main()
                                x1: bool = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv.aes'):
                                        break
                                    elif not file.endswith('.csv.aes'):
                                        print(color.RED + 'This is not a csv file' + color.END)
                                if not x1:
                                    print(color.RED + 'File missing' + color.END)
                            buffer_size1: int = 512 * 2048
                            file2: str = file[0:-4]
                            while True:
                                try:
                                    password: str = getpass.getpass(color.OKBLUE + 'Enter password for export file: ' + color.END)
                                    pyAesCrypt.decryptFile(file, file2, password, buffer_size1)
                                except:
                                    print(color.RED + 'Wrong password' + color.END)
                                else:
                                    break
                            os.remove(file)
                            cursor.execute("select name, bday from users")
                            results: numpy.ndarray = numpy.array(cursor.fetchall(), dtype=str)
                            with open(file2, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv: List[str] = list()
                                for row in reader:
                                    if len(row) == 2:
                                        if row[0] in results:
                                            incorrect_import_csv.append(row)
                                            continue
                                        try:
                                            date_birthday: datetime = datetime.strptime(row[1], '%Y-%m-%d').date()
                                        except ValueError:
                                            incorrect_import_csv.append(row)
                                        else:
                                            cursor.execute("insert into users(name, bday) values (?, ?)", (row[0], date_birthday))
                                    else:
                                        incorrect_import_csv.append(row)
                            conn.commit()
                            with open(account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                writer = csv.writer(csv_file, delimiter=',')
                                for line in incorrect_import_csv:
                                    writer.writerow(line)
                            f_obj.close()
                            csv_file.close()
                            main()
                        else:
                            print(color.RED + 'Wrong command' + color.END)
                    else:
                        print(color.RED + 'Wrong command' + color.END)
            else:
                print(color.RED + 'Wrong command' + color.END)
        main()
    elif usercomand == 'Q':  # Q-exit
        cursor.close()
        clearScr()
        sys.exit()
    else:
        main()


if(__name__ == '__main__'):
    vhod()
    main()