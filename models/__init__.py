from .faculty import Faculty
from .group import Group
from .student import Student
from .subject import Subject
from .teacher import Teacher
from .lection import Lection
from .lections_attendance import LectionsAttendance

__all__ = ['Faculty', 'Group', 'Student', 'Subject', 'Teacher',
           'Lection', 'LectionsAttendance']

tables_list = [
    Faculty.__table__,
    Group.__table__,
    Student.__table__,
    Subject.__table__,
    Teacher.__table__,
    Lection.__table__,
    LectionsAttendance.__table__
]