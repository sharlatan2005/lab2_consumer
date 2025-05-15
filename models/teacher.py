from sqlalchemy import Integer, String
from sqlalchemy import Column
from .base import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)