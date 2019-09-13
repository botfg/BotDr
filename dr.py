import sqlite3
import os
import sys
from pyfiglet import Figlet
import  datetime 
from datetime import datetime




name_db = 'database.db'
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)
conn = sqlite3.connect(path_db)
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor()




def calculate_dates(original_date):
	now = datetime.now()
	date1 = datetime(now.year,original_date.month, original_date.day)
	date2 = datetime(now.year,now.month, now.day)
	if date2 < date1:
		delta1 = datetime(now.year, original_date.month, original_date.day)
		delta2 = datetime(now.year, original_date.month, original_date.day)
		days = (max(delta1, delta2) - now).days + 1
		if days == None:
			c = 'с др'
			return c
		else:
			return days
	elif date2 > date1:
		delta1 = datetime(now.year, original_date.month, original_date.day)
		delta2 = datetime(now.year+1, original_date.month, original_date.day)
		days = (max(delta1, delta2) - now).days + 1
		if days == None:
			c = 'с др'
			return c
		else:
			return days


def main():
	usercomand = input('1-добавить 2-просмотр 3-удалить базу: ')
	if usercomand == "1":
		user_name = input('введи имя: ')
		year = int(input('When is your birthday? [YYYY] '))
		month = int(input('When is your birthday? [MM] '))
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

