from database import SessionLocal, engine
from models import Base, Category, Course
import sqlalchemy

# Veritabanı bağlantısını test et
try:
    db = SessionLocal()
    
    # Tabloları kontrol et
    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in database:", tables)
    
    # Kategorileri kontrol et
    categories = db.query(Category).all()
    print(f"Categories count: {len(categories)}")
    for cat in categories:
        print(f"  - {cat.title} ({cat.slug})")
    
    # Kursları kontrol et
    courses = db.query(Course).all()
    print(f"Courses count: {len(courses)}")
    for course in courses:
        print(f"  - {course.title}")
    
    db.close()
    
except Exception as e:
    print(f"Database error: {e}")