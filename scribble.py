from glob import glob

base_dir = '/sys/bus/w1/devices/'
device_folder = glob(base_dir + '28*')[:]
device_files = [device_folder[i] + '/w1_slave' for i, _ in enumerate(device_folder)]
device_serials = [device_folder[i].strip('/sys/bus/w1/devices/28-') for i, _ in enumerate(device_folder)]
device_serials_str = ', '.join(['(' + str(i + 1) + ') ' + device_serials[i] for i, _ in enumerate(device_serials)])
print("Available probes:\n" + device_serials_str + '.')
print("Indicate the probe position with the in the form:\n "
      "e.g. Ambient, HL, Mash tun top, Mash tun bottom\n"
      "Please indicate the hot liquor tank control probe with the name HL, ")
positions = input()
positions = positions.split(', ')
print(positions, device_files)
logging_positions = []
logging_directories = []
hl_probe = []
for i, j in zip(positions, device_files):
    print(i, j)
    if i != 'na':
        logging_positions.append(i)
        logging_directories.append(j)
#    else:
#        print()
print('fuck = ', logging_positions, logging_directories)