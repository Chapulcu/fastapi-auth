from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.course import Course, CourseStep, CourseEnrollment
from ..models.user import User
from ..schemas.course import CourseCreate, CourseUpdate, CourseStepCreate

def get_courses(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, featured: Optional[bool] = None) -> List[Course]:
    query = db.query(Course).options(joinedload(Course.category_rel))
    
    if category_id:
        query = query.filter(Course.category_id == category_id)
    if featured is not None:
        query = query.filter(Course.featured == featured)
    
    return query.offset(skip).limit(limit).all()

def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.query(Course).options(
        joinedload(Course.category_rel),
        joinedload(Course.steps)
    ).filter(Course.id == course_id).first()

def get_course_by_slug(db: Session, slug: str) -> Optional[Course]:
    return db.query(Course).options(
        joinedload(Course.category_rel),
        joinedload(Course.steps)
    ).filter(Course.slug == slug).first()

def create_course(db: Session, course: CourseCreate) -> Course:
    course_data = course.dict(exclude={'steps'})
    db_course = Course(**course_data)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    
    # Add steps if provided
    if course.steps:
        for step_data in course.steps:
            db_step = CourseStep(**step_data.dict(), course_id=db_course.id)
            db.add(db_step)
        
        db_course.total_steps = len(course.steps)
        db.commit()
        db.refresh(db_course)
    
    return db_course

def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Optional[Course]:
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    
    update_data = course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int) -> bool:
    db_course = get_course(db, course_id)
    if not db_course:
        return False
    
    db.delete(db_course)
    db.commit()
    return True

def enroll_user_to_course(db: Session, user_id: int, course_id: int) -> Optional[CourseEnrollment]:
    # Check if already enrolled
    existing = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id
    ).first()
    
    if existing:
        return existing
    
    enrollment = CourseEnrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def get_user_enrollments(db: Session, user_id: int) -> List[CourseEnrollment]:
    return db.query(CourseEnrollment).options(
        joinedload(CourseEnrollment.course).joinedload(Course.category_rel)
    ).filter(CourseEnrollment.user_id == user_id).all()

def update_course_progress(db: Session, user_id: int, course_id: int, current_step: int, completed_steps: int) -> Optional[CourseEnrollment]:
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        return None
    
    enrollment.current_step = current_step
    enrollment.completed_steps = completed_steps
    db.commit()
    db.refresh(enrollment)
    return enrollment