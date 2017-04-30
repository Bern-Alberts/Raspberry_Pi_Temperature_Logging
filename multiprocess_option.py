from multiprocessing import Pool
import subprocess
import numpy as np
import time
from datetime import datetime as dt
from probe_id import probe_identifier

device_positions, device_files = probe_identifier()

# This program calls the probe in question using its file directory as an input and the subprocess module.
# It the separates the temperature string from the rest and returns it as an integer. It contains an error process that
# will return an error message and the probe in questions filename if the probe fails to provide a temperature reading
# three times in a row, this has however not been tested.


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

# This program calls all available probes simultaneously, using the probe_call() function and prints the results to
# screen as well as returning the results. I have having trouble using it from the database program. It seems to get
# stuck when I call this program from another. Also it seems to start choking after a certain amount of time, initially
# the readings come through consistently around 1.2s but then slowly but surely every now and then the time increases to
# around 2-3s and this seems to happen more regularly the longer the program runs. I have tested another version
# "subprocess_2.py" which does not use the multiprocessing module and the problem does not occur, however, in this
# program I cannot control the order in which the readings are returned.

def temp_readings():
#    if __name__ == '__main__':
        dt1 = dt.now()
        p = Pool(4)
        temp = p.map(probe_call, device_files)
        temp_display = [str(i) + ' = ' + str(j) for i, j in zip(device_positions, temp)]
        dt2 = dt.now()
        print(', '.join(temp_display))
        print(dt2 - dt1)
        time.sleep(0.5)
        return temp

print(temp_readings())