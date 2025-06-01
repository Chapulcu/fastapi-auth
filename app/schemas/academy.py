from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .category import CategoryResponse

class CourseStepBase(BaseModel):
    order: int
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None

class CourseStepCreate(CourseStepBase):
    pass

class CourseStepUpdate(BaseModel):
    order: Optional[int] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None

class CourseStepResponse(CourseStepBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CourseProgressBase(BaseModel):
    current_step: int = 0
    completed: bool = False

class CourseProgressCreate(CourseProgressBase):
    user_id: int
    course_id: int

class CourseProgressUpdate(BaseModel):
    current_step: Optional[int] = None
    completed: Optional[bool] = None

class CourseProgressResponse(CourseProgressBase):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True