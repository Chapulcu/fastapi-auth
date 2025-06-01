from sqlalchemy.orm import Session, joinedload
from models import Category, Course, Step, CourseProgress, User
from schemas.academy import CategoryCreate, CourseCreate, StepCreate
from typing import List, Optional
import uuid

class AcademyCRUD:
    
    # Categories
    def get_categories(self, db: Session) -> List[Category]:
        return db.query(Category).order_by(Category.title).all()
    
    def get_category_by_slug(self, db: Session, slug: str) -> Optional[Category]:
        return db.query(Category).filter(Category.slug == slug).first()
    
    def create_category(self, db: Session, category: CategoryCreate) -> Category:
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    # Courses
    def get_courses(self, db: Session, user_id: Optional[str] = None) -> List[Course]:
        query = db.query(Course).options(joinedload(Course.category_rel))
        courses = query.all()
        
        # Add default progress information
        for course in courses:
            if user_id:
                progress = db.query(CourseProgress).filter(
                    CourseProgress.course_id == course.id,
                    CourseProgress.user_id == user_id
                ).first()
                
                if progress:
                    course.progress = progress
                else:
                    # Create default progress
                    course.progress = CourseProgress(current_step=0, completed=0)
            else:
                course.progress = CourseProgress(current_step=0, completed=0)
        
        return courses
    
    def get_course_by_id(self, db: Session, course_id: str, user_id: Optional[str] = None) -> Optional[Course]:
        course = db.query(Course).options(
            joinedload(Course.category_rel),
            joinedload(Course.steps)
        ).filter(Course.id == course_id).first()
        
        if course:
            if user_id:
                progress = db.query(CourseProgress).filter(
                    CourseProgress.course_id == course_id,
                    CourseProgress.user_id == user_id
                ).first()
                
                if progress:
                    course.progress = progress
                else:
                    course.progress = CourseProgress(current_step=0, completed=0)
            else:
                course.progress = CourseProgress(current_step=0, completed=0)
            
            # Sort steps by order
            if course.steps:
                course.steps.sort(key=lambda x: x.order)
        
        return course
    
    def create_course(self, db: Session, course: CourseCreate) -> Course:
        db_course = Course(**course.dict())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    
    # Steps
    def create_step(self, db: Session, step: StepCreate) -> Step:
        db_step = Step(**step.dict())
        db.add(db_step)
        db.commit()
        db.refresh(db_step)
        return db_step
    
    def add_step_to_course(self, db: Session, course_id: str, step_id: str):
        course = db.query(Course).filter(Course.id == course_id).first()
        step = db.query(Step).filter(Step.id == step_id).first()
        
        if course and step:
            course.steps.append(step)
            course.total_steps = len(course.steps)
            db.commit()
            return True
        return False

academy_crud = AcademyCRUD()