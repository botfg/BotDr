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
import datetime
import getpass
import os
import sys
from datetime import date, datetime
import csv

import numpy
from pysqlcipher3 import dbapi2 as sqlite


def vhod():
    global account_name, account_pass, conn, cursor
    u_a = input('1-sign up 2-sign in 3-exit: ')
    if u_a == '3':
        sys.exit()
    elif u_a == '1':
        account_name = input('login: ')
        if account_name == 'q':
            vhod()
        # check account_existence
        while True:
            x1 = os.path.isfile(account_name + '.db')
            if x1:
                print('an account with that name already exists')
                account_name = input('login: ')
                if account_name == 'q':
                    vhod()
            elif not x1:
                break
        # end check account_existence
        password1 = getpass.getpass('enter password: ')
        if password1 == 'q':
            vhod()
        password2 = getpass.getpass('repeat password: ')
        while True:
            if password1 == password2:
                account_pass = password1
                break
            elif password1 != password2:
                print('different passwords')
                password1 = getpass.getpass('enter password: ')
                password2 = getpass.getpass('repeat password: ')
                if password1 or password2 == 'q':
                    vhod()
        while True:
            u_podtver = input('[Y/n] add ' + account_name + ': ')
            if u_podtver == 'n':
                vhod()
                break
            elif u_podtver == 'Y':
                # make users db
                name_db = account_name + '.db'
                cur_dir = os.getcwd()
                path_db = os.path.join(cur_dir, name_db)
                conn = sqlite.connect(path_db)
                cursor = conn.cursor()
                cursor.execute("PRAGMA key={}".format(account_pass))
                cursor.execute("""CREATE TABLE users
                    ( name text, bday datetime)
                        """)
                conn.commit()
                break
            else:
                print('wrong command')
    elif u_a == '2':
        account_name = input('login: ')
        if account_name == 'q':
            vhod()
        # check account_existence
        while True:
            x = os.path.isfile(account_name + '.db')
            if x:
                break
            elif not x:
                print('account with this name was not found')
                account_name = input('login: ')
                if account_name == 'q':
                    vhod()
        # end check account_existence
        name_db = account_name + '.db'
        cur_dir = os.getcwd()
        path_db = os.path.join(cur_dir, name_db)
        conn = sqlite.connect(path_db)
        cursor = conn.cursor()
        while True:
            try:
                account_pass = getpass.getpass('enter password: ')
                if account_pass == 'q':
                    vhod()
                cursor.execute("PRAGMA key={}".format(account_pass))
                cursor.execute('SELECT COUNT(name) FROM users')
            except:
                print('wrong password')
            else:
                break
    else:
        print('wrong command')
        vhod()


