# This will contain the database connection

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import DATABASEURL

engine = create_engine(DATABASEURL)

db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# access the database
def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()