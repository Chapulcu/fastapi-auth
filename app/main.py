from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, categories, courses, academy

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Learning Management System API",
    description="A comprehensive LMS API with authentication and course management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(courses.router)
app.include_router(academy.router)

@app.get("/")
async def root():
    return {"message": "Learning Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Initialize academy data on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database with sample data"""
    try:
        from app.init_academy_data import init_academy_data
        init_academy_data()
        print("Academy data initialized successfully!")
    except Exception as e:
        print(f"Warning: Could not initialize academy data: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
