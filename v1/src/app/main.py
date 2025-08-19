"""Main application entry point for Document Reader."""

import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Document Reader API",
    description="API for processing documents using various technologies",
    version="1.0.0",
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


def create_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = Path(settings.output_directory)
    if not output_dir.exists():
        logger.info(f"Creating output directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)


def start():
    """Start the application."""
    # Create output directory
    create_output_directory()
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    start()