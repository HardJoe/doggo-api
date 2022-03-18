from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    breed = Column(String(50))
    age = Column(Integer)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    dog_name = Column(String(50), ForeignKey("dogs.name"), nullable=False)
    path = Column(String(100))
