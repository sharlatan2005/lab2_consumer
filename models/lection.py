from sqlalchemy import Integer, DateTime, UniqueConstraint
from sqlalchemy import Column, ForeignKey
from .base import Base

class Lection(Base):
    __tablename__ = 'lections'
    __table_args__ = (
        UniqueConstraint('id_teacher', 'id_subject', 'start_timestamp', 
                        name='uq_lection_teacher_subject_time'),
    )

    id = Column(Integer, primary_key=True)
    id_teacher = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_subject = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    start_timestamp = Column(DateTime, nullable=False)
    end_timestamp = Column(DateTime)