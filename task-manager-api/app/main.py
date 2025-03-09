from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as task_router
from app import models, database
from sqlalchemy.orm import Session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app with metadata
app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
try:
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    raise

# Include routers with versioning
app.include_router(task_router, prefix="/api/v1/tasks", tags=["tasks"])
