from sqlalchemy import Column, Integer, String
from database import Base


# Define To Do class inheriting from Base
class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    breed = Column(String(50))
    age = Column(Integer)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String(100))
