from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.academy import CourseProgress
from ..models.category import Category
from ..models.course import Course, CourseStep
from ..schemas.academy import CourseProgressCreate, CourseProgressUpdate

# Category services are already defined in category.py
# Course services are already defined in course.py

# Additional academy services
def get_course_progress(db: Session, user_id: int, course_id: int) -> Optional[CourseProgress]:
    return db.query(CourseProgress).filter(
        CourseProgress.user_id == user_id,
        CourseProgress.course_id == course_id
    ).first()

def get_user_progress(db: Session, user_id: int) -> List[CourseProgress]:
    return db.query(CourseProgress).filter(CourseProgress.user_id == user_id).all()

def create_course_progress(db: Session, progress: CourseProgressCreate) -> CourseProgress:
    db_progress = CourseProgress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def update_course_progress(db: Session, user_id: int, course_id: int, progress_update: CourseProgressUpdate) -> Optional[CourseProgress]:
    db_progress = get_course_progress(db, user_id, course_id)
    if not db_progress:
        return None
    
    update_data = progress_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_progress, field, value)
    
    db.commit()
    db.refresh(db_progress)
    return db_progress