def main():
    import pyAesCrypt
    global account_name, account_pass, cursor, conn
    option_bar = '1-Add 2-view 3-remove person 4-delete all person 5-edit 6-statistics 7-account actions 9-exit: '
    width = len(option_bar) + 1
    print('-'*int(width))
    usercomand = input(option_bar)
    if usercomand == "1":  # 1-Add
        while True:
            user_name = input('enter name: ')
            if user_name == 'q':
                main()
            # проверка на повторение
            cursor.execute("PRAGMA key={}".format(account_pass))
            sql = ('SELECT COUNT(name) FROM users WHERE name = ?')
            cursor.execute(sql, (user_name,))
            results = cursor.fetchone()
            lol = results[0]
            if lol == 0:
                break
            elif lol > 0:
                print('name already exists')
        date_birthday = input('When is your birthday? [YYYY.MM.DD]: ')
        if date_birthday == 'q':
            main()
        while True:
            try:
                date_birthday = datetime.strptime(
                    date_birthday, '%Y.%m.%d').date()
                if date_birthday == 'q':
                    main()
            except ValueError:
                print('incorrect date')
                date_birthday = input('When is your birthday? [YYYY.MM.DD]: ')
                if date_birthday == 'q':
                    main()
            else:
                break
        while True:
            uc = input('[Y/n] add: ' + user_name +
                       ' ' + str(date_birthday).replace('-', '.') + ": ")
            if uc == 'Y':
                cursor.execute(
                    "insert into users(name, bday) values (?, ?)", (user_name, date_birthday))
                conn.commit()
                break
            elif uc == 'n':
                main()
                break
            else:
                print('wrong command')
        main()
    elif usercomand == '2':  # 2-view
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute('SELECT name FROM users')
        results = numpy.array(cursor.fetchall(), dtype=str)
        if len(results) == 0:
            print('no person')
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
        results = numpy.array(cursor.fetchall(), dtype=str)
        for item in results:
            xb = ('name: ' + item[0] + ' date of birth: ' +
                  item[1].replace('-', '.'))
            print('-'*int(len(xb)))
            print(xb)
            print('in {} days it will be {} years'.format(item[2], item[3]))
        main()
    elif usercomand == '4':  # 4-delete all person
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
        results = numpy.array(cursor.fetchall(), dtype=str)
        if len(results) == 0:
            print('no person')
            main()
        elif len(results) > 0:
            cursor.close
            while True:
                uc = input('delete all person? [Y/n]: ')
                if uc == 'Y':
                    break
                elif uc == 'n':
                    main()
                else:
                    print('wrong')
            while True:
                account_pass = getpass.getpass('enter password: ')
                try:
                    conn.close
                    cursor.execute("PRAGMA key={}".format(account_pass))
                    cursor.execute('SELECT COUNT(name) FROM users')
                except:
                    print('wrong password')
                else:
                    break
            cursor.execute('DELETE FROM users')
            cursor.execute('REINDEX users')
            conn.commit()
            main()
    elif usercomand == '3':  # 3-remove person
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
        results = numpy.array(cursor.fetchall(), dtype=str)
        if len(results) > 0:
            list_name = list()
            for item in results:
                xb = (
                    'name: ' + item[0] + ' date of birth: ' + item[1].replace('-', '.'))
                print('-'*len(xb))
                print(xb)
                print('in {} days it will be {} years'.format(
                    item[2], item[3]))
                list_name.append(item[0])
            uc = input('enter name to delete: ')
            if uc == 'q':
                main()
            while True:
                # проверка name на сущ
                if not (uc in list_name):
                    print('name not found')
                    uc = input('enter name: ')
                    if uc == 'q':
                        main()
                elif uc in list_name:
                    break
                # конец проверки name
            user_podtv = input('delete {}? [Y/n]: '.format(uc))
            if user_podtv == 'n':
                main()
            elif user_podtv == 'Y':
                while True:
                    try:
                        account_pass = getpass.getpass('enter password: ')
                        if account_name == 'q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print('wrong password')
                    else:
                        break
            sql = """DELETE FROM users WHERE name = ?"""
            cursor.execute(
                sql, (uc,))
            conn.commit()
            main()
        elif len(results) == 0:
            print('no person')
        main()
    elif usercomand == '5':  # 5-edit
        cursor.execute("PRAGMA key={}".format(account_pass))
        cursor.execute('select count(name) from users')
        results = cursor.fetchone()
        if results[0] > 0:
            while True:
                uc_name = input('enter name: ')
                if uc_name == 'q':
                    main()
                # проверка на повторение
                sql = 'SELECT COUNT(name) FROM users WHERE name = ?'
                cursor.execute(sql, (uc_name,))
                results = cursor.fetchone()
                lol = results[0]
                if lol == 0:
                    print('name not found')
                elif lol == 1:
                    break
            while True:
                uc = input('1-edit name 2-edit date: ')
                if uc == 'q':
                    main()
                if uc == '1':
                    while True:
                        user_name = input('enter new name: ')
                        if user_name == 'q':
                            main()
                        # проверка на повторение
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        sql = 'SELECT COUNT(name) FROM users WHERE name = ?'
                        cursor.execute(sql, (user_name,))
                        results = cursor.fetchone()
                        lol = results[0]
                        if lol == 0:
                            break
                        elif lol > 0:
                            print('name already exists')
                    while True:
                        account_pass = getpass.getpass('enter password: ')
                        if account_pass == 'q':
                            main()
                        try:
                            conn.close
                            cursor.execute(
                                "PRAGMA key={}".format(account_pass))
                            cursor.execute('SELECT COUNT(name) FROM users')
                        except:
                            print('wrong password')
                        else:
                            break
                    sql = """UPDATE users SET name = ? WHERE name = ?"""
                    cursor.execute(sql, (user_name, uc_name))
                    conn.commit()
                    break
                elif uc == '2':
                    while True:
                        date_birthday = input(
                            'When is your birthday? [YYYY.MM.DD]: ')
                        if date_birthday == 'q':
                            main()
                        try:
                            date_birthday = datetime.strptime(
                                date_birthday, '%Y.%m.%d').date()
                            if date_birthday == 'q':
                                main()
                        except ValueError:
                            print('incorrect date')
                        else:
                            break
                    while True:
                        account_pass = getpass.getpass('enter password: ')
                        if account_pass == 'q':
                            main()
                        try:
                            conn.close
                            cursor.execute(
                                "PRAGMA key={}".format(account_pass))
                            cursor.execute('SELECT COUNT(name) FROM users')
                        except:
                            print('wrong password')
                        else:
                            break
                    sql = """UPDATE users SET bday = ? WHERE name = ?"""
                    cursor.execute(
                        sql, (date_birthday, uc_name))
                    conn.commit()
                    break
                elif uc == 'q':
                    break
                else:
                    print('wrong command')
        elif results[0] == 0:
            print('no person')
        main()
    elif usercomand == '6':  # 6-statistics
        cursor.execute("PRAGMA key={}".format(account_pass))
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
            results = numpy.array(cursor.fetchall(), dtype=str)
            dr_in_this_year = 0
            for i in results:
                if (year - int(i[0])) < int(i[0]):
                    dr_in_this_year += 1
            print('total people: ' + str(results2[0]))
            mas_year = list(int(i[1]) - 1 for i in results)
            avg = int(sum(mas_year)//len(mas_year))
            print('average age: ' + str(avg))
            print("birthdays this year: " + str(dr_in_this_year))
        elif results2[0] == 0:
            print('no person')
        main()
    elif usercomand == '7':  # 7-account actions
        while True:
            uc = input(
                '1-delete account 2-Change Password 3-export/import csv 4-sign out: ')
            if uc == '4':  # 3-sign out
                conn.close
                vhod()
                break
            elif uc == 'q':
                break
            elif uc == '1':  # 1-delete account
                while True:
                    try:
                        account_pass = getpass.getpass('enter password: ')
                        if account_pass == 'q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print('wrong password')
                    else:
                        break
                while True:
                    uc = input('del this account? [Y/n]: ')
                    if uc == 'n':
                        break
                    elif uc == 'Y':
                        cursor.close
                        conn.close
                        os.remove(account_name + '.db')
                        print("write q to go back")
                        vhod()
                        # soon dr
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
                        results = numpy.array(cursor.fetchall(), dtype=str)
                        birth_in_mounth = 0
                        now = datetime.now()
                        mounth = calendar.monthrange(now.year, now.month)[1]
                        for i in results:
                            if (int(mounth) - int(i[2])) > int(i[2]):
                                birth_in_mounth += 1
                            print('this month birthday: ' +
                                  str(birth_in_mounth))
                        for item in results:
                            if int(item[2]) <= 31:
                                xb = (
                                    'name: ' + item[0] + ' date of birth: ' + item[1].replace('-', '.'))
                                print('-'*int(len(xb)))
                                print(xb)
                                print(
                                    'in {} days it will be {} years'.format(item[2], item[3]))
                        # end soon dr
                        main()
                    elif uc == 'q':
                        break
                    else:
                        print('wrong command')
            elif uc == '2':  # Change Password
                while True:
                    try:
                        account_pass = getpass.getpass('enter password: ')
                        if account_pass == 'q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print('wrong password')
                    else:
                        break
                new_account_pass_1 = getpass.getpass('enter new pass: ')
                if new_account_pass_1 == 'q':
                    main()
                new_account_pass_2 = getpass.getpass('repeat new pass: ')
                if new_account_pass_2 == 'q':
                    main()
                while True:
                    if new_account_pass_1 and new_account_pass_2 == account_pass:
                        print('valid password entered')
                        new_account_pass_1 = getpass.getpass(
                            'enter new password: ')
                        if new_account_pass_1 == 'q':
                            main()
                        new_account_pass_2 = getpass.getpass(
                            'repeat new password: ')
                    elif new_account_pass_1 == new_account_pass_2:
                        account_pass = new_account_pass_1
                        break
                    else:
                        print('different passwords')
                        new_account_pass_1 = getpass.getpass(
                            'enter new password: ')
                        if new_account_pass_1 == 'q':
                            main()
                        new_account_pass_2 = getpass.getpass(
                            'repeat new password: ')
                cursor.execute('PRAGMA rekey={}'.format(account_pass))
                break
            elif uc == '3':  # export and import csv
                while True:
                    try:
                        account_pass = getpass.getpass('enter password: ')
                        if account_pass == 'q':
                            main()
                        conn.close
                        cursor.execute("PRAGMA key={}".format(account_pass))
                        cursor.execute('SELECT COUNT(name) FROM users')
                    except:
                        print('wrong password')
                    else:
                        break
                while True:
                    uc = input('1-export 2-import: ')
                    if uc == 'q':
                        main()
                    elif uc == '1': # export
                        while True:
                            uc = input('encrypt export file? [Y/n]: ')
                            if uc == 'q':
                                main()
                            elif uc == 'n':
                                cursor.execute("select name, bday from users")
                                results = numpy.array(cursor.fetchall(), dtype=str)
                                if len(results) == 0:
                                    print('no person')
                                    main()
                                while True:
                                    name_export = input('enter name export file: ')  
                                    if name_export == 'q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print('incorrect name')
                                    elif len(name_export) > 0:
                                        break  
                                with open(name_export + '.csv', "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                main()
                            elif uc == 'Y':
                                while True:
                                    password_1 = getpass.getpass('enter password for export file: ')
                                    if password_1 == 'q':
                                        main()
                                    password_2 = getpass.getpass('repeat password for export file: ')
                                    if password_2 == 'q':
                                        main()
                                    if str(password_1) == str(password_2):
                                        password = str(password_2)
                                        break
                                    else:
                                        print('different password')
                                while True:
                                    name_export = input('enter name export file: ')  
                                    if name_export == 'q':
                                        main()                 
                                    if len(name_export) == 0:
                                        print('incorrect name')
                                    elif len(name_export) > 0:
                                        break
                                cursor.execute("select name, bday from users")
                                results = numpy.array(cursor.fetchall(), dtype=str)
                                if len(results) == 0:
                                    print('no person')
                                    main()
                                file = (name_export + '.csv')
                                with open(file, "w", newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=',')
                                    for line in results:
                                        writer.writerow(line)
                                buffer_size1 = 512 * 2048
                                pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size1)
                                os.remove(file)
                                main()
                            else:
                                print('wrong command')
                    elif uc == '2': # import
                        uc = input('is the file encrypted? [Y/n]: ')
                        if uc == 'q':
                            main
                        elif uc == 'n':
                            while True: # проверка файла на существование
                                file = input('enter csv file: ')
                                if file == 'q':
                                    main()
                                x1 = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv'):
                                        break
                                    elif not file.endswith('.csv'):
                                        print('this is not a csv file')
                                if not x1:
                                    print('file missing')
                            cursor.execute("select name, bday from users")
                            results = numpy.array(cursor.fetchall(), dtype=str)
                            with open(file, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv = list()
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
                            with open(account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                writer = csv.writer(csv_file, delimiter=',')
                                for line in incorrect_import_csv:
                                    writer.writerow(line)
                            main()
                        elif uc == 'Y':
                            while True: # проверка файла на существование
                                file = input('enter csv file: ')
                                if file == 'q':
                                    main()
                                x1 = os.path.isfile(file)
                                if x1:
                                    if file.endswith('.csv.aes'):
                                        break
                                    elif not file.endswith('.csv.aes'):
                                        print('this is not a csv file')
                                if not x1:
                                    print('file missing')
                            buffer_size1 = 512 * 2048
                            file2 = file[0:-4]
                            while True:
                                try:
                                    password = getpass.getpass('enter password for export file: ')
                                    pyAesCrypt.decryptFile(file, file2, password, buffer_size1)
                                except:
                                    print('wrong password')
                                else:
                                    break
                            os.remove(file)
                            cursor.execute("select name, bday from users")
                            results = numpy.array(cursor.fetchall(), dtype=str)
                            with open(file2, "r") as f_obj:
                                reader = csv.reader(f_obj)
                                incorrect_import_csv = list()
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
                            with open(account_name + 'incorrect_import.csv', "w", newline='') as csv_file:
                                writer = csv.writer(csv_file, delimiter=',')
                                for line in incorrect_import_csv:
                                    writer.writerow(line)
                            main()
                        else:
                            print('wrong command')
                    else:
                        print('wrong command')
            else:
                print('wrong command')
        main()
    elif usercomand == '9':  # 9-exit
        cursor.close()
        sys.exit()
    else:
        print('wrong command')
        main()


if(__name__ == '__main__'):
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('Bot DR'))
    print("enter q to go to the main menu")
    vhod()
    # soon dr
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
    results = numpy.array(cursor.fetchall(), dtype=str)
    birth_in_mounth = 0
    now = datetime.now()
    mounth = calendar.monthrange(now.year, now.month)[1]
    for i in results:
        if (int(mounth) - int(i[2])) > int(i[2]):
            birth_in_mounth += 1
    print('this month birthday: ' + str(birth_in_mounth))
    for item in results:
        if int(item[2]) <= 31:
            xb = ('name: ' + item[0] + ' date of birth: ' +
                  item[1].replace('-', '.'))
            print('-'*int(len(xb)))
            print(xb)
            print('in {} days it will be {} years'.format(item[2], item[3]))
    # end soon dr
    main()