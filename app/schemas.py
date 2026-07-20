from pydantic import BaseModel, Field
from typing import List, Optional

class SkillBase(BaseModel):
    name: str

class SkillResponse(SkillBase):
    id: int
    class Config:
        from_attributes = True

class LocationBase(BaseModel):
    city: str
    country: str
    region: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    remote: bool = False
    skill_names: List[str] = []
    location_data: Optional[LocationBase] = None  # один основной город

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    remote: bool
    skills: List[SkillResponse]
    locations: List[LocationResponse]
    class Config:
        from_attributes = True

class JobFilter(BaseModel):
    query: Optional[str] = None       # поиск по title/description
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    remote: Optional[bool] = None
    skill: Optional[str] = None        # фильтр по одному навыку
    city: Optional[str] = None
    country: Optional[str] = None
    page: int = 1
    per_page: int = 20