from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL = f"postgresql+psycopg://postgres:{DATABASE_PASSWORD}@localhost:5432/gigkit"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(engine)

def get_session():
    with SessionLocal() as session:
        yield session

    