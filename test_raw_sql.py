from app.database import engine
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_raw_sql():
    try:
        # Use the correct method for SQLAlchemy 2.0 with columns that exist in the database
        with engine.connect() as conn:
            result = conn.execute(text("SELECT categories.id, categories.title, categories.slug FROM categories"))
            rows = result.fetchall()
            logger.info(f"Found {len(rows)} categories")
            for row in rows:
                logger.info(f"Category: {row}")
    except Exception as e:
        logger.error(f"Error executing raw SQL: {e}")

if __name__ == "__main__":
    test_raw_sql()