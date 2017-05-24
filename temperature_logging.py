from multiprocessing import Pool
import os
from collections import OrderedDict
import numpy as np
from datetime import datetime as dt
from time import strftime

from database_check import db_setup, colour_directory, colour_positions
from sqlalchemy import create_engine
from brewery_db_delcarative import Base, Data
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///brewery_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

brew_probe_numbers = db_setup()


def probe_call(filename):
    error = 0
    try:
        while error <= 3:
            f = open(filename)
            data = list(f)
            data_list = [data[i].strip('\n') for i, _ in enumerate(data)]
            first_line, second_line = data_list

            if first_line.split(' ')[-1] != 'YES':
                error += 1
            elif error == 3:
                report = 'Error probe:' + filename
                temperature = 0
                print(report)
                return temperature
            else:
                temperature = np.int(second_line.split('t=')[1]) / 1000
                return temperature
    except KeyboardInterrupt:
        quit()


def temp_logging_and_display():
    try:
        p = Pool()
        while True:
            dt1 = dt.now()
            temp = p.map(probe_call, colour_directory.values())
            dt2 = dt.now()
            colour_temp = OrderedDict(zip(brew_probe_numbers.keys(), temp))
            st = dt2 - dt1
            st = st.total_seconds()
            time_stamp = strftime('%H:%M:%S')
            for c, t in colour_temp.items():
                session.add(Data(time=time_stamp, brew_probe=brew_probe_numbers[c], temperature=t, sample_time=st))
                session.commit()
            display_string = ', '.join([i + ' = ' + str(j) for i, j in zip(colour_positions.values(), temp)])
            os.system('clear')
            print(display_string)
    except KeyboardInterrupt:
        quit()

temp_logging_and_display()
