from multiprocessing import Pool
import subprocess
import numpy as np
import time
from datetime import datetime as dt
from probe_id import probe_identifier
from time import gmtime, strftime

colour_position, colour_id = probe_identifier()


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
            temp = p.map(probe_call, colour_id.values())
            display_string = ', '.join([i + ' = ' + str(j) for i, j in zip(colour_position.values(), temp)])
            print(display_string)
            dt2 = dt.now()
            print(dt2 - dt1)
    except KeyboardInterrupt:
        return

temp_logging_and_display()
