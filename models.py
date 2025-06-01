from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

# Many-to-many relationship table for course steps
course_steps = Table(
    'course_steps',
    Base.metadata,
    Column('course_id', String, ForeignKey('courses.id'), primary_key=True),
    Column('step_id', String, ForeignKey('steps.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course_progress = relationship("CourseProgress", back_populates="user_rel")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    
    # Relationship
    courses = relationship("Course", back_populates="category_rel")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String, ForeignKey('categories.slug'), nullable=False)
    duration = Column(Integer, default=0)  # in minutes
    total_steps = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    featured = Column(Boolean, default=False)
    
    # Relationships
    category_rel = relationship("Category", back_populates="courses")
    steps = relationship("Step", secondary=course_steps, back_populates="courses")
    progress_records = relationship("CourseProgress", back_populates="course_rel")

class Step(Base):
    __tablename__ = "steps"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(300))
    content = Column(Text)
    
    # Relationships
    courses = relationship("Course", secondary=course_steps, back_populates="steps")

class CourseProgress(Base):
    __tablename__ = "course_progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    current_step = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    
    # Relationships
    user_rel = relationship("User", back_populates="course_progress")
    course_rel = relationship("Course", back_populates="progress_records")