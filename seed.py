import os
import sys
import random  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ОШИБКА: Не найден DATABASE_URL в .env")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models import Base, Job, Skill, Location, job_location, job_skill

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from faker import Faker
fake = Faker()

def seed():
    db = SessionLocal()
    try:
    
        skills = [Skill(name=fake.word()) for _ in range(10)]
        locations = [Location(name=fake.city()) for _ in range(10)]

        db.add_all(skills)
        db.add_all(locations)
        db.commit()

        
        for s in skills:
            db.refresh(s)
        for l in locations:
            db.refresh(l)

        jobs = []
        for i in range(200):
            job = Job(
                title=fake.job(),
                description=fake.text(max_nb_chars=200),
                salary=fake.random_int(min=50000, max=300000),
                remote=fake.boolean()
            )
            
            job.skills = random.sample(skills, k=min(3, len(skills)))
            job.locations = random.sample(locations, k=min(2, len(locations)))
            jobs.append(job)

        db.add_all(jobs)
        db.commit()
        print(f"✅ Успешно создано 200 вакансий!")
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при наполнении БД: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
