from database import SessionLocal
from models import Category, Course, Step
import uuid

def init_academy_data():
    db = SessionLocal()
    try:
        # Kategoriler varsa çık
        if db.query(Category).first():
            print("Academy data already exists")
            return
        
        # Kategorileri oluştur
        categories_data = [
            {"id": str(uuid.uuid4()), "title": "Web", "slug": "web"},
            {"id": str(uuid.uuid4()), "title": "Firebase", "slug": "firebase"},
            {"id": str(uuid.uuid4()), "title": "Cloud", "slug": "cloud"},
            {"id": str(uuid.uuid4()), "title": "Android", "slug": "android"},
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
        
        db.commit()
        print("Categories created")
        
        # Kursları oluştur
        courses_data = [
            {
                "id": "694e4e5f-f25f-470b-bd0e-26b1d4f64028",
                "title": "Basics of Angular",
                "slug": "basics-of-angular",
                "description": "Introductory course for Angular and framework basics",
                "category": "web",
                "duration": 30,
                "total_steps": 11,
                "featured": True,
            },
            {
                "id": "f924007a-2ee9-470b-a316-8d21ed78277f",
                "title": "Basics of TypeScript",
                "slug": "basics-of-typeScript",
                "description": "Beginner course for Typescript and its basics",
                "category": "web",
                "duration": 60,
                "total_steps": 11,
                "featured": True,
            }
        ]
        
        for course_data in courses_data:
            course = Course(**course_data)
            db.add(course)
        
        db.commit()
        print("Courses created")
        
    except Exception as e:
        print(f"Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_academy_data()