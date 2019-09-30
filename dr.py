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
	return days



x1 = os.path.isfile('.database.db')
x2 = os.path.isfile('.database.db.aes')
if x1 == False and x2 == True:
	password = '155Vc'
	password2 = 'Sf5g7'
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

	cursor.execute('SELECT name FROM dr')
	results = cursor.fetchall()
	a = list(results)
	cursor.execute('SELECT date_birthday FROM dr')
	results2 = cursor.fetchall()
	b = list(results2)
	mas = list()
	for item in b:
		mas.append(str_to_dt(item))
	id = 1
	mas2 = list()
	for j in range(len(mas)):
		day_do_dr = calculate_dates(mas[j])
		mas2.append(day_do_dr)
	spisok = list()
	for i, j, e in zip(range(len(a)), range(len(mas)), range(len(mas2))):
		spisok.append([a[i], mas[j], mas2[e]])
	spisok = sorted(spisok, key=itemgetter(2))
	for i in range(len(spisok)):
		if spisok[i][2] <= 31:
			print('-----------------------------------------')
			print('человек: ' + str(id) + ' name: ' + str(spisok[i][0]) + ' data dr: ' + str(spisok[i][1]))
			print('дней до др: ' + str(spisok[i][2]))
			id += 1
			
	print('-----------------------------------------')
	usercomand = input('1-добавить 2-просмотр 3-удалить базу 5-выход: ')
	if usercomand == "1":
		user_name = input('введи имя: ')
		date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		try:
			year = str_to_dt(date_birthday).year
		except:
			print('некоректная дата ')
			date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		try:
			month = str_to_dt(date_birthday).month
		except:
			print('некоректная дата ')
			date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		try:
			day = str_to_dt(date_birthday).day
		except:
			print('некоректная дата ')
			date_birthday = input('When is your birthday? [YYYY.MM.DD] ')
		uc = input('добавить: ' + user_name + ' ' + date_birthday + ": ")
		if uc == '+':
			date_dr = [(user_name, date_birthday)]
			cursor.executemany("INSERT INTO dr VALUES (?,?)", date_dr)
			conn.commit()
		elif  uc == '-':
			main()
		main()
	elif usercomand == '2':
		cursor.execute('SELECT name FROM dr')
		results = cursor.fetchall()
		a = list(results)
		cursor.execute('SELECT date_birthday FROM dr')
		results2 = cursor.fetchall()
		b = list(results2)
		mas = list()
		for item in b:
			mas.append(str_to_dt(item))
		id = 1
		mas2 = list()
		for j in range(len(mas)):
			day_do_dr = calculate_dates(mas[j])
			mas2.append(day_do_dr)
		spisok = list()
		for i, j, e in zip(range(len(a)), range(len(mas)), range(len(mas2))):
			spisok.append([a[i], mas[j], mas2[e]])
		spisok = sorted(spisok, key=itemgetter(2))
		for i in range(len(spisok)):
			print('-----------------------------------------')
			print('человек: ' + str(id) + ' name: ' + str(spisok[i][0]) + ' data dr: ' + str(spisok[i][1]))
			print('дней до др: ' + str(spisok[i][2]))
			id += 1
		main()
	elif  usercomand == '3':
		os.remove(path_db)
	elif usercomand == '5':
		password = '155Vc'
		password2 = 'Sf5g7'
		crypt('.database.db', password, password2)
		sys.exit()
	else:
		main()

try:
	# Создание таблицы
	cursor.execute("""CREATE TABLE dr
					(name text, date_birthday text)
      			   """)
	# Сохраняем изменения
	conn.commit()
except:
	main()


main()

