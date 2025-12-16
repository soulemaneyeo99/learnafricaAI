from typing import Optional, List
from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    level: str = "beginner"
    thumbnail_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    user_id: int
    progress: float
    status: str

    class Config:
        from_attributes = True
