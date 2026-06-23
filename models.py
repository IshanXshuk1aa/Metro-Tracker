from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Line(Base):
    __tablename__ = "line"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color_hex = Column(String, nullable=False)

    stations = relationship("Station", back_populates="line")
    trips = relationship("Trip", back_populates="line")


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    line_id = Column(Integer, ForeignKey("line.id"))
    order_index = Column(Integer, nullable=False)

    line = relationship("Line", back_populates="stations")


class Train(Base):
    __tablename__ = "train"

    id = Column(Integer, primary_key=True, index=True)
    train_no = Column(String, nullable=False, unique=True)

    trips = relationship("Trip", back_populates="train")


class Trip(Base):
    __tablename__ = "trip"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("train.id"))
    line_id = Column(Integer, ForeignKey("line.id"))
    direction = Column(String, nullable=False)
    status = Column(String, nullable=False)

    train = relationship("Train", back_populates="trips")
    line = relationship("Line", back_populates="trips")


class Interchange(Base):
    __tablename__ = "interchange"

    id = Column(Integer, primary_key=True, index=True)

    station_a_id = Column(Integer, ForeignKey("station.id"))
    station_b_id = Column(Integer, ForeignKey("station.id"))

    station_a = relationship(
        "Station",
        foreign_keys=[station_a_id]
    )

    station_b = relationship(
        "Station",
        foreign_keys=[station_b_id]
    )