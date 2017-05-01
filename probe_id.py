from glob import glob

# This program allows the user to view the available w-1 devices and name the position of each probe according to the
# serial number. It takes an input separated by a comma and creates the device directory. It returns a list of the
# various probe positions as well as their directories on the Pi.


def probe_identifier():
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
    logging_positions = []
    logging_directories = []
    hl_probe = []
    for i, j in zip(positions, device_files):
        if i == 'HL':
            hl_probe = [i, j]
        elif i != 'na' and i != 'HL':
            logging_positions.append(i)
            logging_directories.append(j)
    return logging_positions, logging_directories, hl_probe

