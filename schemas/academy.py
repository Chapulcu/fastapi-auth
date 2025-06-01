from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    title: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: str
    
    class Config:
        from_attributes = True

class StepBase(BaseModel):
    order: int
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: str
    
    class Config:
        from_attributes = True

class CourseProgressBase(BaseModel):
    current_step: int = 0
    completed: int = 0

class CourseProgress(CourseProgressBase):
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    category: str
    duration: int = 0
    featured: bool = False

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[int] = None
    featured: Optional[bool] = None

class Course(CourseBase):
    id: str
    total_steps: int
    updated_at: datetime
    progress: Optional[CourseProgress] = None
    steps: Optional[List[Step]] = None
    
    class Config:
        from_attributes = True

class CourseList(CourseBase):
    id: str
    total_steps: int
    updated_at: datetime
    progress: Optional[CourseProgress] = None
    
    class Config:
        from_attributes = True