from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

# Import database
from database import get_db, engine

# Import models - tek Base kullanıyoruz
from models import Base

# Import routers
from routers.academy import router as academy_router
from routers.auth import router as auth_router

# Import auth dependencies for the import fix
from auth.dependencies import get_current_user

load_dotenv()

# Create tables - tek Base ile
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academy API",
    description="FastAPI backend for Academy application with Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(academy_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Academy API with Authentication",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Initialize academy data on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database with sample data"""
    try:
        from init_academy_data import init_academy_data
        init_academy_data()
        print("Academy data initialized successfully!")
    except Exception as e:
        print(f"Warning: Could not initialize academy data: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)