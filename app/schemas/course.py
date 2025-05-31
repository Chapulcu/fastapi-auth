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

class CourseProgress(BaseModel):
    current_step: int
    completed: int

class CourseBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    category_id: int
    duration: Optional[int] = None
    total_steps: Optional[int] = 0
    featured: bool = False

class CourseCreate(CourseBase):
    steps: Optional[List[CourseStepCreate]] = []

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    duration: Optional[int] = None
    total_steps: Optional[int] = None
    featured: Optional[bool] = None

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_rel: Optional[CategoryResponse] = None
    steps: Optional[List[CourseStepResponse]] = []
    progress: Optional[CourseProgress] = None

    class Config:
        from_attributes = True

class CourseEnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    current_step: int
    completed_steps: int
    enrolled_at: datetime
    course: CourseResponse

    class Config:
        from_attributes = True