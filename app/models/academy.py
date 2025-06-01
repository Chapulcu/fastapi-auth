from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

# Academy models are now using integer IDs instead of UUIDs
# to be consistent with the app/ directory structure

# CourseProgress model is the only model we need from academy.py
# since Category and Course models are already defined in their respective files
class CourseProgress(Base):
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    step_id = Column(Integer, ForeignKey("course_steps.id"))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="course_progress")
    course = relationship("Course", backref="progress")
    step = relationship("CourseStep", backref="progress")