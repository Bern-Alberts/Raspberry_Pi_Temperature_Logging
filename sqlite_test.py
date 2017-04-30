import sqlite3
from time import gmtime, strftime
from multiprocess_option import temp_readings

#conn = sqlite3.connect('test_database.db')
#c = conn.cursor()

style_brewed = input("Style brewed:\n")
main_date = strftime('%Y/%m/%d %H:%M', gmtime())
table_name = style_brewed + ' - ' + main_date

temperatures = temp_readings()
print(temperatures)
