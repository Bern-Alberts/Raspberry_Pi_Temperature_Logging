from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy import create_engine

Base = declarative_base()


class Style(Base):
    __tablename__ = 'styles'

    id = Column(Integer, primary_key=True)
    style = Column(String, nullable=False)


class Probe(Base):
    __tablename__ = 'probes'

    id = Column(Integer, primary_key=True)
    position = Column(String, nullable=False)
    colour = Column(String, nullable=False)
    serial = Column(String, nullable=False)


class Brew(Base):
    __tablename__ = 'brews'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    style_id = Column(Integer, ForeignKey('styles.id'))
    styles = relationship("Style")


class Brew_probe(Base):
    __tablename__ = 'brew_probes'

    id = Column(Integer, primary_key=True)
    brew_id = Column(Integer, ForeignKey('brews.id'))
    probe_id = Column(Integer, ForeignKey('probes.id'))
    brews = relationship("Brew")
    probes = relationship("Probe")


class Data(Base):
    __tablename__ = 'data'

    time = Column(String, primary_key=True)
    brew_probe = Column(Integer, ForeignKey('brew_probes.id'), primary_key=True)
    temperature = Column(Float)
    sample_time = Column(Float)
    brew_probes = relationship('Brew_probe')

engine = create_engine('sqlite:///brewery_database.db')
Base.metadata.create_all(engine)
