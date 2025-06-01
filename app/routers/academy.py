from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.academy import CourseProgress
from ..models.category import Category
from ..models.course import Course, CourseStep
from ..models.user import User
from ..schemas.category import CategoryResponse
from ..schemas.course import CourseResponse
from ..schemas.academy import CourseProgressResponse, CourseProgressCreate, CourseProgressUpdate
from ..services.category import get_categories, get_category
from ..services.course import get_courses, get_course
from ..services.academy import get_course_progress, create_course_progress, update_course_progress
from ..utils.dependencies import get_current_active_user
import logging

# Logging ekleyin
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/apps/academy", tags=["Academy"])

@router.get("/test")
async def test_endpoint():
    """Test endpoint to check if router works"""
    return {"message": "Academy router is working!"}

@router.get("/categories", response_model=List[CategoryResponse])
async def get_all_categories(db: Session = Depends(get_db)):
    """Get all course categories sorted alphabetically by title."""
    try:
        categories = get_categories(db)
        logger.info(f"Found {len(categories)} categories")
        return categories
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/courses", response_model=List[CourseResponse])
async def get_all_courses(
    db: Session = Depends(get_db),
    category_id: Optional[int] = None,
    featured: Optional[bool] = None
):
    """Get all courses with optional filtering."""
    try:
        courses = get_courses(db, category_id=category_id, featured=featured)
        logger.info(f"Found {len(courses)} courses")
        return courses
    except Exception as e:
        logger.error(f"Error getting courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course_by_id(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course by ID."""
    try:
        course = get_course(db, course_id)
        if not course:
            logger.warning(f"Course with ID {course_id} not found")
            raise HTTPException(status_code=404, detail="Course not found")
        logger.info(f"Found course: {course.title}")
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course {course_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress/{course_id}", response_model=CourseProgressResponse)
async def get_user_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the current user's progress for a specific course."""
    try:
        progress = get_course_progress(db, current_user.id, course_id)
        if not progress:
            logger.warning(f"No progress found for user {current_user.id} in course {course_id}")
            raise HTTPException(status_code=404, detail="Course progress not found")
        logger.info(f"Found progress for user {current_user.id} in course {course_id}")
        return progress
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting progress for user {current_user.id} in course {course_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/progress/{course_id}", response_model=CourseProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_user_course_progress(
    course_id: int,
    progress: CourseProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create progress record for the current user in a specific course."""
    try:
        # Check if progress already exists
        existing_progress = get_course_progress(db, current_user.id, course_id)
        if existing_progress:
            logger.warning(f"Progress already exists for user {current_user.id} in course {course_id}")
            raise HTTPException(status_code=400, detail="Progress already exists for this course")
        
        # Ensure the progress is for the current user and course
        progress_data = progress.dict()
        progress_data["user_id"] = current_user.id
        progress_data["course_id"] = course_id
        
        new_progress = create_course_progress(db, CourseProgressCreate(**progress_data))
        logger.info(f"Created progress for user {current_user.id} in course {course_id}")
        return new_progress
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating progress for user {current_user.id} in course {course_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/progress/{course_id}", response_model=CourseProgressResponse)
async def update_user_course_progress(
    course_id: int,
    progress_update: CourseProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update the current user's progress for a specific course."""
    try:
        updated_progress = update_course_progress(db, current_user.id, course_id, progress_update)
        if not updated_progress:
            logger.warning(f"No progress found to update for user {current_user.id} in course {course_id}")
            raise HTTPException(status_code=404, detail="Course progress not found")
        logger.info(f"Updated progress for user {current_user.id} in course {course_id}")
        return updated_progress
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating progress for user {current_user.id} in course {course_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))