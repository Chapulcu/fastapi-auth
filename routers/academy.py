from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from crud.academy import academy_crud
from schemas.academy import Category, Course, CourseList, Step, CategoryCreate, CourseCreate, StepCreate

router = APIRouter(prefix="/api/apps/academy", tags=["Academy"])

@router.get("/categories", response_model=List[Category])
async def get_categories(db: Session = Depends(get_db)):
    """Get all course categories sorted alphabetically by title."""
    categories = academy_crud.get_categories(db)
    return categories

@router.get("/courses", response_model=List[CourseList])
async def get_courses(db: Session = Depends(get_db)):
    """Get all courses."""
    courses = academy_crud.get_courses(db)
    
    # Format updated_at for frontend
    for course in courses:
        if hasattr(course, 'updated_at') and course.updated_at:
            course.updated_at = course.updated_at.strftime("%b %d, %Y")
    
    return courses

@router.get("/courses/course", response_model=Course)
async def get_course(
    id: str = Query(..., description="Course ID"),
    db: Session = Depends(get_db)
):
    """Get a specific course by ID with steps."""
    course = academy_crud.get_course_by_id(db, id)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Format updated_at for frontend
    if hasattr(course, 'updated_at') and course.updated_at:
        course.updated_at = course.updated_at.strftime("%b %d, %Y")
    
    return course

@router.post("/categories", response_model=Category)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new course category."""
    existing = academy_crud.get_category_by_slug(db, category.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    return academy_crud.create_category(db, category)

@router.post("/courses", response_model=Course)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    """Create a new course."""
    category = academy_crud.get_category_by_slug(db, course.category)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    return academy_crud.create_course(db, course)