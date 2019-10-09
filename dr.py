#==============================================================================
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
#==============================================================================
import sqlite3
import os
import sys
from pyfiglet import Figlet
import datetime 
from datetime import datetime
from datetime import date
import calendar
import pyAesCrypt
from operator import itemgetter
import getpass
import hashlib
import json
from cryptography.fernet import Fernet
import statistics

cipher_key = b'mWvr6lMjq-o_FwHHCHmBmET99kSk7w8AqVJjapBe2zg='
cipher = Fernet(cipher_key)


f = Figlet(font='slant')
print(f.renderText('Bot DR'))


def sha1OfFile(filepath):
	sha = hashlib.sha3_512()
	with open(filepath, 'rb') as f:
		while True:
			block = f.read(2**10)
			if not block: break
			sha.update(block)
		return sha.hexdigest()


def proverka_db(file):
	x = sha1OfFile(file)
	with open('.data.json', encoding = 'UTF-8') as file:
		data = json.load(file)
	if x == data:
		result = 'file not modified'
	else:
		result = 'file modified'
	os.remove('.data.json')
	return result


def make_hdb(file):
	x = sha1OfFile(file)
	with open('.data.json', 'w', encoding = 'UTF-8') as file:
		json.dump(x, file)


def crypt(dir, password):
	x = os.path.isfile(dir)
	if not x:
		print('No such file or directory')
		main()
	buffer_size = 512 * 2048
	pyAesCrypt.encryptFile(str(dir), str(dir + '.bin'), password, buffer_size)
	os.remove(dir)


def decrypt2(dir, password):
	x = os.path.isfile(dir)
	if x is False:
		print('No such file or directory')
		main()
	buffer_size = 512 * 2048
	pyAesCrypt.decryptFile(str(dir), str(dir[0:-4]), password, buffer_size)
	os.remove(dir)


def calculate_dates(original_date):
	now = datetime.now()
	date1 = datetime(now.year,original_date.month, original_date.day)
	date2 = datetime(now.year,now.month, now.day)
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


x1 = os.path.isfile('.database.db')
x2 = os.path.isfile('.database.db.bin')
if not x1 and x2:
	print("to reset the password(delete the data) enter: reset pass")
	password = getpass.getpass('password1: ')
	if password == "reset pass":
		os.remove('.database.db.bin')
		os.remove('.data.json.bin')
		sys.exit()
	x = os.path.isfile('.data.json.bin')
	if x is True:
		while True:
			try:
				decrypt2('.data.json.bin',password)
				print(proverka_db('.database.db.bin'))
			except ValueError:
				print('Wrong password')
				print("to reset the password(delete the data) enter: reset pass")
				password = getpass.getpass('password1: ')
				if password == "reset pass":
					os.remove('.database.db.bin', '.data.json.bin')
					sys.exit()
			else:
				break
	# if .data.json not found
	while True:
		try:
			decrypt2('.database.db.bin', password)
		except ValueError:
			print('Wrong password')
			password = getpass.getpass('password1: ')
		else:
			break
	name_db = '.database.db'
	cur_dir = os.getcwd()
	path_db = os.path.join(cur_dir, name_db)
	conn = sqlite3.connect(path_db)
	conn.row_factory = lambda cursor, row: row[0]
	cursor = conn.cursor()
