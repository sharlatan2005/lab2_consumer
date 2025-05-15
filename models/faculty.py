from sqlalchemy import Integer, String
from sqlalchemy import Column
from .base import Base

class Faculty(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True)
    name = Column(String)