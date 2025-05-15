from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_CONFIG

engine = create_engine(POSTGRES_CONFIG, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

