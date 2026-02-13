# Main entry point for the FastAPI application.
from fastapi import FastAPI
from db.database import engine, Base
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, notes, admin

# Create tables in database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title=settings.TITLE, version=settings.VERSION)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)

# Root endpoint for health check or welcome message
@app.get("/")
def root():
    return {"message": "Welcome to the Notes App API"}
