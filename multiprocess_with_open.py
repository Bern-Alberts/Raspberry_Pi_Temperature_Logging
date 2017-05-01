from collections import OrderedDict
from multiprocessing import Pool
from datetime import datetime as dt
import numpy as np

from probe_id import probe_identifier

device_positions, device_files = probe_identifier()


def probe_call(filename):
    error = 0
    while error <= 3:
        f = open(filename)
        data = list(f)
        data_list = [data[i].strip('\n') for i, _ in enumerate(data)]
        first_line, second_line = data_list

        if first_line.split(' ')[-1] != 'YES':
            error += 1
        elif error == 3:
            temperature = 'Error probe:' + filename
            return temperature
        else:
            temperature = np.int(second_line.split('t=')[1]) / 1000
            return temperature


if __name__ == '__main__':
        p = Pool(4)
        while True:
            dt1 = dt.now()
            temp = p.map(probe_call, device_files)
            temp_dict = OrderedDict(zip(device_positions, temp))
            temp_display = [str(i) + ' = ' + str(j) for i, j in temp_dict.items()]
            dt2 = dt.now()
            print(', '.join(temp_display))
            print(dt2 - dt1)
