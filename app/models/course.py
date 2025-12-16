from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, index=True) # Ex: Dev, Business, Design
    level = Column(String, default="beginner") # beginner, intermediate, advanced
    thumbnail_url = Column(String, nullable=True)
    
    # Relations (à étendre)
    # lessons = relationship("Lesson", back_populates="course")

class Enrollment(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    progress = Column(Float, default=0.0) # 0 to 100%
    status = Column(String, default="active") # active, completed
