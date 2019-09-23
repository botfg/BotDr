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
		days = (max(delta1, delta2) - now).days + 1
	elif date2 > date1:
		delta1 = datetime(now.year, original_date.month, original_date.day)
		delta2 = datetime(now.year+1, original_date.month, original_date.day)
		days = (max(delta1, delta2) - now).days + 1
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




def main():
	usercomand = input('1-добавить 2-просмотр 3-удалить базу 5-выход: ')
	if usercomand == "1":
		user_name = input('введи имя: ')
		year = int(input('When is your birthday? [YYYY] '))
		if len(str(year)) > 4:
			print('некоректная дата ')
			year = int(input('When is your birthday? [YYYY] '))
		month = int(input('When is your birthday? [MM] '))
		if month > 12 or month < 0:
			print('некоректная дата ')
			month = int(input('When is your birthday? [MM] '))
		day = int(input('When is your birthday? [DD] '))
		if day > 31 or day < 0:
			print('некоректная дата ')
			day = int(input('When is your birthday? [DD] '))
		date_dr = [(user_name, year, month, day)]
		cursor.executemany("INSERT INTO dr VALUES (?,?,?,?)", date_dr)
		conn.commit()
		main()
	elif usercomand == '2':
		cursor.execute('SELECT name FROM dr')
		results = cursor.fetchall()
		a = list(results)
		cursor.execute('SELECT year FROM dr')
		results2 = cursor.fetchall()
		b = list(results2)
		cursor.execute('SELECT month FROM dr')
		results3 = cursor.fetchall()
		c = list(results3)
		cursor.execute('SELECT day FROM dr')
		results4 = cursor.fetchall()
		d = list(results4)
		id, q, w, e, r = 1, 0, 0, 0, 0
		for q, w, e, r in zip(range(len(a)), range(len(b)), range(len(c)), range(len(d))):
			birthday = datetime(int(b[w]),int(c[e]),int(d[r]))
			print('--------------------------------------')
			print('человек: ' + str(id) + ' name: ' + a[q] + ' data dr: ' + str(datetime.date(birthday)))
			print('дней до др: ' + str(calculate_dates(birthday)))
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
					(name text, year text, month text, day trxt)
      			   """)
	# Сохраняем изменения
	conn.commit()
except:
	main()


main()

