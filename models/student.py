from sqlalchemy import Integer, String, DateTime
from sqlalchemy import Column, ForeignKey
from .base import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
