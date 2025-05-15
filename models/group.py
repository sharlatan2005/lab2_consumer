from sqlalchemy import Integer, String
from sqlalchemy import Column, ForeignKey
from .base import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    faculty_id = Column(Integer, ForeignKey('faculties.id'))