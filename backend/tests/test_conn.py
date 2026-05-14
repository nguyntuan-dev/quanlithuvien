from sqlalchemy import create_engine
import os

DATABASE_URL = "postgresql://postgres:18112006@localhost:5432/thu_vien_db"
engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 3})

try:
    print("Connecting to DB...")
    with engine.connect() as conn:
        print("Success!")
except Exception as e:
    print(f"Failed: {e}")
