from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import logging

# Logging ekleyin
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/apps/academy", tags=["Academy"])

@router.get("/test")
async def test_endpoint():
    """Test endpoint to check if router works"""
    return {"message": "Academy router is working!"}

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all course categories sorted alphabetically by title."""
    try:
        from models import Category
        categories = db.query(Category).all()
        logger.info(f"Found {len(categories)} categories")
        
        # Manuel olarak response oluşturalım
        result = []
        for cat in categories:
            result.append({
                "id": cat.id,
                "title": cat.title,
                "slug": cat.slug
            })
        
        return result
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/courses")
async def get_courses(db: Session = Depends(get_db)):
    """Get all courses."""
    try:
        from models import Course
        courses = db.query(Course).all()
        logger.info(f"Found {len(courses)} courses")
        
        # Manuel olarak response oluşturalım
        result = []
        for course in courses:
            result.append({
                "id": course.id,
                "title": course.title,
                "slug": course.slug,
                "description": course.description,
                "category": course.category,
                "duration": course.duration,
                "total_steps": course.total_steps,
                "featured": course.featured,
                "updated_at": course.updated_at.strftime("%b %d, %Y") if course.updated_at else "Unknown",
                "progress": {
                    "current_step": 0,
                    "completed": 0
                }
            })
        
        return result
    except Exception as e:
        logger.error(f"Error getting courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/courses/course")
async def get_course(
    id: str = Query(..., description="Course ID"),
    db: Session = Depends(get_db)
):
    """Get a specific course by ID with steps."""
    try:
        from models import Course, Step
        logger.info(f"Getting course with ID: {id}")
        
        course = db.query(Course).filter(Course.id == id).first()
        
        if not course:
            logger.warning(f"Course not found: {id}")
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Steps'leri al (şimdilik boş array döndürelim)
        steps = []
        
        result = {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "description": course.description,
            "category": course.category,
            "duration": course.duration,
            "total_steps": course.total_steps,
            "featured": course.featured,
            "updated_at": course.updated_at.strftime("%b %d, %Y") if course.updated_at else "Unknown",
            "progress": {
                "current_step": 0,
                "completed": 0
            },
            "steps": steps
        }
        
        logger.info(f"Found course: {course.title}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))