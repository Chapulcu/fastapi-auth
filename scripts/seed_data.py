from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.category import Category
from app.models.course import Course, CourseStep
from app.models.user import User

def seed_categories(db: Session):
    categories_data = [
        {"title": "Web", "slug": "web"},
        {"title": "Firebase", "slug": "firebase"},
        {"title": "Cloud", "slug": "cloud"},
        {"title": "Android", "slug": "android"},
    ]
    
    for cat_data in categories_data:
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
    
    db.commit()

def seed_courses(db: Session):
    # Get categories
    web_cat = db.query(Category).filter(Category.slug == "web").first()
    firebase_cat = db.query(Category).filter(Category.slug == "firebase").first()
    cloud_cat = db.query(Category).filter(Category.slug == "cloud").first()
    android_cat = db.query(Category).filter(Category.slug == "android").first()
    
    courses_data = [
        {
            "title": "Basics of Angular",
            "slug": "basics-of-angular",
            "description": "Introductory course for Angular and framework basics",
            "category_id": web_cat.id,
            "duration": 30,
            "total_steps": 11,
            "featured": True
        },
        {
            "title": "Basics of TypeScript",
            "slug": "basics-of-typescript",
            "description": "Beginner course for Typescript and its basics",
            "category_id": web_cat.id,
            "duration": 60,
            "total_steps": 11,
            "featured": True
        },
        {
            "title": "Android N: Quick Settings",
            "slug": "android-n-quick-settings",
            "description": "Step by step guide for Android N: Quick Settings",
            "category_id": android_cat.id,
            "duration": 120,
            "total_steps": 11,
            "featured": False
        },
        {
            "title": "Build an App for the Google Assistant with Firebase",
            "slug": "build-an-app-for-the-google-assistant-with-firebase",
            "description": "Dive deep into Google Assistant apps using Firebase",
            "category_id": firebase_cat.id,
            "duration": 30,
            "total_steps": 11,
            "featured": False
        },
        {
            "title": "Cloud Functions for Firebase",
            "slug": "cloud-functions-for-firebase",
            "description": "Beginners guide of Firebase Cloud Functions",
            "category_id": firebase_cat.id,
            "duration": 45,
            "total_steps": 11,
            "featured": False
        }
    ]
    
    for course_data in courses_data:
        existing = db.query(Course).filter(Course.slug == course_data["slug"]).first()
        if not existing:
            course = Course(**course_data)
            db.add(course)
            db.commit()
            db.refresh(course)
            
            # Add sample steps
            steps_data = [
                {"order": 0, "title": "Introduction", "subtitle": "Course introduction"},
                {"order": 1, "title": "Getting Started", "subtitle": "Setup and basics"},
                {"order": 2, "title": "Core Concepts", "subtitle": "Understanding the fundamentals"},
            ]
            
            for step_data in steps_data:
                step = CourseStep(**step_data, course_id=course.id)
                db.add(step)
    
    db.commit()

def main():
    db = SessionLocal()
    try:
        print("Seeding categories...")
        seed_categories(db)
        print("Seeding courses...")
        seed_courses(db)
        print("Seed data completed!")
    finally:
        db.close()

if __name__ == "__main__":
    main()