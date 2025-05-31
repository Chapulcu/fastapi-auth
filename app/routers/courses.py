from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.course import CourseResponse, CourseCreate, CourseUpdate, CourseEnrollmentResponse, CourseProgress
from ..services.course import (
    get_courses, get_course, get_course_by_slug, create_course, update_course, delete_course,
    enroll_user_to_course, get_user_enrollments, update_course_progress
)
from ..utils.dependencies import get_current_active_user, require_admin, require_manager_or_admin
from ..models.user import User

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    courses = get_courses(db, skip=skip, limit=limit, category_id=category_id, featured=featured)
    return courses

@router.get("/featured", response_model=List[CourseResponse])
async def list_featured_courses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    courses = get_courses(db, skip=skip, limit=limit, featured=True)
    return courses

@router.get("/my-enrollments", response_model=List[CourseEnrollmentResponse])
async def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enrollments = get_user_enrollments(db, current_user.id)
    return enrollments

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Add progress information if user is enrolled
    from ..models.course import CourseEnrollment
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course_id
    ).first()
    
    if enrollment:
        course.progress = CourseProgress(
            current_step=enrollment.current_step,
            completed=enrollment.completed_steps
        )
    
    return course

@router.get("/slug/{slug}", response_model=CourseResponse)
async def get_course_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    course = get_course_by_slug(db, slug)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Add progress information if user is enrolled
    from ..models.course import CourseEnrollment
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.user_id == current_user.id,
        CourseEnrollment.course_id == course.id
    ).first()
    
    if enrollment:
        course.progress = CourseProgress(
            current_step=enrollment.current_step,
            completed=enrollment.completed_steps
        )
    
    return course

@router.post("/", response_model=CourseResponse)
async def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_admin)
):
    # Check if slug already exists
    if get_course_by_slug(db, course.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this slug already exists"
        )
    
    return create_course(db, course)

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course_by_id(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_admin)
):
    course = update_course(db, course_id, course_update)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.delete("/{course_id}")
async def delete_course_by_id(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if not delete_course(db, course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return {"message": "Course deleted successfully"}

@router.post("/{course_id}/enroll", response_model=CourseEnrollmentResponse)
async def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if course exists
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrollment = enroll_user_to_course(db, current_user.id, course_id)
    return enrollment

@router.put("/{course_id}/progress")
async def update_my_progress(
    course_id: int,
    current_step: int,
    completed_steps: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    enrollment = update_course_progress(db, current_user.id, course_id, current_step, completed_steps)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found. Please enroll in the course first."
        )
    
    return {"message": "Progress updated successfully"}