else:
	name_db = '.database.db'
	cur_dir = os.getcwd()
	path_db = os.path.join(cur_dir, name_db)
	conn = sqlite3.connect(path_db)
	conn.row_factory = lambda cursor, row: row[0]
	cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS dr
				(id INTEGER, name TEXT, date_birthday TEXT)
				""")
conn.commit()


def str_to_dt(string):
	s = string
	x = datetime(int(s[:4]),int(s[5:-3]),int(s[8:]))
	return datetime.date(x)


def str_to_fernet(string):
	x = string.encode('UTF-8')
	encrypted_text = cipher.encrypt(x)
	return encrypted_text


def main():
	option_bar = '1-Add 2-view 3-remove person 4-delete all 5-edit 6-exit 7-statistics: '
	width = len(option_bar) + 1
	print('-'*int(width))
	usercomand = input(option_bar)
	if usercomand == "1":
		user_name = input('enter name: ')
		# проверка на повторение
		cursor.execute('SELECT name FROM dr')
		results = cursor.fetchall()
		a = list(results)
		mas_d_n = list()
		for i in a:
			mas_d_n.append(cipher.decrypt(i).decode())
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
		a = list(results)
		if len(a) == 0:
			id = 1 
		else:
			id = a[-1] + 1
		uc = input('- no add  + add: ' + user_name + ' ' + date_birthday + ": ")
		if uc == '+':
			date_dr = [(id, user_name_a, date_birthday_a)]
			cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
			conn.commit()
		elif  uc == '-':
			main()
		main()
	elif usercomand == '2':
		cursor.execute('SELECT id FROM dr')
		results = cursor.fetchall()
		a0 = list(results)
		cursor.execute('SELECT name FROM dr')
		results = cursor.fetchall()
		a = list(results)
		cursor.execute('SELECT date_birthday FROM dr')
		results = cursor.fetchall()
		b = list(results)
		mas = list()
		for item in b:
			mas.append(str_to_dt(cipher.decrypt(item)))
		mas2 = list()
		for j in range(len(mas)):
			day_do_dr = calculate_dates(mas[j])
			if day_do_dr == None:
				day_do_dr = int(0)
			mas2.append(day_do_dr)
		spisok = list()
		for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
			spisok.append([a0[i0], cipher.decrypt(a[i]).decode(), mas[j], mas2[e]])
		spisok = sorted(spisok, key=itemgetter(3))
		for i in range(len(spisok)):
			xb = 'id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2])
			width = len(xb)
			print('-'*int(width))
			print(xb)
			print('in ' + str(spisok[i][3]) + ' days it will be ' + str(calculate_age(spisok[i][2])) + ' years')
		main()
	elif  usercomand == '4':
		uc = input("+ yes - no: ")
		if uc == "+":
			cursor.execute('DELETE FROM dr')
			cursor.execute('REINDEX dr')
			conn.commit()
		main()
	elif usercomand == '3':
		uc = input('enter id: ')
		cursor.execute('DELETE FROM dr WHERE id = ' + uc) 
		conn.commit()
		main()
	elif  usercomand == '5':
		cursor.execute('SELECT id FROM dr')
		results = cursor.fetchall()
		a0 = list(results)
		cursor.execute('SELECT name FROM dr')
		results = cursor.fetchall()
		a = list(results)
		cursor.execute('SELECT date_birthday FROM dr')
		results2 = cursor.fetchall()
		b = list(results2)
		mas = list()
		for item in b:
			mas.append(str_to_dt(cipher.decrypt(item)))
		spisok = list()
		for i0, i, j in zip(range(len(a0)), range(len(a)), range(len(mas))):
			spisok.append([a0[i0], cipher.decrypt(a[i]).decode(), mas[j]])
		spisok = sorted(spisok, key=itemgetter(0))
		uc_id = input('enter id: ')
		while True:
			try:
				for i in range(len(spisok)):
					if spisok[i][0] == int(uc_id):
						k = i
				xb = 'id: ' + uc_id + ' name: ' + str(spisok[k][1]) + ' date of birth: ' + str(spisok[k][2])
			except UnboundLocalError:
				print("invalid id: no item with id " + uc_id)
				uc_id = input('enter id: ')
			except ValueError:
				print("invalid id: id don't have letters")
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
				mas_d_n = list()
				for i in a:
					mas_d_n.append(cipher.decrypt(i).decode())
				if user_name in mas_d_n:
					print('such name already exists')
					continue
				break
			uc = input('- no add  + add: ' + str(user_name) + ' ' + str(spisok[k][2]) + ": ")
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
					date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
				else:
					break
			uc = input('- no add  + add: ' + spisok[k][1] + ' ' + date_birthday + ": ")
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
	elif usercomand == '6':
		password = getpass.getpass('password1: ')
		crypt('.database.db', password)
		make_hdb('.database.db.bin')
		crypt('.data.json', password)
		sys.exit()
	elif usercomand == '7':
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
		b = list(results2)
		mas = list()
		mas_year = list()
		for item in b:
			mas_year.append(calculate_age(str_to_dt(cipher.decrypt(item))) -1 )
		dr_in_this_year = 0
		for i in b:
			lol = calculate_dates(str_to_dt(cipher.decrypt(i)))
			if lol == None:
				lol = int(0)
			if (year - lol) > lol:
				dr_in_this_year +=1
		avg  = statistics.mean(mas_year) 
		print('total people: ' + str(len(b)))
		print('average age: ' + str(avg))
		print("birthdays this year: " + str(dr_in_this_year))
		main()
	else:
		print('wrong command')
		main()

if(__name__ == '__main__'):
# soon dr
	cursor.execute('SELECT id FROM dr')
	results = cursor.fetchall()
	a0 = list(results)
	cursor.execute('SELECT name FROM dr')
	results = cursor.fetchall()
	a = list(results)
	cursor.execute('SELECT date_birthday FROM dr')
	results2 = cursor.fetchall()
	b = list(results2)
	mas = list()
	for item in b:
		mas.append(str_to_dt(cipher.decrypt(item)))
	mas2 = list()
	for j in range(len(mas)):
		day_do_dr = calculate_dates(mas[j])
		if day_do_dr == None:
			day_do_dr = int(0)
		mas2.append(day_do_dr)
	spisok = list()
	for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
		spisok.append([a0[i0], cipher.decrypt(a[i]).decode(), mas[j], mas2[e]])
	spisok = sorted(spisok, key=itemgetter(3))
	dr_in_mounth = 0
	now = datetime.now()
	mounth = calendar.monthrange(now.year, now.month)[1]
	for i in b:
		lol = calculate_dates(str_to_dt(cipher.decrypt(i)))
		if lol == None:
			lol = int(0)
		if (int(mounth) - lol) > lol:
			dr_in_mounth += 1
	print('this month birthday: ' + str(dr_in_mounth))
	for i in range(len(spisok)):
		if spisok[i][3] <= 31:
			xb = 'id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2])
			width = len(xb)
			print('-'*int(width))
			print(xb)
			print('in ' + str(spisok[i][3]) + ' days it will be ' + str(calculate_age(spisok[i][2])) + ' years')
	# end soon dr
	main()

