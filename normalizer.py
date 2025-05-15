from typing import Dict, Any
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from models import Faculty, Group, Student, Subject, Teacher, Lection, LectionsAttendance

class Normalizer:
    def __init__(self, postgres_session):
        self.postgres_session = postgres_session

    def _upsert_faculty(self, faculty_id: int, faculty_name: str):
        stmt = insert(Faculty).values(
            id=faculty_id,
            name=faculty_name
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def _upsert_group(self, group_id: int, group_name: str, faculty_id: int):
        stmt = insert(Group).values(
            id=group_id,
            name=group_name,
            faculty_id=faculty_id
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def _upsert_student(self, student_id: int, full_name: str, group_id: int):
        stmt = insert(Student).values(
            id=student_id,
            full_name=full_name,
            group_id=group_id
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def _upsert_subject(self, subject_id: int, subject_name: str):
        stmt = insert(Subject).values(
            id=subject_id,
            name=subject_name
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def _upsert_teacher(self, teacher_id: int, full_name: str):
        stmt = insert(Teacher).values(
            id=teacher_id,
            full_name=full_name
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def _upsert_lection(self, id: int, teacher_id: int, subject_id: int, 
                       start_timestamp: datetime, end_timestamp: datetime = None):
        
        stmt = insert(Lection).values(
            id=id,
            id_teacher=teacher_id,
            id_subject=subject_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        ).on_conflict_do_nothing(index_elements=['id'])
        
        self.postgres_session.execute(stmt)

    def _upsert_attendance(self, id: int, student_id: int, lection_id: int):
        stmt = insert(LectionsAttendance).values(
            id=id,
            id_student=student_id,
            id_lection=lection_id
        ).on_conflict_do_nothing(index_elements=['id'])
        self.postgres_session.execute(stmt)

    def process_message(self, message_data: Dict[str, Any]):
        try:
            # Обрабатываем факультет
            self._upsert_faculty(
                faculty_id=message_data['faculty_id'],
                faculty_name=message_data['faculty_name']
            )
            
            # Обрабатываем группу
            self._upsert_group(
                group_id=message_data['group_id'],
                group_name=message_data['group_name'],
                faculty_id=message_data['faculty_id']
            )
            
            # Обрабатываем студента
            self._upsert_student(
                student_id=message_data['student_id'],
                full_name=message_data['student_full_name'],
                group_id=message_data['group_id']
            )
            
            # Обрабатываем предмет
            self._upsert_subject(
                subject_id=message_data['subject_id'],
                subject_name=message_data['subject_name']
            )
            
            # Обрабатываем преподавателя
            self._upsert_teacher(
                teacher_id=message_data['teacher_id'],
                full_name=message_data['teacher_full_name']
            )
            
            # Обрабатываем лекцию (возвращает ID лекции)
            self._upsert_lection(
                id=message_data['lection_id'],
                teacher_id=message_data['teacher_id'],
                subject_id=message_data['subject_id'],
                start_timestamp = datetime.strptime(message_data['start_timestamp'], '%Y-%m-%d %H:%M:%S'),
                end_timestamp = (
                    datetime.strptime(message_data['end_timestamp'], '%Y-%m-%d %H:%M:%S') 
                    if message_data['end_timestamp'] 
                    else None
                )
            )
            
            # Обрабатываем посещение
            self._upsert_attendance(
                id = message_data['id'],
                student_id=message_data['student_id'],
                lection_id=message_data['lection_id']
            )
            
            self.postgres_session.commit()
            
        except Exception as e:
            self.postgres_session.rollback()
            print(f'Error processing message: {e}')
            raise