from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, users
from .config import settings

# Database tablolarını oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Authentication Service",
    description="JWT Authentication with Role-based Access Control",
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

# Routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "FastAPI Authentication Service is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
