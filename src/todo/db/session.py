from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = load_dotenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

engine = create_engine(DATABASE_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

