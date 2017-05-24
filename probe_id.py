from glob import glob
from collections import OrderedDict

# This program allows the user to view the available w-1 devices and name the position of each probe according to the
# serial number. It takes an input separated by a comma and creates the device directory. It returns a list of the
# various probe positions as well as their directories on the Pi.

from sqlalchemy import create_engine
from brewery_db_delcarative import Base, Probe
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///brewery_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

known_probes = OrderedDict()
conventional_positions = OrderedDict()
colour_id = OrderedDict()
colour_serial = OrderedDict()

for x in session.query(Probe).order_by(Probe.id):
    known_probes.update([(x.colour, x.serial)])
    conventional_positions.update([(x.colour, x.position)])
    colour_id.update([(x.colour, x.id)])


def probe_identifier():

    available_probes = known_probes.copy()
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob(base_dir + '28*')[:]
    device_files = [device_folder[i] + '/w1_slave' for i, _ in enumerate(device_folder)]
    device_serials = [device_folder[i].strip('/sys/bus/w1/devices/28-') for i, _ in enumerate(device_folder)]

    if len(known_probes) != len(device_serials):
        unavailable_probe = known_probes.copy()
        for i in device_serials:
            for j, k in known_probes.items():
                if i == k:
                    del unavailable_probe[j]
        for i, j in unavailable_probe.items():
            del available_probes[i]
            print('Unavailable probe:', i, '-', j)

    for i, j in available_probes.items():
        for k, l in enumerate(device_serials):
            if j == l:
                colour_serial.update([(i, device_files[k])])

    while True:
        if known_probes == available_probes:
            print('All known probes available.\n')
            x = input('Conventional set-up:\n'
                      'Hot liquor - red\n'
                      'Mash bottom - yellow\n'
                      'Mash top - green\n'
                      'Ambient - blue\n\n'
                      'Enter "y" to continue or "n" to indicate new positions.\n')
            if x == 'y':
                return conventional_positions, colour_serial, colour_id
            elif x == 'n':
                positions = input("Enter desired positions by colour and position\n"
                                  "i.e. blue-Neverland, yellow-Niffelheim etc.\n")
                new = positions.strip().split(', ')
                new_positions = OrderedDict()
                for i in new:
                    new_key, new_value = i.split('-')
                    new_positions.update([(new_key, new_value)])
                return new_positions, colour_serial, colour_id

            else:
                print("Try again, please follow the instructions.")
                return True

        if known_probes != available_probes:
            x = input('Probes missing, to continue with available probes enter "y", to cancel enter "n".\n')
            if x == 'y':
                for i, j in available_probes.items():
                    print('Available probe: ', i, '-', j)
                positions = input("Enter desired positions by colour and position\n"
                                  "i.e. pink-Neverland, tangerine-Niffelheim etc.\n")
                new = positions.strip().split(', ')
                new_positions = OrderedDict()
                for i in new:
                    new_key, new_value = i.split('-')
                    new_positions.update([(new_key, new_value)])
                return new_positions, colour_serial, colour_id
            if x == 'n':
                quit()

session.close_all()
