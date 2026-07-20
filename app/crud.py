from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from . import models, schemas
from typing import List, Optional

def create_skill(db: Session, skill: schemas.SkillBase) -> models.Skill:
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def get_or_create_skill(db: Session, name: str) -> models.Skill:
    skill = db.query(models.Skill).filter(models.Skill.name == name).first()
    if skill:
        return skill
    return create_skill(db, schemas.SkillBase(name=name))

def create_location(db: Session, loc: schemas.LocationBase) -> models.Location:
    db_loc = models.Location(**loc.model_dump())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def get_or_create_location(db: Session, city: str, country: str, region: Optional[str]) -> models.Location:
    loc = db.query(models.Location).filter(
        models.Location.city == city,
        models.Location.country == country,
        (models.Location.region == region) if region else True
    ).first()
    if loc:
        return loc
    return create_location(db, schemas.LocationBase(city=city, country=country, region=region))

def create_job(db: Session, job: schemas.JobCreate) -> models.Job:
    
    db_skills = [get_or_create_skill(db, name) for name in job.skill_names]

    
    db_locations = []
    if job.location_data:
        loc = get_or_create_location(
            db,
            city=job.location_data.city,
            country=job.location_data.country,
            region=job.location_data.region
        )
        db_locations.append(loc)

    db_job = models.Job(
        title=job.title,
        company=job.company,
        description=job.description,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        remote=job.remote,
    )
    db_job.skills = db_skills
    db_job.locations = db_locations

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def filter_jobs(
    db: Session,
    filters: schemas.JobFilter
) -> tuple[List[models.Job], int]:
    q = db.query(models.Job)

    if filters.query:
        term = f"%{filters.query}%"
        q = q.filter(
            or_(
                models.Job.title.ilike(term),
                models.Job.description.ilike(term) if models.Job.description else False
            )
        )
    if filters.min_salary is not None:
        q = q.filter(models.Job.salary_min >= filters.min_salary)
    if filters.max_salary is not None:
        q = q.filter(models.Job.salary_max <= filters.max_salary)
    if filters.remote is not None:
        q = q.filter(models.Job.remote == filters.remote)
    if filters.skill:
        q = q.join(models.Job.skills).filter(models.Skill.name == filters.skill)
    if filters.city:
        q = q.join(models.Job.locations).filter(models.Location.city == filters.city)
    if filters.country:
        q = q.join(models.Job.locations).filter(models.Location.country == filters.country)

    total = q.count()

    offset = (filters.page - 1) * filters.per_page
    results = q.offset(offset).limit(filters.per_page).all()

    return results, total
