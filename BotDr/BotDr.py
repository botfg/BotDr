# ==============================================================================
# Copyright 2021 Nikolai Bartenev. Contacts: botfgbartenevfgzero76@gmail.com
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
from datetime import date, datetime
import configparser
from hashlib import sha3_512


import numpy
import pyAesCrypt
import pysqlcipher3
from argon2 import PasswordHasher, exceptions
from pysqlcipher3 import dbapi2 as sqlcipher

class color:
    OKBLUE = ('\033[94m')
    OKGREEN = ('\033[92m')
    WARNING = ('\033[93m')
    RED = ('\033[91m')
    END = ('\033[0m')


ph = PasswordHasher()

botdrPrompt = (color.OKGREEN + "BotDr ~# " + color.END)


botdrlogo = (color.OKGREEN + r'''
    ____        __     ____      
   / __ )____  / /_   / __ \_____
  / __  / __ \/ __/  / / / / ___/
 / /_/ / /_/ / /_   / /_/ / /    
/_____/\____/\__/  /_____/_/  
''' + color.END)


db_dir = ('/home/{}/.botdr/'.format(getpass.getuser()))


papka = os.path.isdir(db_dir)
if not papka:
    os.mkdir(db_dir)
    

def logging():
    cursor.execute("select log from settings")
    result = cursor.fetchone()
    return result[0]


def hash(string: str) -> str:
    signature = sha3_512(string.encode()).hexdigest()
    return signature
    
    
def crypt_aes(file, password) -> None:
    buffer_size = 512 * 2048
    pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size)
    os.remove(file)


def clearScr() -> None:
    os.system('clear')


def dec(string: str) -> str:
    length_string = (44 - len(string)) // 2     # 34
    decor = str((length_string * '-') + string + (length_string * '-') + '\n')
    return decor


def createConfig(path):
    #Create a config file
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "accounts status", "off")
    with open(path, "w") as config_file:
        config.write(config_file)
    config_file.close()


def vhod() -> None:
    global account_name, conn, cursor, log_file ,ac
    path = (db_dir + "botdr.ini")
    config = configparser.ConfigParser()
    config.read(path)
    accounts_status = config.get("Settings", "accounts status")
    if accounts_status == "on":
        clearScr()
        print(botdrlogo)
        print('enter Q to go to the main menu\n')
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
                elif account_name == 'main_botdr.db':
                    print(color.RED + 'invalid name' + color.END)
                    continue
                elif len(account_name) < 3:
                    print(color.RED + 'login length must be more than 3 characters' + color.END)
                    continue
                x1 = os.path.isfile(db_dir + account_name + '.db')
                if x1:
                    print(color.RED + 'an account with that name already exists' + color.END)
                elif not x1:
                    break
            # end check account_existence
            while True:
                password1 = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                if password1 == 'Q':
                    vhod()
                elif password1 == account_name:
                    print(color.RED + 'login cannot be a password' + color.END)
                else:
                    break
            password2 = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
            if password2 == 'Q':
                vhod()
            while True:
                if password1 == password2:
                    ac = ph.hash(password1)
                    break
                elif password1 != password2:
                    print(color.RED + 'different passwords' + color.END)
                    password1 = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                    password2 = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
                    if password1 or password2 == 'Q':
                        vhod()
            while True:
                u_podtver = input(color.OKBLUE + '[Y/n] add ' + color.END + account_name + ': ')
                if u_podtver == 'n':
                    vhod()
                    break
                elif u_podtver == 'Y':
                    # make users db
                    name_db = (db_dir + account_name + '.db')
                    conn = sqlcipher.connect(name_db)
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA key={}".format(password1))
                    cursor.execute("""CREATE TABLE 
                        users
                            ( id integer primary key, name varchar(255) NOT NULL, bday datetime NOT NULL)
                            """)
                    conn.commit()
                    cursor.execute("""CREATE TABLE 
                        settings
                            ( log TEXT)
                            """)
                    cursor.execute("""insert into settings(log) values ('off') """)
                    conn.commit()
                    break
                else:
                    print(color.RED + 'wrong command' + color.END)
            vhod()
        elif u_a == '2':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'sign in' + color.END))
            # check account_existence
            while True:
                account_name = input(color.OKBLUE + 'login: ' + color.END)
                if account_name == 'Q':
                    clearScr()
                    sys.exit()
                x = os.path.isfile(db_dir + account_name + '.db')
                if x:
                    break
                elif not x:
                    print(color.RED +  'account with this name was not found' + color.END)
                    if account_name == 'Q':
                        vhod()
            # end check account_existence
            name_db = (db_dir + account_name + '.db')
            conn = sqlcipher.connect(name_db)
            cursor = conn.cursor()
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'sign in ' + color.END + account_name))
            while True:
                try:
                    account_pass = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                    if account_pass == 'Q':
                        sys.exit()
                    cursor.execute("PRAGMA key={}".format(account_pass))
                    cursor.execute('SELECT COUNT(name) FROM users')
                except SystemExit:
                    clearScr()
                    sys.exit()
                except pysqlcipher3.dbapi2.DatabaseError:
                    print(color.RED + 'wrong password' + color.END)
                else:
                    log_file = (db_dir + account_name + '.log')
                    x2 = os.path.isfile(log_file)
                    if not x2:
                        log = open(log_file, 'w')
                    ac = ph.hash(account_pass)
                    break
        else:
            vhod()
    elif accounts_status == "off":
        clearScr()
        x1 = os.path.isfile(db_dir + 'main_botdr.db')
        if x1 == False:
            print(botdrlogo)
            print('enter Q to go to the main menu\n')
            print(dec(color.RED + 'sign up' + color.END))
            while True:
                password1 = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                if password1 == 'Q':
                    clearScr()
                    sys.exit()
                else:
                    break
            password2 = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
            if password2 == 'Q':
                vhod()
            while True:
                if password1 == password2:
                    account_pass = password1
                    break
                elif password1 != password2:
                    print(color.RED + 'different passwords' + color.END)
                    password1 = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                    password2 = getpass.getpass(color.OKBLUE + 'repeat password: ' + color.END)
                    if password1 or password2 == 'Q':
                        vhod()
            while True:
                u_podtver = input(color.OKBLUE + '[Y/n] add account: ' + color.END)
                if u_podtver == 'n':
                    vhod()
                    break
                elif u_podtver == 'Y':
                    # make users db
                    name_db = (db_dir + 'main_botdr.db')
                    conn = sqlcipher.connect(name_db)
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA key={}".format(account_pass))
                    cursor.execute("""CREATE TABLE 
                        users
                            ( id integer primary key, name varchar(255) NOT NULL, bday datetime NOT NULL)
                            """)
                    conn.commit()
                    cursor.execute("""CREATE TABLE 
                        settings
                            ( log TEXT)
                            """)
                    cursor.execute("""insert into settings(log) values ('off') """)
                    conn.commit()
                    break
                else:
                    print(color.RED + 'wrong command' + color.END)
            account_name = ('main_botdr')
            ac = ph.hash(account_pass)
            vhod()     
        if x1 == True:
            name_db = (db_dir + 'main_botdr.db')
            conn = sqlcipher.connect(name_db)
            cursor = conn.cursor()
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'sign in ' + color.END))
            while True:
                try:
                    account_pass = getpass.getpass(color.OKBLUE + 'enter password: ' + color.END)
                    if account_pass == 'Q':
                        sys.exit()
                    cursor.execute("PRAGMA key={}".format(account_pass))
                    cursor.execute('SELECT COUNT(name) FROM users')
                except SystemExit:
                    clearScr()
                    sys.exit()
                except pysqlcipher3.dbapi2.DatabaseError:
                    print(color.RED + 'wrong password' + color.END)
                else:
                    log_file = (db_dir + 'main_botdr.log')
                    x2 = os.path.isfile(log_file)
                    if not x2:
                        log = open(log_file, 'w')
                    account_name = ('main_botdr')
                    ac = ph.hash(account_pass)
                    break    
    

