import subprocess
from probe_id import probe_identifier
from datetime import datetime as dt
import numpy as np

positions, device_files = probe_identifier()


while True:
    t0 = dt.now()
    operations = ['cat ' + i for i in device_files]
    simultaneous_operation = '(' + ' & '.join(operations) + ')'
    s1 = subprocess.check_output(simultaneous_operation, shell=True)
    s1 = s1.decode(encoding='utf-8').split('\n')
    s1 = [s1[i] for i, _ in enumerate(s1) if i % 2 != 0]
    temperatures = [np.int(i.split('t=')[1]) / 1000 for i in s1]
    display = [i + ' = ' + str(j) for i, j in zip(positions, temperatures)]
    t1 = dt.now()
    print(display, t1 - t0)
