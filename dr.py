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
import  datetime 
from datetime import datetime
import pyAesCrypt
from operator import itemgetter
import getpass



f = Figlet(font='slant')
print(f.renderText('Bot DR'))

def crypt(dir, password, password2):
	x = os.path.isfile(dir)
	if x == False:
		print('No such file or directory')
		main()
	buffer_size = 512 * 2048
	try:
		pyAesCrypt.encryptFile(str(dir), str(dir + '.bin'), password, buffer_size)
	except :
		print('Error')
		main()
	dir2 = dir + '.bin'
	try:
		pyAesCrypt.encryptFile(str(dir2), str(dir + '.aes'), password2, buffer_size)
	except :
		print('Error')
		main()
	os.remove(dir)
	os.remove(dir2)





def decrypt(dir, password, password2):
	x = os.path.isfile(dir)
	if x is False:
		print('No such file or directory')
		main()
	buffer_size = 512 * 2048
	dir2 = dir[0:-4] + '.bin'
	try:
		pyAesCrypt.decryptFile(str(dir), str(dir2), password2, buffer_size)
	except:
		print('Error')
		main()
	try:
		pyAesCrypt.decryptFile(str(dir2), str(dir2[0:-4]), password, buffer_size)
	except:
		print('Error')
		main()
	os.remove(dir)
	os.remove(dir2)

def calculate_dates(original_date):
	now = datetime.now()
	date1 = datetime(now.year,original_date.month, original_date.day)
	date2 = datetime(now.year,now.month, now.day)
	if date2 < date1:
		delta1 = datetime(now.year, original_date.month, original_date.day)
		delta2 = datetime(now.year, original_date.month, original_date.day)
		days = (max(delta1, delta2) - now).days
	elif date2 > date1:
		delta1 = datetime(now.year, original_date.month, original_date.day)
		delta2 = datetime(now.year+1, original_date.month, original_date.day)
		days = (max(delta1, delta2) - now).days
	return days + 1



x1 = os.path.isfile('.database.db')
x2 = os.path.isfile('.database.db.aes')
if x1 == False and x2 == True:
	password = getpass.getpass('password1: ')
	password2 = getpass.getpass('password2: ')
	decrypt('.database.db.aes', password, password2)
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

def str_to_dt(string):
	s = string
	x = datetime(int(s[:4]),int(s[5:-3]),int(s[8:]))
	return datetime.date(x)


def main():
	print('-----------------------------------------')
	usercomand = input('1-Add 2-view 3-remove person 4-delete all 5-edit 6-exit: ')
	if usercomand == "1":
		user_name = input('enter name: ')
		date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		try:
			year = str_to_dt(date_birthday)
		except:
			print('incorrect date')
			date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		# ID
		cursor.execute('SELECT id FROM dr')
		results = cursor.fetchall()
		a = list(results)
		if len(a) == 0:
			id = 1 
		else:
			id = int(a[-1]) + 1
		uc = input('- no add  + add: ' + user_name + ' ' + date_birthday + ": ")
		if uc == '+':
			date_dr = [(id, user_name, date_birthday)]
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
		results2 = cursor.fetchall()
		b = list(results2)
		mas = list()
		for item in b:
			mas.append(str_to_dt(item))
		mas2 = list()
		for j in range(len(mas)):
			day_do_dr = calculate_dates(mas[j])
			mas2.append(day_do_dr)
		spisok = list()
		for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
			spisok.append([a0[i0], a[i], mas[j], mas2[e]])
		spisok = sorted(spisok, key=itemgetter(3))
		for i in range(len(spisok)):
			print('-----------------------------------------')
			print('id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2]))
			print('days to birthday: ' + str(spisok[i][3]))
		main()
	elif  usercomand == '4':
		os.remove(path_db)
	elif usercomand == '3':
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
			mas.append(str_to_dt(item))
		mas2 = list()
		for j in range(len(mas)):
			day_do_dr = calculate_dates(mas[j])
			mas2.append(day_do_dr)
		spisok = list()
		for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
			spisok.append([a0[i0], a[i], mas[j], mas2[e]])
		spisok = sorted(spisok, key=itemgetter(3))
		for i in range(len(spisok)):
			print('-----------------------------------------')
			print('id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2]))
			print('days to birthday: ' + str(spisok[i][3]))
		print('-----------------------------------------')
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
			mas.append(str_to_dt(item))
		mas2 = list()
		for j in range(len(mas)):
			day_do_dr = calculate_dates(mas[j])
			mas2.append(day_do_dr)
		spisok = list()
		for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
			spisok.append([a0[i0], a[i], mas[j], mas2[e]])
		spisok = sorted(spisok, key=itemgetter(3))
		for i in range(len(spisok)):
			print('-----------------------------------------')
			print('id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2]))
			print('days to birthday: ' + str(spisok[i][3]))
		print('-----------------------------------------')
		uc_id = input('enter id: ')
		for i in range(len(spisok)):
			if spisok[i][0] == int(uc_id):
				k = i
		print('')
		print('id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2]))
		print('')
		uc = input('1-edit name 2-edit date: ')
		if uc == '1':
			user_name = input('enter new name: ')
			uc = input('- no add  + add: ' + user_name + ' ' + str(spisok[i][2]) + ": ")
			if uc == '+':
				cursor.execute('DELETE FROM dr WHERE id = ' + uc_id)
				date_dr = [(spisok[i][0], user_name, spisok[i][2])]
				cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
				conn.commit()
		elif uc == '2':
			date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
			try:
				year = str_to_dt(date_birthday)
			except:
				print('incorrect date')
				date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
			uc = input('- no add  + add: ' + spisok[i][1] + ' ' + date_birthday + ": ")
			if uc == '+':
				cursor.execute('DELETE FROM dr WHERE id = ' + uc_id)
				date_dr = [(spisok[i][0], spisok[i][1], date_birthday)]
				cursor.executemany("INSERT INTO dr VALUES (?,?,?)", date_dr)
				conn.commit()
		else:
			print('wrong command')
		main()
	elif usercomand == '6':
		password = getpass.getpass('password1: ')
		password2 = getpass.getpass('password2: ')
		crypt('.database.db', password, password2)
		sys.exit()
	else:
		main()



try:
	# Создание таблицы
	cursor.execute("""CREATE TABLE dr
					(id text, name text, date_birthday text)
      			   """)
	# Сохраняем изменения
	conn.commit()
except:
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
		mas.append(str_to_dt(item))
	mas2 = list()
	for j in range(len(mas)):
		day_do_dr = calculate_dates(mas[j])
		mas2.append(day_do_dr)
	spisok = list()
	for i0, i, j, e in zip(range(len(a0)), range(len(a)), range(len(mas)), range(len(mas2))):
		spisok.append([a0[i0], a[i], mas[j], mas2[e]])
	spisok = sorted(spisok, key=itemgetter(3))
	for i in range(len(spisok)):
		if spisok[i][3] <= 31:
			print('this month birthday: ')
			print('id: ' + str(spisok[i][0]) + ' name: ' + str(spisok[i][1]) + ' date of birth: ' + str(spisok[i][2]))
			print('days to birthday: ' + str(spisok[i][3]))
	main()



main()

