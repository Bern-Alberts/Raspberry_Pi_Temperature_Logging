from glob import glob
from collections import OrderedDict

# This program allows the user to view the available w-1 devices and name the position of each probe according to the
# serial number. It takes an input separated by a comma and creates the device directory. It returns a list of the
# various probe positions as well as their directories on the Pi.

known_probes = OrderedDict([('blue', '0316881b94ff'), ('green', '04169192eaff'),
                     ('red', '031688e6a2ff'), ('yellow', '0316883c4eff')])

conventional_positions = OrderedDict([('blue', 'Ambient'), ('green', 'Mash top'),
                               ('red', 'Mash bottom'), ('yellow', 'Hot liquor')])


def probe_identifier():
    available_probes = known_probes.copy()
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob(base_dir + '28*')[:]
    device_files = [device_folder[i] + '/w1_slave' for i, _ in enumerate(device_folder)]
    device_serials = [device_folder[i].strip('/sys/bus/w1/devices/28-') for i, _ in enumerate(device_folder)]

    if len(known_probes) != len(device_serials):
        unavailable_probe = available_probes.copy()
        for i in device_serials:
            for j, k in known_probes.items():
                if i == k:
                    del unavailable_probe[j]
        for i, j in unavailable_probe.items():
            del available_probes[i]
            print('Unavailable probes:', i, '-', j)

    link = available_probes.copy()
    for i, j in link.items():
        for k, l in enumerate(device_serials):
            if j == l:
                link.update([(i, device_files[k])])

    while True:
        if known_probes == available_probes:
            print('All know probes available.\n')
            x = input('Conventional set-up:\n'
                      'Hot liquor - red\n'
                      'Mash bottom - yellow\n'
                      'Mash top - green\n'
                      'Ambient - blue\n\n'
                      'Enter "y" to continue or "n" to indicate new positions.\n')
            if x == 'y':
                return conventional_positions, link
            elif x == 'n':
                positions = input("Enter desired positions by colour and position\n"
                                  "i.e. blue-Neverland, yellow-Niffelheim etc.\n")
                new = positions.strip().split(', ')
                for i in new:
                    new_key, new_value = i.split('-')
                    new_positions = available_probes.copy()
                    new_positions.update([(new_key, new_value)])
                    return new_positions, link
                return False
            else:
                print("Try again, please follow the instructions.")
                return True
        if known_probes != available_probes:
            x = input('Probes missing, to continue with available probes enter "y", to cancel enter "n".\n')
            if x == 'y':
                positions = input("Enter desired positions by colour and position\n"
                                  "i.e. blue-Neverland, yellow-Niffelheim etc.\n")
                new = positions.strip().split(', ')
                print(new)
                for i in new:
                    new_key, new_value = i.split('-')
                    new_positions = available_probes.copy()
                    new_positions.update([(new_key, new_value)])
                    print(new_positions.items())
                    return new_positions, link
            if x == 'n':
                quit()
