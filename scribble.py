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
    #s1 = s1.decode(encoding='utf-8').split('\n')
    print(s1)