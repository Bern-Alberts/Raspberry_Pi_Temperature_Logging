import os
import glob
import time
import datetime as dt
import numpy as np

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[:]
device_file = [d + '/w1_slave' for d in device_folder]


def read_raw(i):
    f = open(device_file[i], 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(i):
    lines = read_raw(i)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != 1:
        t_string = lines[1][equals_pos + 2:]
        t_c = float(t_string) / 1000
        t_f = np.round_((t_c * 9 / 5 + 32), 3)
        return t_c, t_f


print('device files', device_file)

write_path = '/home/pi/pyfiles/log_test.csv'
mode = 'a' if os.path.exists(write_path) else 'w'

with open(write_path, mode) as f:
    f.write("Date & time, T1, T2, T3, T4\n")

    t_ini = dt.datetime.now()
    del_t = dt.timedelta(0, 10)
    t_fin = t_ini + del_t

    while t_ini < t_fin:
        now = dt.datetime.now().strftime("%y/%m/%d-%H:%M:%S")
        t_p0 = read_temp(0)[0]
        t_p1 = read_temp(1)[0]
        t_p2 = read_temp(2)[0]
        t_p3 = read_temp(3)[0]
        f.write(str(now) + "," + str(t_p0) + "," + str(t_p1) + "," + str(t_p2) + "," + str(t_p3) + "\n")
        f.flush()
        time.sleep(1)
        t_ini = dt.datetime.now()

f.close()
