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
import hashlib
import json
import os
import sqlite3
import statistics
import sys
from datetime import date, datetime
from hashlib import sha3_512
from operator import itemgetter


import pyAesCrypt
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from pyfiglet import Figlet

cipher_key = b'oxOj5yx_QAeNmkDokHpdUa8AYfnn8OxZmKkjN93yaZw='
cipher = Fernet(cipher_key)


ph = PasswordHasher()


f = Figlet(font='slant')
print(f.renderText('Bot DR'))


def hash_s(string):
    signature = sha3_512(string.encode()).hexdigest()
    return signature


def crypt(dir, password):
    buffer_size = 512 * 2048
    pyAesCrypt.encryptFile(str(dir), str(dir + '.bin'), password, buffer_size)
    os.remove(dir)


def decrypt_file(dir, password):
    buffer_size = 512 * 2048
    pyAesCrypt.decryptFile(str(dir), str(dir[:-4]), password, buffer_size)
    os.remove(dir)


def calculate_dates(original_date):
    now = datetime.now()
    date1 = datetime(now.year, original_date.month, original_date.day)
    date2 = datetime(now.year, now.month, now.day)
    if date2 < date1:
        delta1 = datetime(now.year, original_date.month, original_date.day)
        delta2 = datetime(now.year, original_date.month, original_date.day)
        days = (max(delta1, delta2) - now).days + 1
        return int(days)
    elif date2 > date1:
        delta1 = datetime(now.year, original_date.month, original_date.day)
        delta2 = datetime(now.year+1, original_date.month, original_date.day)
        days = (max(delta1, delta2) - now).days + 1
        return int(days)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day)) + 1


