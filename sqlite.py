import sqlite3
from time import strftime, gmtime

conn = sqlite3.connect('test_database.db')
c = conn.cursor()

main_date = strftime('%Y_%m_%d ', gmtime())
crap = 'ale_' + main_date
name = "CREATE TABLE " + crap + "(a, b, v, d)"
c.execute(name)
