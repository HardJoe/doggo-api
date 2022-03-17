from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a sqlite engine instance
engine = create_engine("sqlite:///dogs.db")

# Create a DeclarativeMeta instance
Base = declarative_base()


class Dog(Base):
    # Define To Do class inheriting from Base
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    breed = Column(String(50))
    age = Column(Integer)
    image = Column(String(100))
