from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models import Job

app = FastAPI()

@app.get("/jobs")
def get_jobs():
    db = SessionLocal()
    try:
        jobs = db.query(Job).limit(20).all()  # сначала вернём 20, чтобы не спамить
        return [
            {
                "id": j.id,
                "title": j.title,
                "salary": j.salary,
                "remote": j.remote,
                "skills": [s.name for s in j.skills],
                "locations": [l.name for l in j.locations],
            }
            for j in jobs
        ]
    finally:
        db.close()
