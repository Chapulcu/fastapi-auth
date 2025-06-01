from .database import SessionLocal
from .models.category import Category
from .models.course import Course, CourseStep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_academy_data():
    db = SessionLocal()
    try:
        # Kategoriler varsa çık
        if db.query(Category).first():
            logger.info("Academy data already exists")
            return
        
        # Kategorileri oluştur
        categories_data = [
            {"title": "Web", "slug": "web"},
            {"title": "Firebase", "slug": "firebase"},
            {"title": "Cloud", "slug": "cloud"},
            {"title": "Android", "slug": "android"},
        ]
        
        category_map = {}
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            db.flush()  # ID'leri almak için flush yapıyoruz
            category_map[cat_data["slug"]] = category.id
        
        db.commit()
        logger.info("Categories created")
        
        # Kursları oluştur
        courses_data = [
            {
                "title": "Basics of Angular",
                "slug": "basics-of-angular",
                "description": "Introductory course for Angular and framework basics",
                "category_id": category_map["web"],
                "duration": 30,
                "featured": True,
            },
            {
                "title": "Basics of TypeScript",
                "slug": "basics-of-typescript",
                "description": "Beginner course for Typescript and its basics",
                "category_id": category_map["web"],
                "duration": 60,
                "featured": True,
            },
            {
                "title": "Cloud Functions",
                "slug": "cloud-functions",
                "description": "Introductory course for Firebase Cloud Functions",
                "category_id": category_map["firebase"],
                "duration": 45,
                "featured": False,
            },
        ]
        
        course_map = {}
        for course_data in courses_data:
            course = Course(**course_data)
            db.add(course)
            db.flush()  # ID'leri almak için flush yapıyoruz
            course_map[course_data["slug"]] = course.id
        
        db.commit()
        logger.info("Courses created")
        
        # Kurs adımlarını oluştur
        steps_data = [
            # Angular kurs adımları
            {
                "course_id": course_map["basics-of-angular"],
                "step_order": 1,  # Changed from 'order' to 'step_order'
                "title": "Introduction to Angular",
                "subtitle": "Learn the basics of Angular framework",
                "content": "Angular is a platform for building mobile and desktop web applications.",
            },
            {
                "course_id": course_map["basics-of-angular"],
                "step_order": 2,  # Changed from 'order' to 'step_order'
                "title": "Components",
                "subtitle": "Learn about Angular components",
                "content": "Components are the main building block for Angular applications.",
            },
            # TypeScript kurs adımları
            {
                "course_id": course_map["basics-of-typescript"],
                "step_order": 1,  # Changed from 'order' to 'step_order'
                "title": "Introduction to TypeScript",
                "subtitle": "Learn the basics of TypeScript",
                "content": "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.",
            },
            # Firebase kurs adımları
            {
                "course_id": course_map["cloud-functions"],
                "step_order": 1,  # Changed from 'order' to 'step_order'
                "title": "Introduction to Cloud Functions",
                "subtitle": "Learn the basics of Firebase Cloud Functions",
                "content": "Firebase Cloud Functions let you automatically run backend code in response to events triggered by Firebase features.",
            },
        ]
        
        for step_data in steps_data:
            step = CourseStep(**step_data)
            db.add(step)
        
        db.commit()
        logger.info("Course steps created")
        
        logger.info("Academy data initialization completed successfully")
    except Exception as e:
        logger.error(f"Error initializing academy data: {e}")
        db.rollback()
        raise
    finally:
        db.close()