from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, users, categories, courses

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

@app.get("/")
async def root():
    return {"message": "Learning Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
