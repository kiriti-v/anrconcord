from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import artists, health
from app.utils.logger import logger
from app.api.routes.artists import router as artists_router
from app.api.routes.health import router as health_router
from app.api.routes.emerging import router as emerging_router

# Initialize FastAPI app
app = FastAPI(
    title="Emerging Artist API",
    description="API for discovering emerging artists",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(artists_router, prefix="/artists", tags=["Artists"])
app.include_router(emerging_router)

@app.on_event("startup")
async def startup_event():
    logger.info("API server starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API server shutting down") 