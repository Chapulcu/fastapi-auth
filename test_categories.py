from app.database import SessionLocal
from app.models.category import Category
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_categories():
    db = SessionLocal()
    try:
        # Try to query categories
        categories = db.query(Category).all()
        logger.info(f"Found {len(categories)} categories")
        for cat in categories:
            logger.info(f"Category: {cat.id}, {cat.title}, {cat.slug}")
    except Exception as e:
        logger.error(f"Error querying categories: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_categories()