def vhod():
    global account_name, account_pass, conn, cursor
    u_a = input('1-sign up 2-sign in 3-exit: ')
    if u_a == '3':
        sys.exit()
    elif u_a == '1':
        account_name = input('login: ')
        while True:
            # check account_existence
            x1 = os.path.isfile(account_name + '.db')
            if x1:
                print('акаунт с таким именем уже есть')
                account_name = input('login: ')
            # end check account_existence
            elif not x1:
                break
        password1 = getpass.getpass('enter password: ')
        password2 = getpass.getpass('repeat password: ')
        while True:
            if password1 == password2:
                account_pass = password1
                break
            else:
                print('passwords are different')
                password1 = getpass.getpass('enter password: ')
                password2 = getpass.getpass('repeat password: ')
        u_podtver = input('+ add - no add ' + account_name + ': ')
        if u_podtver == '-':
            vhod()
        elif u_podtver == '+':
            # make users db
            name_db = account_name + '.db'
            cur_dir = os.getcwd()
            path_db = os.path.join(cur_dir, name_db)
            conn = sqlite3.connect(path_db)
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE dr
                (id INTEGER, name TEXT, date_birthday TEXT)
                    """)
            cursor.execute("""CREATE TABLE users
                (name TEXT, pass TEXT)
                    """)
            conn.commit()
            pass_hash_a = ph.hash(account_pass)
            tr = hash_s(account_name)
            users_data = [(tr, pass_hash_a)]
            cursor.executemany("INSERT INTO users VALUES (?,?)", users_data)
            conn.commit()
    elif u_a == '2':
        account_name = input('login: ')
        # check account_existence
        while True:
            x1 = os.path.isfile(account_name + '.db.bin')
            x2 = os.path.isfile(account_name + '.db')
            if x1 or x2:
                break
            elif not x1 or not x2:
                print('акаунт с таким именем not ')
                account_name = input('login: ')
        # end check account_existence
        account_pass = getpass.getpass('enter password: ')
        if x1:
            while True:
                try:
                    decrypt_file(account_name + '.db.bin', account_pass)
                except ValueError:
                    print('wrong password')
                    account_pass = getpass.getpass('enter password: ')
                else:
                    break
            name_db = account_name + '.db'
            cur_dir = os.getcwd()
            path_db = os.path.join(cur_dir, name_db)
            conn = sqlite3.connect(path_db)
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
        elif x2:
            name_db = account_name + '.db'
            cur_dir = os.getcwd()
            path_db = os.path.join(cur_dir, name_db)
            conn = sqlite3.connect(path_db)
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            account_name_h = str(hash_s(account_name))
            execute_arg = (account_name_h,)
            cursor.execute('SELECT pass FROM users WHERE name = ?', execute_arg)
            results = cursor.fetchone()
            agony_pass = results
            while True:
                try:
                    ph.verify(agony_pass, account_pass)
                except:
                    print('Wrong password')
                    account_pass = getpass.getpass('enter password: ')
                else:
                    break
            cursor.close()
            conn.close()
            name_db = account_name + '.db'
            cur_dir = os.getcwd()
            path_db = os.path.join(cur_dir, name_db)
            conn = sqlite3.connect(path_db)
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
    else:
        print('wrong command')
        vhod()


def str_to_dt(string):
    x = datetime(int(string[:4]), int(string[5:-3]), int(string[8:]))
    return datetime.date(x)


def str_to_fernet(string):
    string = string.encode()
    encrypted_text = cipher.encrypt(string)
    return encrypted_text


def main():
    global account_name, account_pass, cursor, conn
    # soon dr
    cursor.execute('SELECT id FROM dr')
    results = cursor.fetchall()
    list_id_from_db = list(results)
    cursor.execute('SELECT name FROM dr')
    results = cursor.fetchall()
    list_name_from_db = list(results)
    cursor.execute('SELECT date_birthday FROM dr')
    results = cursor.fetchall()
    list_date_birth_from_db = list(results)
    list_date_birth = [str_to_dt(cipher.decrypt(item)) for item in list_date_birth_from_db]
    list_days_to_birth = [calculate_dates(list_date_birth[i]) for i in range(len(list_date_birth))]
    spisok = sorted([[list_id_from_db[i0], cipher.decrypt(list_name_from_db[i]).decode(), list_date_birth[j], list_days_to_birth[e]] for i0, i, j, e in zip(range(len(list_id_from_db)), range(len(list_name_from_db)), range(len(list_date_birth)), range(len(list_days_to_birth)))], key=itemgetter(3))
    birth_in_mounth = 0
    now = datetime.now()
    mounth = calendar.monthrange(now.year, now.month)[1]
    for i in list_date_birth_from_db:
        lol = calculate_dates(str_to_dt(cipher.decrypt(i)))
        if lol == None:
            lol = int(0)
        if (int(mounth) - lol) > lol:
            birth_in_mounth += 1
    print('this month birthday: ' + str(birth_in_mounth))
    for i in range(len(spisok)):
        if spisok[i][3] == None:
            xb = 'id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i]
                                                              [1]) + ' date of birth: ' + str(spisok[i][2])
            width = len(xb)
            print('-'*int(width))
            print(xb)
            print(str(calculate_age(spisok[i][2])) + ' years old today')          
        elif spisok[i][3] <= 31:
            xb = 'id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i]
                                                              [1]) + ' date of birth: ' + str(spisok[i][2])
            width = len(xb)
            print('-'*int(width))
            print(xb)
            print('in ' + str(spisok[i][3]) + ' days it will be ' +
                  str(calculate_age(spisok[i][2])) + ' years')
    # end soon dr
    option_bar = '1-Add 2-view 3-remove person 4-delete all person 5-edit 6-statistics 7-account действия 9-exit: '
    width = len(option_bar) + 1
    print('-'*int(width))
    usercomand = input(option_bar)
    if usercomand == "1":  #1-Add
        user_name = input('enter name: ')
        # проверка на повторение
        cursor.execute('SELECT name FROM dr')
        results = cursor.fetchall()
        list_name_from_db = list(results)
        mas_d_n = [cipher.decrypt(x).decode() for x in list_name_from_db]
        if user_name in mas_d_n:
            print('such name already exists')
            main()
        user_name_a = str_to_fernet(user_name)
        date_birthday = input('When is your birthday? [YYYY.MM.DD]: ')
        while True:
            try:
                year = str_to_dt(date_birthday)
            except:
                print('incorrect date')
                date_birthday = input('When is your birthday? [YYYY.MM.DD]: ')
            else:
                break
        date_birthday_a = str_to_fernet(date_birthday)
        # ID
        cursor.execute('SELECT id FROM dr')
        results = cursor.fetchall()
        list_id_from_db = list(results)
        if len(list_id_from_db) == 0:
            id = 1
        else:
            id = list_id_from_db[-1] + 1
        uc = input('- no add  + add: ' + user_name +
                   ' ' + date_birthday + ": ")
        if uc == '+':
            date_dr = [(id, user_name_a, date_birthday_a)]
            cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
            conn.commit()
        elif uc == '-':
            main()
        main()
    elif usercomand == '2':  #2-view
        cursor.execute('SELECT id FROM dr')
        results = cursor.fetchall()
        list_id_from_db = list(results)
        cursor.execute('SELECT name FROM dr')
        results = cursor.fetchall()
        list_name_from_db = list(results)
        cursor.execute('SELECT date_birthday FROM dr')
        results = cursor.fetchall()
        list_date_birth_from_db = list(results)
        list_date_birth = [str_to_dt(cipher.decrypt(item)) for item in list_date_birth_from_db]
        list_days_to_birth = [calculate_dates(list_date_birth[i]) for i in range(len(list_date_birth))]
        spisok = sorted([[list_id_from_db[i0], cipher.decrypt(list_name_from_db[i]).decode(), list_date_birth[j], list_days_to_birth[e]] for i0, i, j, e in zip(range(len(list_id_from_db)), range(len(list_name_from_db)), range(len(list_date_birth)), range(len(list_days_to_birth)))], key=itemgetter(3))
        for i in range(len(spisok)):
            xb = 'id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i]
                                                              [1]) + ' date of birth: ' + str(spisok[i][2])
            width = len(xb)
            print('-'*int(width))
            print(xb)
            print('in ' + str(spisok[i][3]) + ' days it will be ' +
                  str(calculate_age(spisok[i][2])) + ' years')
        main()
    elif usercomand == '4':  #4-delete all person
        uc = input("+ yes - no: ")
        if uc == "+":
            cursor.execute('DELETE FROM dr')
            cursor.execute('REINDEX dr')
            conn.commit()
        main()
    elif usercomand == '3':  #3-remove person
        uc = input('enter id: ')
        cursor.execute('DELETE FROM dr WHERE id = ' + uc)
        conn.commit()
        main()
    elif usercomand == '5':  #5-edit
        cursor.execute('SELECT id FROM dr')
        results = cursor.fetchall()
        list_id_from_db = list(results)
        cursor.execute('SELECT name FROM dr')
        results = cursor.fetchall()
        list_name_from_db = list(results)
        cursor.execute('SELECT date_birthday FROM dr')
        results = cursor.fetchall()
        list_date_birth_from_db = list(results)
        list_date_birth = [str_to_dt(cipher.decrypt(item)) for item in list_date_birth_from_db]
        list_days_to_birth = [calculate_dates(list_date_birth[i]) for i in range(len(list_date_birth))]
        spisok = sorted([[list_id_from_db[i0], cipher.decrypt(list_name_from_db[i]).decode(), list_date_birth[j], list_days_to_birth[e]] for i0, i, j, e in zip(range(len(list_id_from_db)), range(len(list_name_from_db)), range(len(list_date_birth)), range(len(list_days_to_birth)))], key=itemgetter(3))
        uc_id = input('enter id: ')
        while True:
            try:
                for i in range(len(spisok)):
                    if spisok[i][0] == int(uc_id):
                        k = i
                xb = 'id: ' + uc_id + ' name: ' + \
                    str(spisok[k][1]) + ' date of birth: ' + str(spisok[k][2])
            except UnboundLocalError:
                print("invalid id: no item with id " + uc_id)
                uc_id = input('enter id: ')
            except ValueError:
                print("invalid id: id don'execute_arg have letters")
                uc_id = input('enter id: ')
            else:
                break
        width = len(xb)
        print('-'*int(width))
        print(xb)
        uc = input('1-edit name 2-edit date: ')
        if uc == '1':
            while True:
                user_name = input('enter new name: ')
                # проверка на повторение
                cursor.execute('SELECT name FROM dr')
                results = cursor.fetchall()
                a = list(results)
                mas_d_n = [cipher.decrypt(i).decode() for i in a]
                if user_name in mas_d_n:
                    print('such name already exists')
                    continue
                break
            uc = input('- no add  + add: ' + str(user_name) +
                       ' ' + str(spisok[k][2]) + ": ")
            if uc == '+':
                cursor.execute('DELETE FROM dr WHERE id = ' + uc_id)
                user_name_a = str_to_fernet(user_name)
                date_birthday_a = str_to_fernet(str(spisok[k][2]))
                date_dr = [(uc_id, user_name_a, date_birthday_a)]
                cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
                conn.commit()
        elif uc == '2':
            date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
            while True:
                try:
                    year = str_to_dt(date_birthday)
                except:
                    print('incorrect date')
                    date_birthday = input(
                        'When is your birthday? [YYYY.MM.DD] ')
                else:
                    break
            uc = input('- no add  + add: ' +
                       spisok[k][1] + ' ' + date_birthday + ": ")
            #TODO удалить сразу с базы
            if uc == '+':
                cursor.execute('DELETE FROM dr WHERE id = ' + uc_id)
                user_name_a = str_to_fernet(spisok[k][1])
                date_birthday_a = str_to_fernet(date_birthday)
                date_dr = [(uc_id, user_name_a, date_birthday_a)]
                cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
                conn.commit()
            elif uc == '-':
                main()
        else:
            print('wrong command')
        main()
    elif usercomand == '6':  #6-statistics
        today = date.today()
        year = today.year
        if year % 4 == 0:
            if year % 100 == 0 and year % 400 != 0:
                year = 365
            else:
                year = 366
        else:
            year = 365
        cursor.execute('SELECT date_birthday FROM dr')
        results2 = cursor.fetchall()
        list_date_birth_from_db = list(results2)
        mas_year = [calculate_age(str_to_dt(cipher.decrypt(item))) - 1 for item in list_date_birth_from_db]
        dr_in_this_year = 0
        for i in list_date_birth_from_db:
            lol = calculate_dates(str_to_dt(cipher.decrypt(i)))
            if lol == None:
                lol = int(0)
            if (year - lol) > lol:
                dr_in_this_year += 1
        avg = statistics.mean(mas_year)
        print('total people: ' + str(len(list_date_birth_from_db)))
        print('average age: ' + str(avg))
        print("birthdays this year: " + str(dr_in_this_year))
        main()
    elif usercomand == '7': #7-account действия
        uc = input('1-delete account 2-смена пароля 3-sign out: ') 
        if uc  == '3':
            crypt(account_name + '.db', account_pass)
            vhod()
            main()
        elif uc == '1':
            account_name = input('имя акка ')
            # check account_existence
            while True:
                x1 = os.path.isfile(account_name + '.db')
                if x1:
                    break
                elif not x1:
                    print('акаунт с таким именем not ')
                    account_name = input('login: ')
            # end check account_existence
            account_name_h = str(hash_s(account_name))
            execute_arg = (account_name_h,)
            cursor.execute('SELECT pass FROM users WHERE name = ?', execute_arg)
            results = cursor.fetchone()
            agony_pass = results
            account_pass = getpass.getpass('enter password: ')
            while True:
                try:
                    ph.verify(agony_pass, account_pass)
                except:
                    print('Wrong password')
                    account_pass = getpass.getpass('enter password: ')
                else:
                    break
            cursor.close()
            conn.close()
            try:
                os.remove(account_name + '.db.bin')
            except:
                os.remove(account_name + '.db')
            vhod()
            main()
        elif uc == '2': #смена пароля
            account_name = input('введи имя акаунта: ')
            # check account_existence
            cursor.execute('SELECT name FROM users')
            results = cursor.fetchall()
            crypt_login = list(results)
            account_existence = 0
            for i in crypt_login:
                if hash_s(account_name) == i:
                    account_existence += 1
                if account_existence == 0:
                    print('account does not exist')
                    vhod()
                    main()
            # end account_existence
            account_pass = getpass.getpass('введи пароль: ')
            account_name_h = str(hash_s(account_name))
            execute_arg = (account_name_h,)
            cursor.execute('SELECT pass FROM users WHERE name = ?', execute_arg)
            results = cursor.fetchone()
            agony_pass = results
            while True:
                try:
                    ph.verify(agony_pass, account_pass)
                except:
                    print('Wrong password')
                    account_pass = getpass.getpass('enter password: ')
                else:
                    break
            new_account_pass_1 = getpass.getpass('новый pass: ')
            new_account_pass_2 = getpass.getpass('повтори пасс: ')
            while True:
                if new_account_pass_1 == new_account_pass_2:
                    account_pass = new_account_pass_1
                    break
                else:
                    print('неверный пароль')
                    new_account_pass_1 = getpass.getpass('pass: ')
                    new_account_pass_2 = getpass.getpass('повтори пасс: ')
            new_account_pass_agony = ph.hash(account_pass)
            sql = """UPDATE users SET pass = ? WHERE name = ?"""
            cursor.execute(sql, (new_account_pass_agony, account_name_h))
            conn.commit()
            main()
        else:
            print('wrong command')
            vhod()
            main()
    elif usercomand == '9':  #9-exit
        crypt(account_name + '.db', account_pass)
        sys.exit()
    else:
        print('wrong command')
        main()


if(__name__ == '__main__'):
    vhod()
    main()