from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


class Switch(Base):
    __tablename__ = 'switches'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), server_default="")

    fabric_id = Column(Integer, ForeignKey('fabrics.id'))
    fabric = relationship ('Fabric', back_populates='switches')

    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location', back_populates='switches')


class Fabric(Base):
    __tablename__ = "fabrics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), server_default="")

    switches = relationship('Switch', back_populates='fabric', order_by='Switch.name')


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), server_default="")

    switches = relationship('Switch', back_populates='location', order_by='Switch.name')