def main() -> None:
    global account_name, cursor, conn, log_file ,ac
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'options' + color.END))
    # soon dr
    cursor.execute("""select cast ((julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday)
        )-julianday('now')) + 1 as int) as tillbday from users""")
    results = numpy.array(cursor.fetchall(), dtype=int)
    birth_in_mounth = 0
    now = datetime.now()
    mounth = calendar.monthrange(now.year, now.month)[1]
    path = (db_dir + "botdr.ini")
    config = configparser.ConfigParser()
    config.read(path)
    for i in results:
        if i[0] <= mounth:
            birth_in_mounth += 1            
    print(color.RED + 'dr' + color.END + ')--' + color.OKBLUE +  'YIEW This month birthday: ' + color.END + str(birth_in_mounth))
    # end soon dr
    print(color.RED + '\n1' + color.END + ')--' + color.OKBLUE + 'ADD' + color.END)
    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'YIEW:' + color.END + str(len(results)))
    print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'DELETE' + color.OKBLUE)
    print(color.RED + '4' + color.END + ')--' + color.OKBLUE + 'DELETE ALL' + color.END)
    print(color.RED + '5' + color.END + ')--' + color.OKBLUE + 'EDIT' + color.END)
    print(color.RED + '6' + color.END + ')--' + color.OKBLUE + 'STATISTICS' + color.END)
    print(color.RED + '7' + color.END + ')--' + color.OKBLUE + 'ACCOUNT ACTIONS' + color.END)
    print(color.RED + '8' + color.END + ')--' + color.OKBLUE + 'SEARCH' + color.END)
    print(color.RED + '9' + color.END + ')--' + color.OKBLUE + 'SETTINGS' + color.END)
    print(color.RED + 'Q' + color.END + ')--' + color.OKBLUE + 'EXIT\n' + color.END)
    usercomand = input(botdrPrompt)
    clearScr()
    if usercomand == "dr":
        print(botdrlogo)
        print(dec(color.RED + 'Birthday in this month: ' + color.END + str(birth_in_mounth))) 
        cursor.execute("""select name, bday, cast ((julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday, '+1 day')
        )-julianday('now')) int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results = numpy.array(cursor.fetchall(), dtype=str)
        for item in results:
            if int(item[2]) <= mounth:      
                print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
        while True:
            print(color.RED + 'Q)--GO BACK\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Q':
                main()
                break
    elif usercomand == "1":  # 1-Add
        print(botdrlogo)
        print(dec(color.RED + 'Add' + color.END))
        while True:
            user_name = input(color.OKBLUE + 'Enter name: ' + color.END)
            if user_name == 'Q':
                main()
            # проверка на повторение
            sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
            cursor.execute(sql, (user_name,))
            results = cursor.fetchone()
            lol = results[0]
            if lol == 0:
                break
            elif lol > 0:
                print(color.RED + 'Name already exists' + color.END)
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Add:' + color.END + user_name))
        date_birthday = input(color.OKBLUE + 'When is your birthday?' + color.END + '[YYYY.MM.DD]: ')
        if date_birthday == 'Q':
            main()
        while True:
            try:
                date_birthday = datetime.strptime(date_birthday, '%Y.%m.%d').date()
                if date_birthday == 'Q':
                    main()
            except ValueError:
                print('Incorrect date')
                date_birthday = input(color.OKBLUE + 'When is your birthday?' + color.END + '[YYYY.MM.DD]: ')
                if date_birthday == 'Q':
                    main()
            else:
                break
        while True:
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Add:' + color.END + user_name))
            uc = input(color.OKBLUE + '[Y/n] add: ' + color.END + user_name + ' ' + str(date_birthday).replace('-', '.') + ": ")
            if uc == 'Y':
                cursor.execute("insert into users(name, bday) values (?, ?)", (user_name, date_birthday))
                conn.commit()
                log_status = logging()
                if log_status == 'on':
                    log = open(log_file, 'a')
                    log.write('INFO: Add person: ' + str(datetime.now()) + '\n')
                    log.close()
                break
            elif uc == 'n':
                main()
                break
            else:
                print(color.RED + 'Wrong command' + color.END)
        main()
    elif usercomand == '2':  # 2-view
        print(botdrlogo)
        cursor.execute('SELECT name FROM users')
        results = numpy.array(cursor.fetchall(), dtype=str)
        if not results.size:
            main()
        cursor.execute("""select name, bday, cast ((julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday, '+1 day')
        )-julianday('now')) as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results = numpy.array(cursor.fetchall(), dtype=str)
        print(dec(color.RED + 'View' + color.END))
        for item in results:
            print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
            print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
        while True:
            print(color.RED + 'Q)--GO BACK\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Q':
                main()
                break
    elif usercomand == '4':  # 4-delete all person
        print(botdrlogo)
        print(dec(color.RED + 'Delete all' + color.END))
        cursor.execute("""select name, bday, cast ((julianday(
            case
                when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                then strftime('%Y-', 'now', '+1 year')
                else strftime('%Y-', 'now')
            end || strftime('%m-%d', bday, '+1 day')
        )-julianday('now')) as int) as tillbday, cast (julianday(
            case
                when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                then strftime('%Y-', 'now') - strftime('%Y-', bday)
                else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
            end
        ) as int) as year_after_bday from users order by tillbday""")
        results = numpy.array(cursor.fetchall(), dtype=str)
        if not results.size:
            main()
        elif results.size > 0:
            while True:
                uc = input(color.OKBLUE + 'Delete all person? [Y/n]: ' + color.END)
                if uc == 'Y':
                    while True:
                        try:
                            account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                            if account_pass == "Q":
                                main()
                            ph.verify(ac, account_pass)
                        except exceptions.VerifyMismatchError:
                            print(color.RED + 'Wrong password' + color.END)
                        else:
                            cursor.execute('DELETE FROM users')
                            cursor.execute('REINDEX users')
                            conn.commit()
                            log_status = logging()
                            if log_status == 'on':
                                log = open(log_file, 'a')
                                log.write('INFO: Delete all person: ' + str(datetime.now()) + '\n')
                                log.close()
                            account_pass = ''
                            main()
                            break
                elif uc == 'n':
                    main()
    elif usercomand == '3':  # 3-delete person
        print(botdrlogo)
        print(dec(color.RED + 'Delete' + color.END))
        while True:
            print(color.OKBLUE + 'show everyone? [Y/n]\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Y':
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Delete' + color.END))
                cursor.execute("""select name, bday, cast ((julianday(
                    case
                        when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                        then strftime('%Y-', 'now', '+1 year')
                        else strftime('%Y-', 'now')
                    end || strftime('%m-%d', bday, '+1 day')
                )-julianday('now')) as int) as tillbday, cast (julianday(
                    case
                        when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                        then strftime('%Y-', 'now') - strftime('%Y-', bday)
                        else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
                    end
                ) as int) as year_after_bday from users order by tillbday""")
                results = numpy.array(cursor.fetchall(), dtype=str)
                for item in results:
                    print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                    print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
                break
            elif uc == 'n':
                print('')
                break
            elif uc == 'Q':
                main()
        while True:
            uc = input(color.OKBLUE + 'Enter name to delete: ' + color.END)
            if uc == 'Q':
                main()
            sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
            cursor.execute(sql, (uc,))
            results = cursor.fetchone()
            if results[0] == 0:
                print(color.RED + 'Name not found' + color.END)
            elif results[0] == 1:
                break
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Delete' + color.END))
        user_podtv = input(color.OKBLUE + 'Delete ' + uc + color.OKBLUE + ' ? [Y/n]: ' + color.END)
        if user_podtv == 'n':
            main()
        elif user_podtv == 'Y':
            while True:
                try:
                    account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                    if account_pass == 'Q':
                        main()
                    ph.verify(ac, account_pass)
                except exceptions.VerifyMismatchError:
                    print(color.RED + 'Wrong password' + color.END)
                else:
                    sql = ("""DELETE FROM users WHERE name = ?""")
                    cursor.execute(sql, (uc,))
                    conn.commit()
                    log_status = logging()
                    if log_status == 'on':
                        log = open(log_file, 'a')
                        log.write('INFO: Delete person: ' + str(datetime.now()) + '\n')
                        log.close()
                    account_pass = ''
                    main()
    elif usercomand == '5':  # 5-edit
        print(botdrlogo)
        print(dec(color.RED + 'Edit' + color.END))
        cursor.execute('select count(name) from users')
        results2 = cursor.fetchone()
        while True:
            print(color.OKBLUE + 'show everyone? [Y/n]\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Y':
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Edit' + color.END))
                cursor.execute("""select name, bday, cast ((julianday(
                    case
                        when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                        then strftime('%Y-', 'now', '+1 year')
                        else strftime('%Y-', 'now')
                    end || strftime('%m-%d', bday, '+1 day')
                )-julianday('now')) as int) as tillbday, cast (julianday(
                    case
                        when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                        then strftime('%Y-', 'now') - strftime('%Y-', bday)
                        else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
                    end
                ) as int) as year_after_bday from users order by tillbday""")
                results = numpy.array(cursor.fetchall(), dtype=str)
                for item in results:
                    print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                    print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
                break
            elif uc == 'n':
                break
            elif uc == 'Q':
                main()
        if results2[0] > 0:
            while True:
                uc_name = input(color.OKBLUE + '\nEnter name: ' + color.END)
                if uc_name == 'Q':
                    main()
                sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
                cursor.execute(sql, (uc_name,))
                results = cursor.fetchone()
                if results[0] == 0:
                    print(color.RED + 'Name not found' + color.END)
                elif results[0] == 1:
                    break
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Edit ' + color.END + uc_name))
            sql = ('SELECT * FROM users WHERE name = ?')
            cursor.execute(sql, (uc_name,))
            results = cursor.fetchone()
            print(color.OKBLUE + 'Name: ' + color.END + str(results[1]) + color.OKBLUE + ' birth date: ' + color.END + str(results[2]))
            while True:
                print(color.RED + '\n1' + color.END + ')--' + color.OKBLUE + 'Edit name' + color.END)
                print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Edit date\n' + color.END)
                uc = input(botdrPrompt)
                if uc == 'Q':
                    main()
                if uc == '1':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'Edit name ' + color.END + uc_name))
                    while True:
                        user_name = input(color.OKBLUE + 'Enter new name: ' + color.END)
                        if user_name == 'Q':
                            main()
                        # проверка на повторение
                        sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
                        cursor.execute(sql, (user_name,))
                        results = cursor.fetchone()
                        lol = results[0]
                        if lol == 0:
                            break
                        elif lol > 0:
                            print(color.RED + 'Name already exists' + color.END)
                    while True:
                        try:
                            account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                            if account_pass == 'Q':
                                main()
                            ph.verify(ac, account_pass)
                        except exceptions.VerifyMismatchError:
                            print(color.RED + 'Wrong password' + color.END)
                        else:
                            sql = ("""UPDATE users SET name = ? WHERE name = ?""")
                            cursor.execute(sql, (user_name, uc_name))
                            conn.commit()
                            log_status = logging()
                            if log_status == 'on':
                                log = open(log_file, 'a')
                                log.write('INFO: Rename person: ' + str(datetime.now()) + '\n')
                                log.close()
                            account_pass = ''
                            break
                    break
                elif uc == '2':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'Edit date birth ' + color.END + uc_name))
                    while True:
                        date_birthday = input(color.OKBLUE + 'When is your birthday? [YYYY.MM.DD]: ' + color.END)
                        if date_birthday == 'Q':
                            main()
                        try:
                            date_birthday = datetime.strptime(date_birthday, '%Y.%m.%d').date()
                            if date_birthday == 'Q':
                                main()
                        except ValueError:
                            print(color.RED + 'Incorrect date' + color.END)
                        else:
                            break
                    while True:
                        try:
                            account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                            if account_pass == 'Q':
                                main()
                            ph.verify(ac, account_pass)
                        except exceptions.VerifyMismatchError:
                            print(color.RED + 'wrong password' + color.END)
                        else:
                            sql = ("""UPDATE users SET bday = ? WHERE name = ?""")
                            cursor.execute(sql, (date_birthday, uc_name))
                            conn.commit()
                            log_status = logging()
                            if log_status == 'on':
                                log = open(log_file, 'a')
                                log.write('INFO: Edit person birthday: ' + str(datetime.now()) + '\n')
                                log.close()
                            break
                    break
                elif uc == 'Q':
                    break
        main()
    elif usercomand == '6':  # 6-statistics
        print(botdrlogo)
        print(dec(color.RED + 'Statistics' + color.END))
        cursor.execute('select count(name) from users')
        results2 = cursor.fetchone()
        if results2[0] > 0:
            today = date.today()
            year = today.year
            if year % 4 == 0:
                if year % 100 == 0 and year % 400 != 0:
                    year = 365
                else:
                    year = 366
            else:
                year = 365
            cursor.execute("""select name, bday, cast ((julianday(
                case
                    when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now', '+1 year')
                    else strftime('%Y-', 'now')
                end || strftime('%m-%d', bday, '+1 day')
            )-julianday('now')) as int) as tillbday, cast (julianday(
                case
                    when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now') - strftime('%Y-', bday)
                    else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
                end
            ) as int) as year_after_bday from users order by tillbday""")
            results = numpy.array(cursor.fetchall(), dtype=str)
            days_after_ny = int((datetime(date.today().year,1,1) - datetime.today()).days)*-1
            dr_in_this_year = 0
            for i in results:
                if int(i[2]) < (year - days_after_ny):
                    dr_in_this_year += 1
            print(color.OKBLUE + 'total people: ' + color.END + str(results2[0]))
            mas_year = [int(i[3]) - 1 for i in results]
            avg = int(sum(mas_year)//len(mas_year))
            old = str(min(i[1] for i in results))
            young = str(max(i[1] for i in results))
            itemindex_young = numpy.where(results==young)
            itemindex_old = numpy.where(results==old)
            print(color.OKBLUE + 'average age: ' + color.END + str(avg))
            print(color.OKBLUE + 'birthdays in this year: ' + color.END + str(dr_in_this_year))
            text = ""
            if len(itemindex_young[0]) > 1:
                for i in range(0,len(itemindex_young)):
                    text += str(results[itemindex_young[0][i]][0] + ', ')
                print(color.OKBLUE + 'the youngest: ' + color.END + text[:-1] + str(' ') + str(young))
            elif len(itemindex_young[0]) == 1:
                print(color.OKBLUE + 'the youngest: ' + color.END + results[itemindex_young[0][0]][0] + str(' ') + str(young))
            text = ""
            if len(itemindex_old[0]) > 1:
                for i in range(0,len(itemindex_old)):
                    text += str(results[itemindex_old[0][i]][0] + ', ')
                print(color.OKBLUE + 'the oldest: ' + color.END + text[:-1] + str(' ') + str(old))
            elif len(itemindex_old[0]) == 1:
                print(color.OKBLUE + 'the oldest: ' + color.END + results[itemindex_old[0][0]][0] + str(' ') + str(old))
            while True:
                print(color.RED + '\nQ)--GO BACK\n' + color.END)
                uc = input(botdrPrompt)
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
            uc = input(botdrPrompt)
            if uc == '4':  # 4-sign out
                conn.close()
                log_status = logging()
                if log_status == 'on':
                    log = open(log_file, 'a')
                    log.write('INFO: Sign out: ' + str(datetime.now()) + '\n')
                    log.close()
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
                        ph.verify(ac, account_pass)
                    except exceptions.VerifyMismatchError:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        account_pass = ''
                        break
                while True:
                    uc = input(color.OKBLUE + 'Delete this account? [Y/n]: ' + color.END)
                    if uc == 'n':
                        break
                    elif uc == 'Y':
                        cursor.close()
                        conn.close()
                        os.remove(db_dir + account_name + '.db')
                        log_status = logging()
                        if log_status == 'on':
                            log = open(log_file, 'a')
                            log.write('INFO: Delete account: ' + str(datetime.now()) + '\n')
                            log.close()
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
                        ph.verify(ac, account_pass)
                    except exceptions.VerifyMismatchError:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        break
                while True:
                    new_account_pass_1 = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                    if new_account_pass_1 == 'Q':
                        main()
                    elif new_account_pass_1 == account_name:
                        print(color.RED + 'Login cannot be a password' + color.END)
                    else:
                        break
                new_account_pass_2 = getpass.getpass(color.OKBLUE + 'Repeat new pass: ' + color.END)
                if new_account_pass_2 == 'Q':
                    main()
                while True:
                    if new_account_pass_1 and new_account_pass_2 == account_pass:
                        print(color.RED + 'Valid password entered' + color.END)
                        new_account_pass_1 = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                        if new_account_pass_1 == 'Q':
                            main()
                        new_account_pass_2 = getpass.getpass(color.OKBLUE + 'Repeat new password: ' + color.END)
                    elif new_account_pass_1 == new_account_pass_2:
                        account_pass = new_account_pass_1
                        break
                    else:
                        print(color.RED + 'Different passwords' + color.END)
                        new_account_pass_1 = getpass.getpass(color.OKBLUE + 'Enter new password: ' + color.END)
                        if new_account_pass_1 == 'Q':
                            main()
                        new_account_pass_2 = getpass.getpass(color.OKBLUE + 'Repeat new password: ' + color.END)
                cursor.execute('PRAGMA rekey={}'.format(account_pass))
                ac = ph.hash(account_pass)
                account_pass = ''
                log_status = logging()
                if log_status == 'on':
                    log = open(log_file, 'a')
                    log.write('INFO: Change password: ' + str(datetime.now()) + '\n')
                    log.close()
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
                        ph.verify(ac, account_pass)
                    except exceptions.VerifyMismatchError:
                        print(color.RED + 'Wrong password' + color.END)
                    else:
                        account_pass = ''
                        break
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Export and import csv' + color.END))
                while True:
                    print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Export' + color.END)
                    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Import\n' + color.END)
                    uc = input(botdrPrompt)
                    if uc == 'Q':
                        main()
                    elif uc == '1': # export
                        cursor.execute("select name, bday from users")
                        results = numpy.array(cursor.fetchall(), dtype=str)
                        if results.size == 0:
                            main()
                            break
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Export csv' + color.END))
                        while True:
                            uc = input(color.OKBLUE + 'Encrypt export file? [Y/n]: ' + color.END)
                            if uc == 'Q':
                                main()
                            elif uc == 'n':
                                while True:
                                    name_export = input(color.OKBLUE + 'Enter name export file: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break  
                                while True:
                                    name_dir = input(color.OKBLUE + 'Enter dir: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break
                                    x1 = os.path.isdir(name_dir)
                                    if x1:
                                        break
                                    elif not x1:
                                        print('dir not found')
                                with open(name_dir + '/' + name_export + '.csv', "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                csv_file.close()
                                log_status = logging()
                                if log_status == 'on':
                                    log = open(log_file, 'a')
                                    log.write('INFO: Not encrypted export: ' + str(datetime.now()) + '\n')
                                    log.close()
                                main()
                            elif uc == 'Y':
                                while True:
                                    password_1 = getpass.getpass(color.OKBLUE + 'Enter password for export file: ' + color.END)
                                    if password_1 == 'Q':
                                        main()
                                    password_2 = getpass.getpass(color.OKBLUE + 'Repeat password for export file: ' + color.END)
                                    if password_2 == 'Q':
                                        main()
                                    if str(password_1) == str(password_2):
                                        password = str(password_2)
                                        break
                                    else:
                                        print(color.RED + 'Different password' + color.END)
                                while True:
                                    name_export = input(color.OKBLUE + 'Enter name export file: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break
                                while True:
                                    name_dir = input(color.OKBLUE + 'Enter dir: ' + color.END)
                                    if name_export == 'Q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print(color.RED + 'Incorrect name' + color.END)
                                    elif len(name_export) > 0:
                                        break
                                    x1 = os.path.isdir(name_dir)
                                    if x1:
                                        break
                                    elif not x1:
                                        print('dir not found')
                                cursor.execute("select name, bday from users")
                                results = numpy.array(cursor.fetchall(), dtype=str)
                                if results.size == 0:
                                    print(color.RED + 'No person' + color.END)
                                    main()
                                file = (name_dir + '/' + name_export + '.csv')
                                with open(file, "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                csv_file.close()
                                buffer_size1 = 512 * 2048
                                pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size1)
                                os.remove(file)
                                log_status = logging()
                                if log_status == 'on':
                                    log = open(log_file, 'a')
                                    log.write('INFO: Encrypted export: ' + str(datetime.now()) + '\n')
                                    log.close()
                                main()
                            else:
                                print(color.RED + 'Wrong command' + color.END)
                    elif uc == '2': # import
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Import csv' + color.END))
                        uc = input(color.OKBLUE + 'Is the file encrypted? [Y/n]: ' + color.END)
                        if uc == 'Q':
                            main()
                        elif uc == 'n':
                            while True:
                                name_dir = input(color.OKBLUE + 'Enter dir: ' + color.END)
                                if name_dir == 'Q':
                                    main()                 
                                if len(name_dir) == 0:
                                    print(color.RED + 'Incorrect name' + color.END)
                                elif len(name_dir) > 0:
                                    break
                                x1 = os.path.isdir(name_dir)
                                if x1:
                                    break
                                elif not x1:
                                    print('dir not found')
                            while True: # проверка файла на существование
                                file = input(color.OKBLUE + 'Enter csv file: ' + color.END)
                                if file == 'Q':
                                    main()
                                x1 = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv'):
                                        break
                                    elif not file.endswith('.csv'):
                                        print(color.RED + 'This is not a csv file' + color.END)
                                if not x1:
                                    print(color.RED + 'File missing' + color.END)
                            cursor.execute("select name, bday from users")
                            results = numpy.array(cursor.fetchall(), dtype=str)
                            with open(name_dir + '/' + file, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv = []
                                for row in reader:
                                    if len(row) == 2:
                                        if row[0] in results:
                                            incorrect_import_csv.append(row)
                                            continue
                                        try:
                                            date_birthday = datetime.strptime(row[1], '%Y-%m-%d').date()
                                        except ValueError:
                                            incorrect_import_csv.append(row)
                                        else:
                                            cursor.execute("insert into users(name, bday) values (?, ?)", (row[0], date_birthday))
                                    else:
                                        incorrect_import_csv.append(row)
                            conn.commit()
                            if incorrect_import_csv:
                                with open(name_dir + '/' + account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in incorrect_import_csv:
                                        writer.writerow(line)
                                csv_file.close()
                            f_obj.close()
                            log_status = logging()
                            if log_status == 'on':
                                log = open(log_file, 'a')
                                log.write('INFO: Not encrypted import: ' + str(datetime.now()) + '\n')
                                log.close()
                            main()
                        elif uc == 'Y':
                            while True:
                                name_dir = input(color.OKBLUE + 'Enter dir: ' + color.END)
                                if name_dir == 'Q':
                                    main()                 
                                if len(name_dir) == 0:
                                    print(color.RED + 'Incorrect name' + color.END)
                                elif len(name_dir) > 0:
                                    break
                                x1 = os.path.isdir(name_dir)
                                if x1:
                                    break
                                elif not x1:
                                    print('dir not found')
                            while True: # проверка файла на существование
                                file = input(color.OKBLUE + 'Enter csv file: ' + color.END)
                                if file == 'Q':
                                    main()
                                x1 = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv.aes'):
                                        break
                                    elif not file.endswith('.csv.aes'):
                                        print(color.RED + 'This is not a csv file' + color.END)
                                if not x1:
                                    print(color.RED + 'File missing' + color.END)
                            buffer_size1 = 512 * 2048
                            file2 = file[0:-4]
                            while True:
                                try:
                                    password = getpass.getpass(color.OKBLUE + 'Enter password for export file: ' + color.END)
                                    pyAesCrypt.decryptFile(file, file2, password, buffer_size1)
                                except:
                                    print(color.RED + 'Wrong password' + color.END)
                                else:
                                    break
                            os.remove(file)
                            cursor.execute("select name, bday from users")
                            results = numpy.array(cursor.fetchall(), dtype=str)
                            with open(name_dir + '/' + file2, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv = []
                                for row in reader:
                                    if len(row) == 2:
                                        if row[0] in results:
                                            incorrect_import_csv.append(row)
                                            continue
                                        try:
                                            date_birthday = datetime.strptime(row[1], '%Y-%m-%d').date()
                                        except ValueError:
                                            incorrect_import_csv.append(row)
                                        else:
                                            cursor.execute("insert into users(name, bday) values (?, ?)", (row[0], date_birthday))
                                    else:
                                        incorrect_import_csv.append(row)
                            conn.commit()
                            if incorrect_import_csv:
                                with open(name_dir + '/' + account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in incorrect_import_csv:
                                        writer.writerow(line)
                                csv_file.close()
                            f_obj.close()
                            log_status = logging()
                            if log_status == 'on':
                                log = open(log_file, 'a')
                                log.write('INFO: Encrypted import: ' + str(datetime.now()) + '\n')
                                log.close()
                            main()
                        else:
                            print(color.RED + 'Wrong command' + color.END)
                    else:
                        print(color.RED + 'Wrong command' + color.END)
            else:
                print(color.RED + 'Wrong command' + color.END)
        main()
    elif usercomand == '8':  # 8-SEARCH
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Search' + color.END))
        cursor.execute('select count(name) from users')
        results = cursor.fetchone()
        if results[0] > 0:
            while True:
                uc_name = input(color.OKBLUE + 'Enter name: ' + color.END)
                if uc_name == 'Q':
                    main()
                sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
                cursor.execute(sql, (uc_name,))
                results = cursor.fetchone()
                if results[0] == 0:
                    print(color.RED + 'Name not found' + color.END)
                elif results[0] == 1:
                    break
            sql = ("""select name, bday, cast ((julianday(
                case
                    when strftime('%m-%d', bday) < strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now', '+1 year')
                    else strftime('%Y-', 'now')
                end || strftime('%m-%d', bday, '+1 day')
            )-julianday('now')) as int) as tillbday, cast (julianday(
                case
                    when strftime('%m-%d', bday) > strftime('%m-%d', 'now')
                    then strftime('%Y-', 'now') - strftime('%Y-', bday)
                    else strftime('%Y-', 'now') - strftime('%Y-', bday) + '1 year'
                end
            ) as int) as year_after_bday from users where name = ? order by tillbday""")
            cursor.execute(sql, (uc_name,))
            item = numpy.array(cursor.fetchone(), dtype=str)
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Search' + color.END))
            print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
            print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
            while True:
                print(color.RED + 'Q)--GO BACK\n' + color.END)
                uc_name = input(botdrPrompt)
                if uc_name == 'Q':
                    main()
                    break
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Search' + color.END))
                print(color.OKBLUE + 'Name: ' + color.END + item[0] + color.OKBLUE + ' date of birth: ' + color.END + item[1].replace('-', '.'))
                print(color.OKBLUE + 'In ' + color.END + item[2] + color.OKBLUE + ' days it will be ' + color.END + item[3] + color.OKBLUE + ' years\n' + color.END)
        elif results[0] == 0:
           main()         
    elif usercomand == '9': # settings
        while True:
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Settings' + color.END))
            path = (db_dir + "botdr.ini")
            config = configparser.ConfigParser()
            config.read(path)
            accounts_status = config.get("Settings", "accounts status")
            log_status = logging()
            print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'on/off accounts status: ' + color.END + color.OKGREEN + accounts_status + color.END)
            print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'on/off logging: ' + color.END + color.OKGREEN + log_status + color.END)
            print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'info' + color.END)
            while True:
                print(color.RED + '\nQ)--GO BACK\n' + color.END)
                uc = input(botdrPrompt)
                if uc == '1':
                    if accounts_status == 'off':
                        config.set("Settings", "accounts status", "on")
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Accounts status' + color.END))
                        while True:
                            try:
                                account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                                if account_pass == "Q":
                                    main()                            
                                ph.verify(ac, account_pass)
                            except exceptions.VerifyMismatchError:
                                print(color.RED + 'Wrong password' + color.END)
                            else:
                                account_pass = ''
                                break
                        while True:
                            new_account_name = input(color.OKBLUE + 'enter a new login for the main account: ' + color.END)
                            x1 = os.path.isfile(new_account_name)
                            if new_account_name == "Q":
                                main()
                            elif len(new_account_name) < 3:
                                print(color.RED + 'login length must be more than 3 characters' + color.END)
                            elif x1 == True:
                                print(color.RED + 'an account with that name already exists' + color.END)
                            else:
                                break
                        log_status = logging()
                        config.set("Settings", "accounts status", "on")
                        if log_status == 'on':
                            log = open(log_file, 'a')
                            log.write('INFO: Multi Account Activation: ' + str(datetime.now()) + '\n')
                            log.write('INFO: Exit: ' + str(datetime.now()) + '\n')
                            log.close()
                        os.rename(db_dir + 'main_botdr.db', db_dir + str(new_account_name) + '.db')
                        os.rename(db_dir + 'main_botdr.log', db_dir + str(new_account_name) + '.log')
                        x1 = os.path.isfile(db_dir + 'main_botdr.log')
                        if x1:
                            os.remove(db_dir + 'main_botdr.log')
                    elif accounts_status == 'on':
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'Accounts status' + color.END))
                        while True:
                            try:
                                account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                                if account_pass == "Q":
                                    main()                            
                                ph.verify(ac, account_pass)
                            except exceptions.VerifyMismatchError:
                                print(color.RED + 'Wrong password' + color.END)
                            else:
                                account_pass = ''
                                break
                        config.set("Settings", "accounts status", "off")
                        if log_status == 'on':
                            log = open(log_file, 'a')
                            log.write('INFO: Multi Account Deactivation: ' + str(datetime.now()) + '\n')
                            log.write('INFO: Exit: ' + str(datetime.now()) + '\n')
                            log.close()
                        os.rename(db_dir + str(account_name) + '.db', db_dir + 'main_botdr.db')
                        os.rename(db_dir + str(account_name) + '.log', db_dir + 'main_botdr.log')
                        x1 = os.path.isfile(db_dir + str(account_name) + '.log')
                        if x1:
                            os.remove(db_dir + str(account_name) + '.log')
                    with open(path, "w") as config_file:
                        config.write(config_file)
                    config_file.close()
                    break
                elif uc == '2':
                    if log_status == 'off':
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'on logging' + color.END))
                        while True:
                            try:
                                account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                                if account_pass == "Q":
                                    main()                            
                                ph.verify(ac, account_pass)
                            except exceptions.VerifyMismatchError:
                                print(color.RED + 'Wrong password' + color.END)
                            else:
                                if log_status == 'on':
                                    log = open(log_file, 'a')
                                    log.write('INFO: Logging is enabled: ' + str(datetime.now()) + '\n')
                                    log.close()
                                cursor.execute("""UPDATE settings SET log = ('on') """)
                                conn.commit()
                                account_pass = ''
                                break
                    elif log_status == 'on':
                        clearScr()
                        print(botdrlogo)
                        print(dec(color.RED + 'off logging' + color.END))
                        while True:
                            try:
                                account_pass = getpass.getpass(color.OKBLUE + 'Enter password: ' + color.END)
                                if account_pass == "Q":
                                    main()                            
                                ph.verify(ac, account_pass)
                            except exceptions.VerifyMismatchError:
                                print(color.RED + 'Wrong password' + color.END)
                            else:
                                if log_status == 'on':
                                    log = open(log_file, 'a')
                                    log.write('INFO: Logging is disabled: ' + str(datetime.now()) + '\n')
                                    log.close()
                                cursor.execute("""UPDATE settings SET log = ('off') """)
                                conn.commit()
                                account_pass = ''
                                break
                    with open(path, "w") as config_file:
                        config.write(config_file)
                    config_file.close()
                    main()
                elif uc == '3':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'Info' + color.END))
                    print(color.OKGREEN + 'version: ' + color.END + '1.5')
                    print(color.OKGREEN + 'license: ' + color.END + 'Apache License Version 2.0')
                    print(color.OKGREEN + 'author: ' + color.END + 'botfg76')
                    print(color.OKGREEN + 'author email: ' + color.END + 'botfgbartenevfgzero76@gmail.com')
                    while True:
                        print(color.RED + '\nQ)--GO BACK\n' + color.END)
                        uc_name = input(botdrPrompt)
                        if uc_name == 'Q':
                            break
                elif uc == 'Q':
                    main()    
            clearScr()
            sys.exit()    
    elif usercomand == 'Q':  # Q-exit
        log_status = logging()
        if log_status == 'on':
            log = open(log_file, 'a')
            log.write('INFO: Exit: ' + str(datetime.now()) + '\n')
            log.close()
        clearScr()
        sys.exit()
    else:
        main()


def super_main():
    global log_file
    path = (db_dir + "botdr.ini")
    if not os.path.exists(path):
        createConfig(path)
    vhod()
    log_status = logging()
    if log_status == 'on':
        log = open(log_file, 'a')
        log.write('INFO: Run app: ' + str(datetime.now()) + '\n')
        log.close()
    main()


if __name__ == '__main__':
    super_main()
