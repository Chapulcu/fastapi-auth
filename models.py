from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

# Association table for many-to-many relationship between courses and steps
course_steps = Table(
    'course_steps',
    Base.metadata,
    Column('course_id', String, ForeignKey('courses.id'), primary_key=True),
    Column('step_id', String, ForeignKey('steps.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    course_progress = relationship("CourseProgress", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    
    # Relationships
    courses = relationship("Course", back_populates="category_rel")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, ForeignKey("categories.slug"), nullable=False)
    duration = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category_rel = relationship("Category", back_populates="courses")
    steps = relationship("Step", secondary=course_steps, back_populates="courses")
    course_progress = relationship("CourseProgress", back_populates="course")

class Step(Base):
    __tablename__ = "steps"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    order = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    
    # Relationships
    courses = relationship("Course", secondary=course_steps, back_populates="steps")

class CourseProgress(Base):
    __tablename__ = "course_progress"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    current_step = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="course_progress")
    course = relationship("Course", back_populates="course_progress")