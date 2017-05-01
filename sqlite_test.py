from multiprocessing import Pool
import subprocess
import numpy as np
import time
from datetime import datetime as dt
from probe_id import probe_identifier
import sqlite3
from time import gmtime, strftime

device_positions, device_files, HL_probe = probe_identifier()

conn = sqlite3.connect('test_database.db')
c = conn.cursor()

style_brewed = input("Style brewed:\n")
main_date = strftime('%Y_%m_%d', gmtime())
table_name = style_brewed + '_' + main_date
print(table_name)
table_columns = "(" + ', '.join(device_positions) + ")"
create_table = "CREATE TABLE " + table_name + table_columns
c.execute(create_table)
print(create_table)


def probe_call(filename):
    error = 0
    while error <= 3:
        data_bytes = subprocess.check_output('cat ' + filename, shell=True)
        data_list = data_bytes.decode(encoding='utf-8').splitlines()
        first_line, second_line = data_list
        if first_line.split(' ')[-1] != 'YES':
            error += 1
        elif error == 3:
            temperature = 'Error probe:' + filename
            return temperature
        else:
            temperature = np.int(second_line.split('t=')[1]) / 1000
            return temperature


def temp_logging_and_display():
    try:
        p = Pool()
        while True:
            dt1 = dt.now()
            temp = p.map(probe_call, device_files)
            temp_insert = "INSERT INTO " + table_name + " VALUES (?)"
            print(temp_insert)
            c.executemany(temp_insert, temp)
            temp_display = [str(i) + ' = ' + str(j) for i, j in zip(device_positions, temp)]
            dt2 = dt.now()
            print(', '.join(temp_display))
            print(dt2 - dt1)
    except KeyboardInterrupt:
        print()
        conn.commit()
        conn.close()

temp_logging_and_display()
