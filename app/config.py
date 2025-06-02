from decouple import config

class Settings:
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    # DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./app.db") # Old SQLite URL
    DATABASE_URL: str = config("DATABASE_URL", default="postgresql://user:password@localhost:5432/appdb") 
    # IMPORTANT: Replace the above default URL with your actual PostgreSQL connection string
    # or set the DATABASE_URL environment variable (e.g., in a .env file).
    # Example: postgresql://your_db_user:your_db_password@your_db_host:your_db_port/your_db_name
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:4200", "http://localhost:3000"]

settings = Settings()
