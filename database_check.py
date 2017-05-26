from datetime import date
from probe_id import probe_identifier
from collections import OrderedDict

from sqlalchemy import create_engine
from brewery_db_delcarative import Base, Style, Brew, Brew_probe
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, and_

engine = create_engine('sqlite:///brewery_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

brew_style = [input('Style to be brewed:\n')]
brew_date = str(date.today())
print(brew_date)
colour_positions, colour_directory, colour_id = probe_identifier()


def db_setup():
    style_num = 0
    (ret, ), = session.query(exists().where(Style.style.in_(brew_style)))
    if ret is True:
        print('Style exists.')
        for i, in session.query(Style.id).filter(Style.style == brew_style[0]):
            style_num = i
            print('Style id =', style_num)

    elif ret is False:
        session.add(Style(style=brew_style[0]))
        session.commit()
        print('Style added.')
        for i, in session.query(Style.id).filter(Style.style == brew_style[0]):
            style_num = i
            print('Style id =', style_num)

    brew_num = 0
    brew_probes = OrderedDict()
    (bnc, ), = session.query(exists().where((and_(Brew.style_id == style_num, Brew.date == brew_date))))

    if bnc is True:
        print('Brew exists.')
        for i, in session.query(Brew.id).filter(Brew.date == brew_date).filter(Brew.style_id == style_num):
            brew_num = i
            print('Brew id =', brew_num)

    if bnc is False:
        session.add(Brew(style_id=style_num, date=brew_date))
        session.commit()
        print('Brew created.')
        for i, in session.query(Brew.id).filter(Brew.date == brew_date).filter(Brew.style_id == style_num):
            brew_num = i
            print('Brew id =', brew_num)

    for a, i in colour_id.items():
        (bpc, ), = session.query(exists().where((and_(Brew_probe.brew_id == brew_num, Brew_probe.probe_id == i))))

        if bpc is True:
            print('Brew-probe number exists.')

            for y, in session.query(Brew_probe.id).filter(Brew_probe.brew_id == brew_num). \
                    filter(Brew_probe.probe_id == i):
                brew_probes.update([(a, y)])

        elif bpc is False:
            session.add(Brew_probe(brew_id=brew_num, probe_id=i))
            session.commit()
            print('Brew-probe number added.')

            for y, in session.query(Brew_probe.id).filter(Brew_probe.brew_id == brew_num). \
                    filter(Brew_probe.probe_id == i):
                brew_probes.update([(a, y)])

    input("Press enter to continue.")
    return brew_probes

session.close_all()
