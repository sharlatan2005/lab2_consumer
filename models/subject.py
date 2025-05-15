from sqlalchemy import Integer, String
from sqlalchemy import Column
from .base import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)